class ScenarioSimulationAgent:
    def run(self, demand: float) -> dict:
        return {
            "low": round(demand * 0.85),
            "medium": round(demand),
            "high": round(demand * 1.15)
        }
