import joblib
import pandas as pd
import algorithms.variance_algorithm as ewma
import numpy as np
from algorithms.custom_mse_function import custom_asymmetric_train

"""
This class is used to predict whether a given mouse movement is real or fake.
@input: Mouse movement data using MACT format
@output: Either Fake or Real
"""

# Function to process the input data (similar to calculate_params)
def process_input(input_data):
    # Process the input_data using calculate_params or similar function
    # This should match the format used during training
    processed_data = ewma.calculate_params(input_data)
    return pd.DataFrame([processed_data])

# Load the saved model
model_filename = 'samples/lightgbm_boostingtree_custom.joblib'
clf = joblib.load(model_filename)

# take input from user
input_data = input("Enter the data: ")

# Process the input and make a prediction
processed_input = process_input(input_data)
prediction = clf.predict(processed_input)

print("Model's prediction:", prediction)
# Output the prediction (1 or 0)
if prediction[0] > 0.5:
    print("This is a Fake Mouse Movement From That Old MACT!")
else:
    print("This is a Real Mouse Movement")
