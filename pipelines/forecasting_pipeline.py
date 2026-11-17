from agents.similarity_analysis_agent import SimilarityAnalysisAgent
from agents.market_intelligence_agent import MarketIntelligenceAgent
from agents.demand_estimation_agent import DemandEstimationAgent
from agents.scenario_simulation_agent import ScenarioSimulationAgent


class ForecastingPipeline:
    def run(self, new_product, historical_df):

        similarity_agent = SimilarityAnalysisAgent()
        market_agent = MarketIntelligenceAgent()
        demand_agent = DemandEstimationAgent()
        scenario_agent = ScenarioSimulationAgent()
         
        # Returns list of proxy products with similarity
        similar_products = similarity_agent.run(
            new_product, historical_df
        )

        # Extract proxy product IDs
        proxy_product_ids = [
            p["product_id"] for p in similar_products
        ]

                  
        proxy_sales_df = historical_df[
            historical_df["product_id"].isin(proxy_product_ids)
        ]

        # Safety check
        if proxy_sales_df.empty:
            raise ValueError("No historical data found for proxy products")

         
        # MARKET INTELLIGENCE        
        trend_factor = market_agent.run(new_product)

         
        # DEMAND ESTIMATION 
        demand_result = demand_agent.run(
            new_product,
            proxy_sales_df,
            trend_factor
        )

         
        # SCENARIO SIMULATION         
        scenarios = scenario_agent.run(
            demand_result["final_adjusted_demand"]
        )

        return {
            "demand": demand_result,
            "scenarios": scenarios
        }
