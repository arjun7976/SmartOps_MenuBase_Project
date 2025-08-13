import streamlit as st
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from pathlib import Path

def train_salary_model(data_path='data1.csv', model_path='salary_pass_model.pkl'):
    """
    Train and save the salary prediction model if it doesn't exist.
    
    Args:
        data_path (str): Path to the training data CSV file
        model_path (str): Path to save/load the trained model
        
    Returns:
        bool: True if model was loaded or trained successfully, False otherwise
    """
    try:
        # Try to load existing model first
        if Path(model_path).exists():
            return True
            
        # If no model exists, train a new one
        st.info("Training salary prediction model...")
        
        # Load and prepare data
        data = pd.read_csv(data_path)
        data['Pass'] = (data['Salary'] > 50000).astype(int)
        
        # Train model
        X = data[['Experience']]
        y = data['Pass']
        
        model = LogisticRegression()
        model.fit(X, y)
        
        # Save model
        joblib.dump(model, model_path)
        return True
        
    except Exception as e:
        st.error(f"❌ Error training salary prediction model: {e}")
        return False

def show_salary_prediction():
    """Show the salary pass/fail prediction interface."""
    st.title("💰 Salary Pass/Fail Prediction")
    st.markdown("""
    This model predicts whether a person's salary is likely to be above or below $50,000 
    based on their years of experience.
    """)
    
    # Try to load or train the model
    model_loaded = train_salary_model()
    
    if not model_loaded:
        st.error("❌ Could not load or train the salary prediction model.")
        return
    
    try:
        # Load the model
        model = joblib.load('salary_pass_model.pkl')
        
        # Input form
        st.markdown("### Enter Candidate's Experience")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            experience = st.number_input(
                "Years of Experience",
                min_value=0.0, 
                max_value=50.0, 
                step=0.1,
                value=5.0,
                format="%.1f"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            predict_btn = st.button("Predict", type="primary")
        
        # Make prediction when button is clicked
        if predict_btn:
            with st.spinner('Predicting...'):
                try:
                    # Make prediction
                    prediction = model.predict([[experience]])[0]
                    probability = model.predict_proba([[experience]])[0][1]
                    
                    # Display result
                    st.markdown("### Prediction Result")
                    
                    if prediction == 1:
                        st.success(
                            f"✅ **PASS** - {probability*100:.1f}% confident "
                            f"the salary is above $50,000"
                        )
                        st.balloons()
                    else:
                        st.error(
                            f"❌ **FAIL** - {(1-probability)*100:.1f}% confident "
                            f"the salary is below $50,000"
                        )
                    
                    # Show some additional insights
                    st.markdown("### Insights")
                    if prediction == 1:
                        if experience < 5:
                            st.info("👔 Even with limited experience, the model predicts a salary above $50,000. "
                                  "This could be due to high demand skills or advanced education.")
                        else:
                            st.info("📈 With this level of experience, it's common to see salaries above $50,000.")
                    else:
                        if experience > 3:
                            st.info("💡 Consider additional training or certifications to increase your earning potential.")
                        else:
                            st.info("🌱 Early in your career. Gaining more experience will help increase your salary potential.")
                    
                    # Show the decision boundary
                    st.markdown("### How the Model Decides")
                    decision_boundary = model.intercept_[0] / (-model.coef_[0][0])
                    st.write(f"The model predicts a salary above $50,000 for experience greater than "
                            f"**{decision_boundary:.1f} years**.")
                    
                except Exception as e:
                    st.error(f"❌ Error making prediction: {e}")
        
        # Add some space at the bottom
        st.markdown("<br><br>", unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"❌ Error loading salary prediction model: {e}")
        st.info("Please make sure the model file exists and is in the correct format.")

# For testing the module directly
if __name__ == "__main__":
    show_salary_prediction()
