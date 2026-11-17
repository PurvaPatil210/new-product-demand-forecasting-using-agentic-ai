import numpy as np


class FeedbackLearningAgent:
    """
    Learns from actual post-launch sales and corrects future demand forecasts.
    """

    def run(
        self,
        forecast_weekly: list,
        actual_weekly: list,
        current_weights: dict
    ) -> dict:

        if not forecast_weekly or not actual_weekly:
            return {
                "mape": None,
                "bias": None,
                "updated_weights": current_weights,
                "correction_factor": 1.0
            }

        # Align weeks
        actual_map = {
            w["week"]: w["units_sold"] for w in actual_weekly
        }

        errors = []
        bias_values = []

        for f in forecast_weekly:
            week = f["week"]
            if week in actual_map and actual_map[week] > 0:
                forecast = f["demand"]
                actual = actual_map[week]

                error = abs(actual - forecast) / actual
                bias = (actual - forecast) / actual

                errors.append(error)
                bias_values.append(bias)

        if not errors:
            return {
                "mape": None,
                "bias": None,
                "updated_weights": current_weights,
                "correction_factor": 1.0
            }

        # Metrics
        mape = round(np.mean(errors) * 100, 2)
        bias = round(np.mean(bias_values), 3)

        # Correction factor
        correction_factor = 1 + bias
        correction_factor = max(0.7, min(1.3, correction_factor))

        # Weight learning
        actual_weight = min(
            0.9,
            current_weights["actual"] + 0.1
        )

        proxy_weight = round(1 - actual_weight, 2)

        updated_weights = {
            "proxy": proxy_weight,
            "actual": actual_weight
        }

        return {
            "mape": mape,
            "bias": bias,
            "correction_factor": round(correction_factor, 2),
            "updated_weights": updated_weights
        }
