const express = require("express");
const axios = require("axios");
const cors = require("cors");
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 5000;
const ML_SERVICE_URL = process.env.ML_SERVICE_URL || "http://localhost:5001";

app.use(express.json());
app.use(cors());

// ✅ Endpoint to process RFM segmentation and return model training status + customer segmentation data
app.post("/api/process_rfm", async (req, res) => {
	try {
		const response = await axios.post(
			`${ML_SERVICE_URL}/process_rfm`,
			req.body
		);

		// ✅ Extract necessary data from the response
		const { message, segmented_customers, triggers } = response.data;

		res.json({
			message: message || "Model trained successfully",
			segmented_customers: segmented_customers || [],
			triggers: triggers || [],
		});
	} catch (error) {
		console.error("Error processing RFM segmentation:", error.message);
		res.status(500).json({ error: "Failed to process RFM segmentation" });
	}
});

// ✅ Endpoint to predict customer purchase
app.post("/api/predict_purchase", async (req, res) => {
	try {
		const response = await axios.post(
			`${ML_SERVICE_URL}/predict_purchase`,
			req.body
		);
		res.json(response.data);
	} catch (error) {
		console.error("Error predicting purchase:", error.message);
		res.status(500).json({ error: "Failed to predict purchase" });
	}
});

// ✅ Endpoint to add a new customer and return behavioral trigger
app.post("/api/add_customer", async (req, res) => {
	try {
		const response = await axios.post(
			`${ML_SERVICE_URL}/add_customer`,
			req.body
		);
		res.json(response.data);
	} catch (error) {
		console.error("Error adding customer:", error.message);
		res.status(500).json({ error: "Failed to add customer" });
	}
});

// ✅ Endpoint to calculate monthly revenue
app.post("/api/calculate_monthly_revenue", async (req, res) => {
	try {
		const response = await axios.post(
			`${ML_SERVICE_URL}/calculate_monthly_revenue`,
			req.body
		);
		res.json(response.data);
	} catch (error) {
		console.error("Error calculating monthly revenue:", error.message);
		res.status(500).json({ error: "Failed to calculate monthly revenue" });
	}
});

app.listen(PORT, () => {
	console.log(`Node.js backend running on port ${PORT}`);
});
