import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

class MonographModels:
    def __init__(self, train_size=0.8):
        self.train_size = train_size
        self.model = None
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        self.y_pred = None
        self.mse = None
        self.mae = None

    def set_data(self, X, y):
        """Set the input data for the model."""
        X_train, X_test, y_train, y_test = self.split_data(X, y)
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

    def split_data(self, X, y):
        """Split the data into training and testing sets."""
        n_train = int(len(X) * self.train_size)
        X_train, X_test = X[:n_train], X[n_train:]
        y_train, y_test = y[:n_train], y[n_train:]
        return X_train, X_test, y_train, y_test

    def train(self):
        """Train the model."""
        self.model.fit(self.X_train, self.y_train)
        self.y_pred = self.model.predict(self.X_test)
        self.mse = np.mean((self.y_pred - self.y_test) ** 2)
        self.mae = np.mean(np.abs(self.y_pred - self.y_test))

    def plot_comparison(self):
        """Generate plots to compare actual vs predicted values."""
        plt.figure(figsize=(12, 6))
        plt.plot(self.y_test, label='Actual')
        plt.plot(self.y_pred, label='Predicted')
        plt.xlabel('Index')
        plt.ylabel('Value')
        plt.legend()
        plt.title('Actual vs Predicted Values')
        plt.show()