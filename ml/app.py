from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model_path = "rfm_model.pkl"
scaler_path = "scaler.pkl"

# Load existing model and scaler if available
if os.path.exists(model_path) and os.path.exists(scaler_path):
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
else:
    model = None
    scaler = None

def load_rfm_data(file_path):
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        df.dropna(inplace=True)

        # Check if the necessary columns are present
        if 'Quantity' not in df.columns or 'UnitPrice' not in df.columns:
            raise ValueError("Missing required columns: 'Quantity' or 'UnitPrice'")

        # Calculate 'TotalPrice' dynamically if columns exist
        df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

        today_date = pd.to_datetime("2011-12-14")
        rfm = df.groupby('CustomerID').agg({
            'InvoiceDate': lambda date: (today_date - date.max()).days,
            'InvoiceNo': 'nunique',
            'TotalPrice': 'sum'
        })
        
        rfm.columns = ["Recency", "Frequency", "Monetary"]
        rfm = rfm[rfm["Monetary"] > 0]
        return rfm
    except Exception as e:
        print(f"Error loading RFM data: {e}")
        return None


def assign_segments(rfm):
    # Example logic to assign segments based on Recency, Frequency, and Monetary values
    rfm['segment'] = np.where((rfm['Recency'] < 30) & (rfm['Frequency'] > 5) & (rfm['Monetary'] > 1000), "High-Value", "Low-Value")
    return rfm

def behavioral_trigger(segment):
    # Define your behavioral triggers based on the customer's segment
    if segment == "High-Value":
        return "Offer Discount"
    elif segment == "Low-Value":
        return "Send Reminder"
    else:
        return "No Action"

def train_model(rfm):
    try:
        rfm['Purchased_Again'] = np.random.choice([0, 1], size=len(rfm), p=[0.7, 0.3])
        X = rfm[['Recency', 'Frequency', 'Monetary']]
        y = rfm['Purchased_Again']
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        
        joblib.dump(model, model_path)
        joblib.dump(scaler, scaler_path)
        
        return model, scaler
    except Exception as e:
        print(f"Error training model: {e}")
        return None, None

@app.route('/process_rfm', methods=['POST'])
def process_rfm():
    global model, scaler  
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Load and process RFM data
    rfm = load_rfm_data(file_path)
    if rfm is None:
        return jsonify({"error": "Failed to process RFM data"}), 500
    
    # Assign segments to customers
    rfm = assign_segments(rfm)
    
    # Train the model
    model, scaler = train_model(rfm)
    if model is None or scaler is None:
        return jsonify({"error": "Model training failed"}), 500

    # Predict purchases
    rfm['Predicted_Purchase'] = model.predict(scaler.transform(rfm[['Recency', 'Frequency', 'Monetary']]))

    # Generate trigger actions
    rfm['Trigger_Action'] = rfm['segment'].apply(behavioral_trigger)

    response = {
        "message": "Model trained successfully",
        "segmented_customers": rfm[['segment', 'Recency', 'Frequency', 'Monetary', 'Trigger_Action']].to_dict(orient="records")
    }

    return jsonify(response)


@app.route('/predict_purchase', methods=['POST'])
def predict_purchase():
    global model, scaler
    if model is None or scaler is None:
        return jsonify({"error": "Model is not trained yet. Please process RFM data first."}), 400
    
    data = request.get_json()
    if not data or not all(k in data for k in ["Recency", "Frequency", "Monetary"]):
        return jsonify({"error": "Missing required fields: Recency, Frequency, and Monetary"}), 400
    
    try:
        input_data = np.array([[data["Recency"], data["Frequency"], data["Monetary"]]])
        input_scaled = scaler.transform(input_data)
        prediction = model.predict(input_scaled)
        return jsonify({"Predicted_Purchase": int(prediction[0])})
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500
    
@app.route('/add_customer', methods=['POST'])
def add_customer():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ["CustomerID", "Recency", "Frequency", "Monetary"]):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Add the new customer data (you can save this in a database or a list)
        # For now, we'll just return a confirmation message.
        customer_data = {
            "CustomerID": data["CustomerID"],
            "Recency": data["Recency"],
            "Frequency": data["Frequency"],
            "Monetary": data["Monetary"]
        }
        
        # You can also include any logic to save the data to a database or process it further here
        
        return jsonify({"message": "Customer added successfully", "customer_data": customer_data}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to add customer: {str(e)}"}), 500
    
@app.route('/calculate_monthly_revenue', methods=['POST'])
def calculate_monthly_revenue():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        # Load the data
        df = pd.read_excel(file_path, engine='openpyxl')
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        df['Month'] = df['InvoiceDate'].dt.to_period('M')
        
        # Calculate monthly revenue
        monthly_revenue = df.groupby(['CustomerID', 'Month'])['TotalPrice'].sum().reset_index()
        monthly_revenue.columns = ['CustomerID', 'Month', 'MonthlyRevenue']
        
        # Convert to dictionary format for response
        monthly_revenue_data = monthly_revenue.to_dict(orient="records")
        
        response = {
            "message": "Monthly revenue calculated successfully",
            "monthly_revenue": monthly_revenue_data
        }
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Error calculating monthly revenue: {e}")
        return jsonify({"error": "Failed to calculate monthly revenue"}), 500



if __name__ == '__main__':
    app.run(debug=True, port=5000)
