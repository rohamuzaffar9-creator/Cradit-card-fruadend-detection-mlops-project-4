import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import mlflow
import mlflow.sklearn

# Load data
df = pd.read_csv("data/creditcard.csv")

X = df.drop("Class", axis=1)
y = df["Class"]

print("Shape:", X.shape)
print("Fraud Cases:", sum(y == 1))
print("Legit Cases:", sum(y == 0))

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y   # IMPORTANT for imbalance
)

mlflow.set_experiment("Fraud_Detection")

with mlflow.start_run():

    model = RandomForestClassifier(
        n_estimators=20,   # FAST (important fix)
        n_jobs=2,          # CPU optimization
        random_state=42
    )

    print("Training started...")

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = model.score(X_test, y_test)

    print(classification_report(y_test, y_pred))

    mlflow.log_param("n_estimators", 20)
    mlflow.log_metric("accuracy", accuracy)

    mlflow.sklearn.log_model(model, "model")

    joblib.dump(model, "models/fraud_model.pkl")

    print("Accuracy:", accuracy)
    print("Model saved successfully!")
