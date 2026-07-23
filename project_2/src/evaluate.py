from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    f1_score
)

def evaluate_model(
        model,
        X_test,
        y_test
):

    predictions = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    f1 = f1_score(
        y_test,
        predictions,
        average="weighted"
    )

    cm = confusion_matrix(
        y_test,
        predictions
    )

    report = classification_report(
        y_test,
        predictions
    )

    return (
        accuracy,
        f1,
        cm,
        report,
        predictions
    )