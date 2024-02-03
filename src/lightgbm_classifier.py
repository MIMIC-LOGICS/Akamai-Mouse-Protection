
import lightgbm 
import numpy as np
import pandas as pd
import algorithms.variance_algorithm as ewma
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import numpy as np
from sklearn.metrics import confusion_matrix
from algorithms.custom_mse_function import custom_asymmetric_train

def load_data(real_path, fake_path):
    """
    Load the fake and real data, in mact format, from the files and combines them into a single dataframe.
    @param real_path: The path to the file containing the real data
    @param fake_path: The path to the file containing the fake data
    @return: A tuple containing the data and the labels
    """
    # Process each file
    real_data_df = process_file(real_path, 0)
    fake_data_df = process_file(fake_path, 1)

    # Combine the real and fake data
    combined_df = pd.concat([real_data_df, fake_data_df], ignore_index=True)

    # Some values from calculate_params returnes np.inf, I replace them with np.nan and then drop all the nan3
    combined_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    combined_df.dropna(inplace=True)

    assert np.all(np.isfinite(combined_df)), "Data contains non-finite values."

    X = combined_df.drop('Label', axis=1)  # Data without the label
    y = combined_df['Label']

    return X, y

def process_file(file_path, label):
    """
    Extracts the features from the file and returns a dataframe containing the features and the label.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
        data = [ewma.calculate_params(line) for line in lines if ewma.calculate_params(line) is not None and ewma.calculate_params(line).size > 0]
        df = pd.DataFrame(data)
        df['Label'] = label  # Add a column for the label
        return df
    
def build_gbm(X_train, X_valid, y_train, y_valid, objective=custom_asymmetric_train):
    """
    @param X_train: The training data
    @param X_valid: The validation data
    @param y_train: The training labels
    @param y_valid: The validation labels

    @return: A trained lightgbm model
    """
    gbm = lightgbm.LGBMClassifier() 

    # updating objective function to custom
    gbm.set_params(**{'objective': objective})

    # fitting model 
    gbm.fit(
        X_train,
        y_train,
        eval_set=[(X_valid, y_valid)],
    )

    return gbm

def calculate_accuracy(y_valid, y_pred):
    """
    Calculate the accuracy of the model and print the confusion matrix.
    @param y_valid: The validation labels
    @param y_pred: The predicted labels
    """
    
    accuracy = accuracy_score(y_valid, y_pred.round())

    print("Accuracy: %.2f%%" % (accuracy * 100.0))

    #compute confusion matrix and save the model
    y_pred_binary = np.where(y_pred >= 0.5, 1, 0)

    # Compute confusion matrix

    conf_matrix = confusion_matrix(y_valid, y_pred_binary)

    print(conf_matrix)

def main():
    X,y = load_data('samples/real_10k.txt', 'samples/fake_10k.txt')

    # Split the data into training and testing sets
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.3, random_state=42)

    # Train the model with custom MSE

    gbm = build_gbm(X_train, X_valid, y_train, y_valid)

    y_pred = gbm.predict(X_valid)

    calculate_accuracy(y_valid, y_pred)

    model_filename = 'samples/lightgbm_boostingtree_custom.joblib'
    joblib.dump(gbm, model_filename)

    # Train the model without custom MSE
    gbm2 = build_gbm(X_train, X_valid, y_train, y_valid, objective='binary')
                    
    y_pred = gbm2.predict(X_valid)

    calculate_accuracy(y_valid, y_pred)

    # Save the model
    model_filename = 'samples/lightgbm_boostingtree.joblib'
    joblib.dump(gbm, model_filename)

if __name__ == "__main__":
    main()