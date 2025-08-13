import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
import io

def load_data():
    """Load sample Titanic dataset."""
    try:
        return pd.read_csv("Titanic-Dataset.csv")
    except:
        df = sns.load_dataset('titanic')
        return df.rename(columns={
            'pclass': 'Pclass',
            'sex': 'Sex',
            'age': 'Age',
            'sibsp': 'SibSp',
            'parch': 'Parch',
            'fare': 'Fare',
            'survived': 'Survived'
        })

def preprocess_data(df):
    """Preprocess the Titanic dataset."""
    df = df.copy()
    df['Age'].fillna(df['Age'].median(), inplace=True)
    df['Fare'].fillna(df['Fare'].median(), inplace=True)
    df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
    df['IsAlone'] = (df['FamilySize'] == 1).astype(int)
    return df

def train_model(X, y):
    """Train and return a logistic regression model."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return model, accuracy, X_test, y_test, y_pred

# In ml_titanic.py, update the show_titanic_prediction function:

def show_titanic_prediction():
    """Main function to display the Titanic survival prediction interface."""
    st.title("🚢 Titanic Survival Prediction")
    st.markdown("""
    Predict the survival of Titanic passengers using machine learning.
    This model uses logistic regression to predict survival based on passenger features.
    """)
    
    # Remove or comment out the deprecated line
    # st.set_option('deprecation.showPyplotGlobalUse', False)
    
    with st.spinner("Loading data..."):
        df = load_data()
        df = preprocess_data(df)
    
    # Data visualization
    st.subheader("Data Visualization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = plt.figure(figsize=(8, 4))
        sns.countplot(data=df, x='Sex', hue='Survived')
        plt.title('Survival by Gender')
        st.pyplot(fig1, clear_figure=True)
        
        fig2 = plt.figure(figsize=(8, 4))
        sns.countplot(data=df, x='Pclass', hue='Survived')
        plt.title('Survival by Passenger Class')
        st.pyplot(fig2, clear_figure=True)
    
    with col2:
        fig3 = plt.figure(figsize=(8, 4))
        sns.histplot(data=df, x='Age', hue='Survived', element='step', kde=True)
        plt.title('Age Distribution by Survival')
        st.pyplot(fig3, clear_figure=True)
        
        fig4 = plt.figure(figsize=(8, 4))
        sns.boxplot(data=df, x='Pclass', y='Fare')
        plt.title('Fare Distribution by Passenger Class')
        st.pyplot(fig4, clear_figure=True)

    # Rest of your function remains the same...
    
    # Model training
    st.subheader("Model Training")
    feature_cols = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'FamilySize', 'IsAlone']
    X = pd.get_dummies(df[feature_cols], columns=['Sex'], drop_first=True)
    y = df['Survived']
    
    if st.button("Train Model"):
        with st.spinner("Training model..."):
            model, accuracy, X_test, y_test, y_pred = train_model(X, y)
            st.success(f"Model trained successfully! Accuracy: {accuracy:.2%}")
            
            # Confusion matrix
            st.subheader("Confusion Matrix")
            cm = confusion_matrix(y_test, y_pred)
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                       xticklabels=['Not Survived', 'Survived'],
                       yticklabels=['Not Survived', 'Survived'])
            plt.xlabel('Predicted')
            plt.ylabel('Actual')
            st.pyplot(fig)
            
            # Save model to session state
            st.session_state.titanic_model = model
            st.session_state.titanic_features = X.columns.tolist()
    
    # Prediction interface
    if 'titanic_model' in st.session_state:
        st.subheader("Make a Prediction")
        col1, col2 = st.columns(2)
        
        with col1:
            pclass = st.selectbox("Passenger Class", [1, 2, 3])
            age = st.slider("Age", 0, 100, 30)
            sex = st.radio("Sex", ["male", "female"])
            sibsp = st.slider("Number of Siblings/Spouses", 0, 8, 0)
            
        with col2:
            parch = st.slider("Number of Parents/Children", 0, 6, 0)
            fare = st.number_input("Fare", min_value=0.0, value=32.0, step=1.0)
            family_size = sibsp + parch + 1
            is_alone = 1 if family_size == 1 else 0
        
        if st.button("Predict Survival"):
            input_data = {
                'Pclass': pclass,
                'Age': age,
                'SibSp': sibsp,
                'Parch': parch,
                'Fare': fare,
                'FamilySize': family_size,
                'IsAlone': is_alone,
                'Sex_male': 1 if sex == 'male' else 0
            }
            
            model = st.session_state.titanic_model
            features = st.session_state.titanic_features
            input_df = pd.DataFrame([input_data])
            
            for col in features:
                if col not in input_df.columns:
                    input_df[col] = 0
            
            input_df = input_df[features]
            prediction = model.predict(input_df)[0]
            probability = model.predict_proba(input_df)[0][1]
            
            if prediction == 1:
                st.success(f"🎉 Predicted to Survive! (Confidence: {probability:.2%})")
                st.balloons()
            else:
                st.error(f"❌ Predicted to Not Survive (Survival Chance: {probability:.2%})")

if __name__ == "__main__":
    show_titanic_prediction()