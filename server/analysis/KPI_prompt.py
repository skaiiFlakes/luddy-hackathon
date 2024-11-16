import pandas as pd

def generate_prompt(data):
    """
    Generates ChatGPT prompts for financial analysis based on KPIs.

    Parameters:
        data (pd.DataFrame): A DataFrame with columns ['KPI', 'Specific Inputs, design additions'].

    Returns:
        str: The final prompt for financial analysis.
    """
    if 'KPI' not in data.columns or 'Specific Inputs, design additions' not in data.columns:
        raise ValueError("Data must contain 'KPI' and 'Specific Inputs, design additions' columns.")
    
    # Build the prompt
    prompt = "Analyze the following financial metrics with the given inputs:\n\n"
    
    for _, row in data.iterrows():
        kpi = row['KPI']
        inputs = row['Specific Inputs, design additions']
        prompt += f"- **{kpi}**: {inputs}\n"
    
    prompt += "\nProvide 10 actionable strategies based on KPI provided, highlighting trends, recommendations, and areas for improvement."
    return prompt

# Example usage
if __name__ == "__main__":
    # Load the KPI data from a CSV or manually create it
    kpi_data = pd.DataFrame({
        "KPI": [
            "Customer Acquisition Costs", "Churn Rate", "Average order size",
            "Monthly Recurring Revenue", "Annual Run Rate", "Cash Runway",
            "Burn Rate", "K - factor (virality)", "Gross sales",
            "NPS / Product market fit", "CAC / LTV ratio"
        ],
        "Specific Inputs, design additions": [
            "Monthly ad spending", "% churn rate", "$ in average spent per customer",
            "$ in expected sales from customers per month", "$ expected from customers per year, important",
            "Time (months) to achieve profitability", "$ per month spent by startup",
            "Average invites or mentions per user", "Monthly $ in gross sales",
            "(% Promoters - % Detractors) from feedback of scale 1-10",
            "Total monthly sales and marketing costs, monthly customers acquired"
        ]
    })

# Generate and print the prompt
final_prompt = generate_prompt(kpi_data)
print(final_prompt)