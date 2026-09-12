import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title(" Superkart Sales Prediction")

# Section for online prediction
st.subheader("Online Prediction")

# Collect user input for property features
Product_Weight =  st.number_input("ProductWeight", min_value=1, step=1, value=1)
Product_Allocated_Area = st.number_input("Product Allocated Area", min_value=0.001, value=0.001)
Product_MRP = st.number_input("ProductMRP", min_value=1, step=1, value=1)
Store_Age_Years  = st.number_input("Store_Age_Years", min_value=1, step=1, value=1)
Product_Id_char = st.selectbox("Product_Id_char ", ["FD", "NC" ,"DR"])
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular" ,"No Sugar"])
Product_Type_Category = st.selectbox("Product_Type_Category", ["Perishable", "Non Perishable"])
Store_Size = st.selectbox("StoreSize", ["High", "Medium","Small" ])
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2","Tier 3" ])
Store_Type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2","Supermarket Type3" ,"Foodmart" ,"Departmental"])

# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    'Product_Weight': Product_Weight,
    'Product_Allocated_Area': Product_Allocated_Area,
    'Product_MRP': Product_MRP,
    'Store_Age_Years': Store_Age_Years,
    'Product_Id_char': Product_Id_char,
    'Product_Sugar_Content': Product_Sugar_Content,
    'Product_Type_Category': Product_Type_Category,
    'Store_Size': Store_Size,
    'Store_Location_City_Type': Store_Location_City_Type,
    'Store_Type': Store_Type
}])

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/superkartsales", json=input_data.to_dict(orient='records')[0])  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Predicted Price (in dollars)']
        st.success(f"Predicted Superkart sales (in dollars): {prediction}")
    else:
        st.error("Unable to connect to the prediction API.")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/superkartsalesbatch", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")
