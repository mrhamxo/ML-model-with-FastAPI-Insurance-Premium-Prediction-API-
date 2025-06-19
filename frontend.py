import streamlit as st
import requests

# -------------------- API Endpoint --------------------
API_URL = "http://127.0.0.1:8000/predict"

# -------------------- Page Configuration --------------------
st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="💰",
    layout="centered"
)

# -------------------- Title & Instructions --------------------
st.title("💼 Insurance Premium Prediction")
st.markdown(
    """
    🚀 **Predict your insurance premium category** based on personal and lifestyle factors.  
    Fill out the details below and click **Predict** to get your premium class.
    """
)

# -------------------- Input Form --------------------
with st.form("insurance_form"):
    st.subheader("👤 Personal Information")

    # Organize into two columns
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=1, max_value=119, value=30)
        weight = st.number_input("Weight (kg)", min_value=1.0, value=65.0)
        income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=10.0)
        smoker = st.selectbox("Are you a smoker?", options=[False, True])

    with col2:
        height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.7)
        city = st.text_input("City", value="Karachi")
        occupation = st.selectbox(
            "Occupation",
            ['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job']
        )

    # Submit button for form
    submitted = st.form_submit_button("🔍 Predict Premium Category")

# -------------------- API Request Logic --------------------
if submitted:
    # Pack inputs into JSON
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    with st.spinner("⏳ Predicting your insurance premium category..."):
        try:
            response = requests.post(API_URL, json=input_data)
            result = response.json()

            if response.status_code == 200:
                # Support both direct or nested prediction formats
                if "predicted_category" in result:
                    prediction = result["predicted_category"]
                    st.success(f"✅ **Predicted Insurance Premium Category:** {prediction}")

                elif "response" in result and isinstance(result["response"], dict):
                    prediction = result["response"]
                    st.success(f"✅ **Predicted Insurance Premium Category:** {prediction['predicted_category']}")
                    
                    # Show advanced details if available
                    if "confidence" in prediction:
                        st.metric("🔒 Confidence", f"{prediction['confidence']*100:.2f}%")
                    if "class_probabilities" in prediction:
                        st.subheader("📊 Class Probabilities")
                        st.json(prediction["class_probabilities"])

                else:
                    st.warning("⚠️ Unexpected response format:")
                    st.json(result)

            else:
                st.error(f"❌ API Error ({response.status_code})")
                st.json(result)

        except requests.exceptions.ConnectionError:
            st.error("🚫 Could not connect to FastAPI server. Please ensure it is running.")

# -------------------- Footer --------------------
st.markdown("---")
st.caption("Made with ❤️ using FastAPI & Streamlit")
