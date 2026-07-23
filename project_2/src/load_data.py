from sklearn.datasets import load_iris
import pandas as pd

def get_data():
    iris = load_iris()

    X = iris.data
    y = iris.target

    df = pd.DataFrame(
        X,
        columns=iris.feature_names
    )

    df["target"] = y

    return X, y, iris, df