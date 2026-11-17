import pandas as pd
import numpy as np


class SimilarityAnalysisAgent:
    """
    Identifies top proxy products using multi-dimensional similarity scoring.
    Operates at PRODUCT level (not daily rows).
    """

    def run(
        self,
        new_product: dict,
        historical_df: pd.DataFrame,
        top_k: int = 10
    ) -> list:
        """
        Returns a list of proxy products with similarity scores.
        """
      
        product_df = (historical_df.drop_duplicates(subset=["product_id"]).reset_index(drop=True))
        df = product_df.copy()

         
        # CATEGORICAL MATCHES         
        df["category_match"] = (df["category"] == new_product["category"]).astype(int)
        df["sub_category_match"] = (df["sub_category"] == new_product["sub_category"]).astype(int)
        df["brand_match"] = (df["brand"] == new_product["brand"]).astype(int)
        df["channel_match"] = (df["primary_channel"] == new_product["expected_channel"]).astype(int)
        df["market_match"] = (df["target_market"] == new_product["target_market"]).astype(int)

         
        # PRICE SIMILARITY   
        new_price = float(new_product["expected_mrp"])

        df["price_similarity"] = 1 - (abs(df["selling_price"] - new_price) / new_price)
        df["price_similarity"] = df["price_similarity"].clip(0, 1)

         
        # FINAL SIMILARITY SCORE (WEIGHTED)         
        df["similarity_score"] = (
            0.35 * (0.7 * df["category_match"] + 0.3 * df["sub_category_match"]) +
            0.20 * df["price_similarity"] +
            0.15 * df["market_match"] +
            0.15 * df["channel_match"] +
            0.15 * df["brand_match"]
        )

         
        # SELECT TOP PROXY PRODUCTS         
        top_df = (df.sort_values("similarity_score", ascending=False).head(top_k))

                       
        proxy_products = [
            {
                "product_id": row["product_id"],
                "similarity_score": round(row["similarity_score"], 3)
            }
            for _, row in top_df.iterrows()
        ]

        return proxy_products