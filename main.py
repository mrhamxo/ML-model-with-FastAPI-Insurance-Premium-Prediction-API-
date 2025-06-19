from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json
 
app = FastAPI()

# -------------------- Data Model --------------------

class Patient(BaseModel):
    # Basic patient fields with validation
    id: Annotated[str, Field(..., description='ID of the Patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the Patient')]
    city: Annotated[str, Field(..., description='City of Patient')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the Patient')]
    gender: Annotated[Literal['male', 'female', 'other'], Field(..., description='Gender of the Patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the Patient in meters')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the Patient in kgs')]
    
    # BMI computed from height and weight
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi
    
    # Health verdict based on BMI value
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'
        
# Partial model for updating patient fields
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120)]
    gender: Annotated[Optional[Literal['male', 'female', 'other']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]
        
# -------------------- Utility Functions --------------------

# Load patient data from JSON file
def load_data():
    with open("patients.json", "r") as file:
        data = json.load(file)
    return data

# Save patient data back to JSON file
def save_data(data):
    with open("patients.json", "w") as file:
        json.dump(data, file)

# -------------------- API Endpoints --------------------

@app.get("/")
def hello():
    # Welcome/root endpoint
    return {'message: Patient Management System API'}

@app.get("/about")
def about():
    # About endpoint
    return {'message: This is fully functional API to manage patients.'}

@app.get("/view")
def view():
    # View all patient data
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description='ID of the patient in DB', example='P001')):
    # Get a single patient's data by ID
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code=404, detail = "patient data not found")

@app.get("/sort")
def sort_patient(sort_by : str = Query(..., description='sort on the basis of height, weight or BMI'), 
                 order: str = Query('asc', description='sort in asc or desc order')):
    # Sort patient data by a given field and order
    valid_fields = ['height', 'weight', 'bmi']
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail='Invalid field select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')

    data = load_data()
    
    sort_order = True if order == 'desc' else False

    # Sort using the given field
    sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse = sort_order)
    
    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    # Create a new patient record
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')
    
    # Add patient to data store (excluding ID from body)
    data[patient.id] = patient.model_dump(exclude=['id'])

    # Save updated data
    save_data(data)
    
    return JSONResponse(status_code=201, content={'message' : 'Patient Data Created Successful'})

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    # Update an existing patient's info
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient data not found')
    
    # Get existing record and apply updates
    existing_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    # Recalculate BMI/verdict using full model validation
    existing_patient_info['id'] = patient_id
    patient_pydandic_obj = Patient(**existing_patient_info)

    # Convert back to dict
    existing_patient_info = patient_pydandic_obj.model_dump(exclude='id')

    # Save updated info
    data[patient_id] = existing_patient_info
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'Patient Data Updated'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    # Delete a patient by ID
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient Data not found')
    
    del data[patient_id]
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient deleted'})
