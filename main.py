import pandas as pd
from pipelines.forecasting_pipeline import ForecastingPipeline

NEW_PRODUCT_PATH = "data/New Product launch Info.csv"
SIMILAR_PRODUCTS_PATH = "data/Similar product dataset.csv"


def main():
    new_product = pd.read_csv(NEW_PRODUCT_PATH).iloc[0].to_dict()
    historical_df = pd.read_csv(SIMILAR_PRODUCTS_PATH)

    pipeline = ForecastingPipeline()
    result = pipeline.run(new_product, historical_df)

    demand = result["demand"]

    print("\n=== FINAL DEMAND FORECAST ===\n")
    print(f"Baseline Monthly Demand : {demand['baseline_monthly_demand']}")
    print(f"Final Adjusted Demand   : {demand['final_adjusted_demand']}")
    print(f"Confidence              : {demand['confidence']}")

    if "daily_forecast_file" in demand:
        print(f"\nDaily forecast saved to: {demand['daily_forecast_file']}")


if __name__ == "__main__":
    main()
