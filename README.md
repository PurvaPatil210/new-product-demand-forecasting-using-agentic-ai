
# New Product Demand Forecasting Using Agentic AI

## Project Overview

This project focuses on predicting demand for newly launched products using an Agentic AI-based forecasting approach.

Since new products in FMCG market do not have historical sales data, the system identifies similar existing products and uses their historical sales information to estimate demand.

The system combines product similarity analysis, market intelligence, demand estimation and scenario simulation to generate demand forecasts.

## Key Features

- **Market Intelligence:** Collects market trends using Google Trends and Google News.
- **Similarity Analysis:** Identifies similar existing products using weighted similarity scoring.
- **Demand Estimation:** Estimates product demand using historical sales, pricing, promotions and market trends.
- **Scenario Simulation:** Generates low, medium and high demand scenarios.
- **Feedback and Learning:** Implements a feedback mechanism to evaluate forecast accuracy and adjust forecasting weights.

## Agent Architecture

The project consists of five modular agents:

1. Market Intelligence Agent
2. Similarity Analysis Agent
3. Demand Estimation Agent
4. Scenario Simulation Agent
5. Feedback and Learning Agent

The first four agents are integrated into the forecasting pipeline. The Feedback and Learning Agent is implemented separately.

## Technology Stack

- Python
- Pandas
- NumPy
- Google Trends (PyTrends)
- Google News RSS
- Power BI

## Project Structure

internship_project/
│
├── agents/
│   ├── demand_estimation_agent.py
│   ├── feedback_learning_agent.py
│   ├── market_intelligence_agent.py
│   ├── scenario_simulation_agent.py
│   └── similarity_analysis_agent.py
│
├── data/
│   └── Dataset files (not included)
│
├── outputs/
│   └── Generated forecasts (not included)
│
├── pipelines/
│   └── forecasting_pipeline.py
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md

## Installation and Setup

### 1. Clone the Repository

git clone YOUR_GITHUB_REPOSITORY_URL

### 2. Navigate to the Project Directory

cd internship_project

### 3. Create a Virtual Environment

python -m venv venv

### 4. Activate the Virtual Environment

Windows:

venv\Scripts\activate

### 5. Install Dependencies

pip install -r requirements.txt

### 6. Add Required Datasets

Place the authorized input datasets inside the data/ directory using the expected filenames:

- New Product launch Info.csv
- Similar product dataset.csv

The company-provided datasets are not included in this repository.

### 7. Run the Project

python main.py

## Output

The system generates:

- Baseline monthly demand
- Final adjusted monthly demand
- Forecast confidence level
- Daily demand forecast for one year
- Low, medium and high demand scenarios

## Dashboard

A Power BI dashboard was developed to visualize demand forecasting results.

## Note

This repository contains the project implementation and source code. Company-provided datasets and confidential information are excluded.
