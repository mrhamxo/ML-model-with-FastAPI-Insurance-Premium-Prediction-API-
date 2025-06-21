# ML-model-with-FastAPI
A production-ready AI-based FastAPI project that predicts **insurance premium categories** based on lifestyle and personal data such as age, BMI, smoking habits, income, city, and occupation. It also includes a complete patient management system with full CRUD functionality and a Streamlit-based web frontend for interaction.

## 🚀 Features

### ✅ Insurance Premium Predictor API
- Built with **FastAPI**
- Predicts insurance category based on:
  - Age group
  - BMI (auto-computed)
  - Lifestyle risk (smoking + obesity)
  - Income
  - City tier (1, 2, 3)
  - Occupation
- City tier logic is defined using major Pakistani cities

### 🧑‍⚕️ Patient Management API
- Complete RESTful API with:
  - `POST /create`
  - `GET /view`, `GET /patient/{id}`
  - `PUT /edit/{id}`
  - `DELETE /delete/{id}`
  - `GET /sort?sort_by=bmi&order=asc`
- Automatically calculates BMI and verdict category (Underweight, Normal, Overweight, Obese)
- Data persisted in `patients.json` as local database

### 🌐 Frontend (Streamlit UI)
- Collects user data in a user-friendly form
- Sends POST request to FastAPI backend
- Displays:
  - Predicted insurance category
  - (Optional) Confidence and class probabilities
- Fully interactive and responsive UI

## 🔧 Tech Stack

| Component     | Technology        |
|---------------|------------------|
| Backend API   | FastAPI           |
| Frontend      | Streamlit         |
| Model         | scikit-learn, pandas |
| Deployment    | Uvicorn (for API) |
| Storage       | JSON File DB      |

## 📊 ML Model Summary

- Preprocessed using `OneHotEncoder`, standard feature engineering
- Trained using a classification algorithm (e.g., RandomForest / LogisticRegression)
- Model saved as `model.pkl`
- Training process included in `insurance_premium_ml.ipynb`

## ⚙️ How to Run

### 1. Clone the Repo
```bash
git clone https://github.com/your-username/insurance-premium-predictor.git
cd insurance-premium-predictor
````

### 2. Create & Activate Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run FastAPI Backend

```bash
uvicorn app:app --reload
```

### 4. Run Streamlit Frontend

```bash
streamlit run frontend.py
```

### 5. Test CRUD API

```bash
uvicorn main:app --reload
```

## 📬 API Endpoints

### 🎯 Insurance Premium Prediction

```
POST /predict
```

**Request Body:**

```json
{
  "age": 35,
  "weight": 70,
  "height": 1.75,
  "income_lpa": 10,
  "smoker": true,
  "city": "Lahore",
  "occupation": "private_job"
}
```

**Response:**

```json
{
  "predicted_category": "high"
}
```

### 🧑 Patient Management Routes

| Method | Route                         | Description               |
| ------ | ----------------------------- | ------------------------- |
| GET    | `/view`                       | View all patients         |
| GET    | `/patient/{id}`               | View specific patient     |
| POST   | `/create`                     | Add new patient           |
| PUT    | `/edit/{id}`                  | Update patient            |
| DELETE | `/delete/{id}`                | Delete patient            |
| GET    | `/sort?sort_by=bmi&order=asc` | Sort by height/weight/BMI |

## 📸 Screenshots

Web UI (Streamlit)             
![Image](https://github.com/user-attachments/assets/ce2093dd-0110-45c8-9616-f913a8415bd8)

## 💬 Questions?

Feel free to contact me via GitHub issues or [LinkedIn](https://www.linkedin.com/in/muhammad-hamza-khattak/)
