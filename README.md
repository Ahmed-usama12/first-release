# First Release 🚀

This repository contains a full-stack application for cleaning CSV files using a **React frontend, an Express backend, and a Flask-based ML service**.

## 📂 Folder Structure

First Release 🚀

This repository contains a full-stack application for cleaning CSV files using a React frontend, an Express backend, and a Flask-based ML service.

📂 Folder Structure

first-release/
│── ml/          # Machine Learning Service (Flask)
│── backend/     # Backend Service (Express.js)
│── frontend/    # Frontend UI (React.js)
│── README.md    # Project Documentation
│── .gitignore   # Ignored files and dependencies

⚙️ Prerequisites

Make sure you have the following installed on your machine:

Node.js (v16 or later)

npm (or Yarn)  (Recommended)

Python 3.8+

Git

🛠️ Setup Instructions

1️⃣ Clone the Repository

git clone https://github.com/YOUR_USERNAME/first-release.git
cd first-release

2️⃣ Backend Setup (Express.js)

Navigate to the backend folder:

cd backend

Install dependencies:

# Using npm
npm install

# Or using Yarn (if preferred)
yarn install


Start the backend server:

# Using npm
npm start

# Or using Yarn (if preferred)
yarn start


The backend will be running on http://localhost:5001/.

3️⃣ Machine Learning Service Setup (Flask)

Navigate to the ML folder:

cd ../ml

Create a virtual environment:

python -m venv venv
source venv/bin/activate  # For Mac/Linux
venv\Scripts\activate     # For Windows

Install dependencies:

pip install -r requirements.txt

Start the Flask ML API:

python app.py

The ML service will be running on http://localhost:5000/.

4️⃣ Frontend Setup (React.js)

Navigate to the frontend folder:

cd ../frontend

Install dependencies:

# Using npm
npm install

# Or using Yarn (if preferred)
yarn install


Start the frontend:

# Using npm
npm start

# Or using Yarn (if preferred)
yarn start


The frontend will be available on http://localhost:3000/.

🔄 API Endpoints

Backend API (http://localhost:5001/)

Method

Endpoint

Description

POST

/clean_csv

Upload CSV file for cleaning

ML Service API (http://localhost:5000/)

Method

Endpoint

Description

POST

/clean_csv

Cleans the uploaded CSV file

📈 Git Branch Rules

main (Protected): Only the repository owner can push or merge.

first-release (Protected): Only the repository owner can push or pull.

Feature branches: Developers should create feature branches (feature-branch-name) and open pull requests for review.

To Create a Feature Branch:

git checkout -b feature-branch-name
git push origin feature-branch-name

📄 Contribution Guidelines

Fork the repository.

Create a feature branch (feature-branch-name).

Commit your changes:

git commit -m "Added new feature"

Push your branch:

git push origin feature-branch-name

Open a Pull Request to first-release.

🔥 Troubleshooting

Common Issues & Fixes

Issue

Solution

Port already in use

Kill the process: npx kill-port 5000 5001

Module not found (Node.js)

Run yarn install or npm start again

Virtual env issues (Python)

Run source venv/bin/activate or venv\Scripts\activate

🏆 License

This project is licensed under the MIT License.

🚀 Happy Coding! Let me know if you need any changes! 😃

