import pandas as pd
import algorithms.variance_algorithm as ewma
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import numpy as np
from lightgbm_classifier import load_data, process_file, calculate_accuracy

def main():
    real_data_file = 'samples/real_10k.txt'
    fake_data_file = 'samples/fake_10k.txt'

    X,y = load_data(real_data_file, fake_data_file)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train the Random Forest classifier
    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)

    # Make predictions on the test set
    predictions = clf.predict(X_test)

    calculate_accuracy(y_test, predictions)

    model_filename = 'samples/random_forest_model.joblib'
    joblib.dump(clf, model_filename)

if __name__ == '__main__':
    main()