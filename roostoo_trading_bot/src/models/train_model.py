import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
import joblib

def train_and_save_model(data_path, model_path):
    """
    Train a Random Forest model and save it to disk.

    Args:
        data_path (str): Path to the historical data CSV file.
        model_path (str): Path to save the trained model.
    """
    # Load historical data
    data = pd.read_csv(data_path)

    # Ensure the required features and target column are present
    required_features = ['RSI', 'SMA_20', 'MACD_12_26_9', 'MACDs_12_26_9', 'MACDh_12_26_9']
    if not all(feature in data.columns for feature in required_features):
        raise ValueError(f"Historical data must contain the following columns: {required_features}")

    # Features and target
    X = data[required_features]
    y = data['target']  # Target: 1 for Buy, 0 for Sell

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Hyperparameter tuning using GridSearchCV
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }

    model = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, scoring='accuracy')
    grid_search.fit(X_train, y_train)

    # Best model from grid search
    best_model = grid_search.best_estimator_

    # Evaluate the model
    y_pred = best_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # Save the model
    joblib.dump(best_model, model_path)
    print(f"Model saved to {model_path}")

# Example usage
if __name__ == "__main__":
    data_path = "data/historical/market_data_with_indicators.csv"  # Path to historical data
    model_path = "data/models/random_forest_model.pkl"  # Path to save the model
    train_and_save_model(data_path, model_path)