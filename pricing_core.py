"""Shared training and prediction logic for the pricing pipeline."""

from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline, make_pipeline


def default_csv_path() -> Path:
    return Path(__file__).resolve().parent / "market_data.csv"


def load_market_data(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    if "product_name" not in df.columns or "price" not in df.columns:
        raise ValueError("CSV must contain 'product_name' and 'price' columns.")
    return df


def train_pipeline(df: pd.DataFrame) -> Pipeline:
    model = make_pipeline(TfidfVectorizer(), LinearRegression())
    model.fit(df["product_name"], df["price"])
    return model


def predict_price_etb(model: Pipeline, product_name: str) -> float:
    raw = float(model.predict([product_name])[0])
    return max(0.0, raw)
