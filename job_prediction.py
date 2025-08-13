import streamlit as st
import pandas as pd
import base64
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

def set_background_image(image_file):
    """Set background image for the app."""
    try:
        with open(image_file, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            h1 {{
                color: #FFFFFF;
                text-shadow: 2px 2px #000000;
            }}
            h3 {{
                color: #FFFFFF;
                text-shadow: 1px 1px #000000;
            }}
            label {{
                color: #FFFFFF !important;
            }}
            .stButton > button {{
                color: #FFFFFF;
                background-color: #4CAF50;
            }}
            .stTextInput input {{
                color: #000000;
                background-color: #FFFFFF;
            }}
            .stNumberInput input {{
                color: #000000;
                background-color: #FFFFFF;
            }}
            .stSelectbox div[data-baseweb="select"] {{
                color: #000000;
                background-color: #FFFFFF;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.warning(f"Could not load background image: {e}")

def load_and_prepare_data(file_path):
    """Load and prepare the dataset for training."""
    try:
        data = pd.read_csv(file_path)
        
        # Initialize label encoders
        le_qualification = LabelEncoder()
        le_internship = LabelEncoder()
        le_referral = LabelEncoder()
        le_result = LabelEncoder()
        
        # Encode categorical columns
        data["Qualification"] = le_qualification.fit_transform(data["Qualification"])
        data["Internship"] = le_internship.fit_transform(data["Internship"])
        data["Referral"] = le_referral.fit_transform(data["Referral"])
        data["Job_Result"] = le_result.fit_transform(data["Job_Result"])
        
        # Prepare features and target
        x = data[[
            "Qualification", "Internship", "Comm_Skill", "Tech_Skill_Level",
            "Certifications", "Interview_Score", "Resume_Score", "Referral"
        ]]
        y = data["Job_Result"]
        
        return {
            'data': data,
            'x': x,
            'y': y,
            'encoders': {
                'qualification': le_qualification,
                'internship': le_internship,
                'referral': le_referral,
                'result': le_result
            }
        }
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def train_model(x, y):
    """Train the linear regression model."""
    try:
        model = LinearRegression()
        model.fit(x, y)
        return model
    except Exception as e:
        st.error(f"Error training model: {e}")
        return None

def show_job_prediction():
    """Show the job prediction interface."""
    # Set background image
    set_background_image("background.jpg")
    
    st.title("Job Selection Prediction")
    
    # Load data
    data = load_and_prepare_data("dataset.csv")
    if data is None:
        return
    
    # Train model
    model = train_model(data['x'], data['y'])
    if model is None:
        return
    
    # Get encoders
    le_qualification = data['encoders']['qualification']
    le_internship = data['encoders']['internship']
    le_referral = data['encoders']['referral']
    le_result = data['encoders']['result']
    
    # Input form
    st.write("### Enter Candidate Information:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        qualification = st.selectbox(
            "Qualification",
            le_qualification.classes_.tolist()
        )
        internship = st.selectbox(
            "Internship",
            le_internship.classes_.tolist()
        )
        referral = st.selectbox(
            "Referral",
            le_referral.classes_.tolist()
        )
        comm_skill = st.number_input(
            "Communication Skill (0-10)",
            min_value=0, max_value=10, value=5
        )
    
    with col2:
        tech_skill = st.number_input(
            "Technical Skill Level (0-10)",
            min_value=0, max_value=10, value=5
        )
        certifications = st.number_input(
            "Number of Certifications",
            min_value=0, value=0
        )
        interview_score = st.number_input(
            "Interview Score (0-100)",
            min_value=0, max_value=100, value=50
        )
        resume_score = st.number_input(
            "Resume Score (0-100)",
            min_value=0, max_value=100, value=50
        )
    
    if st.button("Predict Job Result", type="primary"):
        try:
            # Prepare input data
            input_data = [[
                le_qualification.transform([qualification])[0],
                le_internship.transform([internship])[0],
                comm_skill,
                tech_skill,
                certifications,
                interview_score,
                resume_score,
                le_referral.transform([referral])[0],
            ]]
            
            # Make prediction
            prediction = model.predict(input_data)[0]
            result_label = le_result.inverse_transform([int(round(prediction))])[0]
            
            # Display result
            st.markdown("### Prediction Result")
            if "Not Selected" in result_label:
                st.error(f"Predicted Job Result: {result_label} ❌")
                st.write("The candidate may need to improve in certain areas to increase their chances.")
            elif "Selected" in result_label:
                st.success(f"Predicted Job Result: {result_label} ✅")
                st.write("The candidate has a strong profile for the position!")
            else:
                st.info(f"Predicted Job Result: {result_label}")
                
            # Show feature importance
            st.markdown("### Feature Importance")
            feature_importance = pd.DataFrame({
                'Feature': data['x'].columns,
                'Coefficient': model.coef_
            }).sort_values('Coefficient', ascending=False)
            
            st.bar_chart(feature_importance.set_index('Feature'))
            
        except Exception as e:
            st.error(f"Error making prediction: {e}")
    
    # Add some space at the bottom
    st.markdown("<br><br>", unsafe_allow_html=True)
