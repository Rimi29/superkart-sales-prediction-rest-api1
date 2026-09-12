# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
superkart_sales_predictor_api = Flask("Superkart Total Sales Predictor")

# Load the trained machine learning model
model = joblib.load("superkart_total_sales_prediction_model_v2_0.joblib")

# Define a route for the home page (GET request)
@superkart_sales_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the Superkart Total Sales Prediction API!"

# Define an endpoint for single store sales  prediction (POST request)
@superkart_sales_predictor_api.post('/v1/superkartsales')
def predict_superkart_sales():
    """
    This function handles POST requests to the '/v1/superkartsales' endpoint.
    It expects a JSON payload containing property details and returns
    the predicted rental price as a JSON response.
    """
    # Get the JSON data from the request body
    sales_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Product_Weight': sales_data['Product_Weight'],
        'Product_Allocated_Area': sales_data['Product_Allocated_Area'],
        'Product_MRP': sales_data['Product_MRP'],
        'Store_Age_Years': sales_data['Store_Age_Years'],
        'Product_Id_char': sales_data['Product_Id_char'],
        'Product_Sugar_Content': sales_data['Product_Sugar_Content'],
        'Product_Type_Category': sales_data['Product_Type_Category'],
        'Store_Size': sales_data['Store_Size'],
        'Store_Location_City_Type': sales_data['Store_Location_City_Type'],
        'Store_Type': sales_data['Store_Type']



    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction (get total sales)
    predicted_total_sales = model.predict(input_data)[0]


    # Return the actual price
    return jsonify({'Predicted Price (in dollars)': predicted_total_sales})


# Define an endpoint for batch prediction (POST request)
@superkart_sales_predictor_api.post('/v1/superkartsalesbatch')
def predict_superkart_sales_batch():
    """
    This function handles POST requests to the '/v1/superkartsalesbatch' endpoint.
    It expects a CSV file containing property details for multiple properties
    and returns the predicted rental prices as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all properties in the DataFrame (get log_prices)
    predicted_sales_prices = model.predict(input_data).tolist()
    input_data['predicted_sales_prices'] = predicted_sales_prices
    
    # Return the predictions dictionary as a JSON response
    return input_data.to_json(orient='records')


# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    rental_price_predictor_api.run(debug=True)
