from pricing_core import (
    default_csv_path,
    load_market_data,
    predict_price_etb,
    train_pipeline,
)


def predict_price(name: str, model) -> str:
    val = predict_price_etb(model, name)
    return f"Suggested Price for '{name}': ETB {val:,.2f}"


if __name__ == "__main__":
    csv_path = default_csv_path()
    try:
        df = load_market_data(csv_path)
        print(f"📊 Loaded {len(df)} items from your Ethiopian market dataset.")
    except FileNotFoundError:
        print("❌ Error: market_data.csv not found. Run your scraper first!")
        raise SystemExit(1) from None

    print("🧠 Training the AI on current market trends...")
    trained = train_pipeline(df)
    print("✅ Training complete!")

    print("-" * 40)
    print(predict_price("iPhone 13 128GB", trained))
    print(predict_price("Samsung Galaxy S21", trained))
    print(predict_price("Redmi Note 12", trained))
    print("-" * 40)
