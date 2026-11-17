import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


class DemandEstimationAgent:

    def run(self, new_product, df: pd.DataFrame, trend_factor: float):

        if df.empty:
            return self._empty_output()

        df = df.copy()

         
        # DATE PARSING         
        df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
        df = df.dropna(subset=["date"])

        launch_date = datetime.strptime(
            new_product["planned_launch_date"], "%Y-%m-%d"
        )

        # Use last 3 years of proxy data
        df = df[df["date"].dt.year >= launch_date.year - 3]

        if df.empty:
            return self._empty_output()

         
        # MONTHLY BASELINE DEMAND         
        monthly_sales = (
            df.groupby(["product_id", df["date"].dt.to_period("M")])["units_sold"]
            .sum()
            .reset_index()
        )

        baseline_monthly = (
            monthly_sales
            .groupby("product_id")["units_sold"]
            .mean()
            .mean()
        )

         
        # PRICE, PROMOTION, TREND         
        avg_proxy_price = df["selling_price"].mean()
        new_price = float(new_product["expected_mrp"])

        price_multiplier = avg_proxy_price / new_price
        price_adjusted = baseline_monthly * price_multiplier

        promo_multiplier = 1.1 if new_product["promotion_strategy_at_launch"] == "Yes" else 1.0

        final_monthly = price_adjusted * promo_multiplier * trend_factor

        yearly_target = final_monthly * 12

        confidence = "high" if len(monthly_sales) >= 36 else "medium"

         
        # DAILY SEASONALITY (PROXY DATA)         
        df["day_of_year"] = df["date"].dt.dayofyear

        daily_product_sales = (
            df.groupby(["product_id", "day_of_year"])["units_sold"]
            .sum()
            .reset_index()
        )

        daily_avg = (
            daily_product_sales
            .groupby("day_of_year")["units_sold"]
            .mean()
        )

        num_proxy_products = df["product_id"].nunique()
        daily_avg = daily_avg / num_proxy_products

         
        # FORECAST DAILY (1 YEAR)         
        forecast_days = []
        current = launch_date

        while current < launch_date + timedelta(days=365):
            doy = current.timetuple().tm_yday
            base_units = daily_avg.get(doy, daily_avg.mean())

            forecast_days.append({
                "date": current.strftime("%Y-%m-%d"),
                "base_units": base_units
            })

            current += timedelta(days=1)

        total_base_units = sum(d["base_units"] for d in forecast_days)

        if total_base_units == 0:
            return self._empty_output()

        daily_forecast = [
            {
                "date": d["date"],
                "forecast_units": int(round((d["base_units"] / total_base_units) * yearly_target))
            }
            for d in forecast_days
        ]

         
        # WRITE CSV WITH FULL TRACEABILITY         
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, "new_product_demand_forecast(!).csv")

        factors_row = {
            "baseline_monthly_demand": round(baseline_monthly, 2),
            "avg_proxy_price": round(avg_proxy_price, 2),
            "new_product_price": round(new_price, 2),
            "price_multiplier": round(price_multiplier, 4),
            "promo_multiplier": promo_multiplier,
            "trend_factor": trend_factor,
            "final_monthly_demand": round(final_monthly, 2),
            "yearly_target_demand": round(yearly_target, 2),
            "num_proxy_products": num_proxy_products,
            "confidence": confidence
        }

        factors_df = pd.DataFrame([factors_row])

        forecast_df = pd.DataFrame(daily_forecast)

        with open(output_path, "w", newline="") as f:
            factors_df.to_csv(f, index=False)
            f.write("\n")
            forecast_df.to_csv(f, index=False)

        return {
            "baseline_monthly_demand": int(round(baseline_monthly)),
            "final_adjusted_demand": int(round(final_monthly)),
            "daily_forecast_file": output_path,
            "confidence": confidence
        }

    def _empty_output(self):
        return {
            "baseline_monthly_demand": 0,
            "final_adjusted_demand": 0,
            "daily_forecast_file": None,
            "confidence": "low"
        }
