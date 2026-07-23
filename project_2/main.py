from src.load_data import get_data
from src.preprocess import preprocess_data
from src.model import train_model
from src.evaluate import evaluate_model

import seaborn as sns
import matplotlib.pyplot as plt


print("="*50)
print("DECODELABS PROJECT 2")
print("DATA CLASSIFICATION USING AI")
print("="*50)

# Load Data
X, y, iris, df = get_data()

print("\nDataset Head:\n")
print(df.head())

# Preprocess
(
    X_train,
    X_test,
    y_train,
    y_test,
    scaler
) = preprocess_data(
    X,
    y
)

print("\nTraining Samples:")
print(len(X_train))

print("\nTesting Samples:")
print(len(X_test))

# Train Model
model = train_model(
    X_train,
    y_train
)

# Evaluate
(
    accuracy,
    f1,
    cm,
    report,
    predictions
) = evaluate_model(
    model,
    X_test,
    y_test
)

print("\nAccuracy:")
print(accuracy)

print("\nF1 Score:")
print(f1)

print("\nConfusion Matrix:")
print(cm)

print("\nClassification Report:")
print(report)

# Save Confusion Matrix
plt.figure(figsize=(6,4))

sns.heatmap(
    cm,
    annot=True,
    fmt='d'
)

plt.title(
    "Confusion Matrix"
)

plt.xlabel(
    "Predicted"
)

plt.ylabel(
    "Actual"
)

plt.savefig(
    "screenshots/confusion_matrix.png"
)

plt.show()

# Custom Prediction
sample = [[
    5.1,
    3.5,
    1.4,
    0.2
]]

sample = scaler.transform(
    sample
)

prediction = model.predict(
    sample
)

print(
    "\nCustom Prediction:"
)

print(
    iris.target_names[
        prediction[0]
    ]
)