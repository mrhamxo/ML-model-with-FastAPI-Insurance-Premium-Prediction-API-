from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import pandas as pd
import pickle

# -------------------- Load ML Model --------------------

# Load the trained model from file using binary mode
with open('annually_insurance_premium_using_ml\\model.pkl', 'rb') as f:
    model = pickle.load(f)
    
# Create FastAPI instance
app = FastAPI()

# -------------------- Define City Tiers --------------------

# Tier 1 cities (metro)
tier_1_cities = ['Islamabad', 'Karachi', 'Lahore', 'Peshawar', 'Quetta', 'Rawalpindi', 'Faisalabad']

# Tier 2 cities (developed but smaller than Tier 1)
tier_2_cities = [
    'Multan', 'Gujranwala', 'Hyderabad', 'Sialkot', 'Bahawalpur', 'Sargodha', 'Sukkur', 'Larkana', 'Sheikhupura',
    'Abbottabad', 'Jhelum', 'Gujrat', 'Mardan', 'Kasur', 'Okara', 'Sahiwal', 'Turbat', 'Mingora', 'Nawabshah', 
    'Chiniot', 'Kohat', 'Muzaffarabad', 'Gilgit', 'Kotli', 'Skardu', 'Khuzdar', 'Bannu', 'Gwadar', 'Jhang', 'Hafizabad',
    'Kamoke', 'Jacobabad', 'Shikarpur', 'Charsadda', 'Mansehra', 'Narowal', 'Vehari', 'Layyah', 'Attock', 'Lodhran',
    'Badin', 'Khanewal', 'Bhakkar', 'Haripur', 'Swabi', 'Jamshoro', 'Gojra', 'Chakwal', 'Jaranwala', 'Khanpur', 'Kamalia',
    'Daska', 'Nowshera', 'Thatta', 'Pakpattan', 'Jaccobabad', 'Samundri', 'Muridke', 'Mianwali', 'Kandhkot', 'Shahdadpur', 
    'Shahkot', 'Arifwala', 'Pattoki', 'Shikarpur', 'Hangu', 'Charsadda', 'Burewala', 'Jatoi',
]

# -------------------- Pydantic Input Model --------------------

class UserInput(BaseModel):
    # Basic user input fields with validation
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the user')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the user')]
    height: Annotated[float, Field(..., gt=0, lt=2.5, description='Height of the user')]
    income_lpa: Annotated[float, Field(..., gt=0, description='Annual salary of the user in lpa')]
    smoker: Annotated[bool, Field(..., description='Is user a smoker')]
    city: Annotated[str, Field(..., description='The user belongs to which city')]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(..., description='Occupation of the user')]

    # Computed BMI based on height and weight
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = self.weight / (self.height ** 2)
        return bmi

    # Determine lifestyle risk based on smoking status and BMI
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"

    # Categorize user by age group
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        else:
            return "senior"

    # Map city to its tier
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3

# -------------------- Prediction Endpoint --------------------

@app.post("/predict")
def predict_premium(data: UserInput):
    # Construct DataFrame with engineered features
    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'city': data.city,
        'occupation': data.occupation 
    }])
    
    # Make prediction using the ML model
    prediction = model.predict(input_df)[0]
    
    # Return prediction as JSON response
    return JSONResponse(status_code=200, content={'predicted_category': prediction})
