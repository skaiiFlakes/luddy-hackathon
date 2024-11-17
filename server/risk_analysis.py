import openai
import os
from dotenv import load_dotenv


# given 1 kpi, create a risk score for the startup,
def get_kpi_risk_level(kpi_name: str, value: float) -> str:
    """
    Return risk level for a given KPI value.
    For startups between 3 months and 2 years old.
    Returns: 'Critical', 'High', 'Medium', 'Low', or 'Minimal'
    """

    kpi_metrics = {
        "CAC": {
            "critical": 500,  # $500
            "warning": 300,  # $300
            "healthy": 100,  # $100
            "type": "lower_better"
        },
        "CR": {
            "critical": 0.10,  # 10%
            "warning": 0.05,  # 5%
            "healthy": 0.02,  # 2%
            "type": "lower_better"
        },
        "AOS": {
            "critical": 10,  # $10
            "warning": 50,  # $50
            "healthy": 100,  # $100
            "type": "higher_better"
        },
        "MRR": {
            "critical": 10000,  # $10k
            "warning": 30000,  # $30k
            "healthy": 100000,  # $100k
            "type": "higher_better"
        },
        "ARR": {
            "critical": 120000,  # $120k
            "warning": 360000,  # $360k
            "healthy": 1200000,  # $1.2M
            "type": "higher_better"
        },
        "CR": {
            "critical": 3,  # 3 months
            "warning": 6,  # 6 months
            "healthy": 12,  # 12 months
            "type": "higher_better"
        },
        "BR": {
            "critical": 100000,  # $100k monthly
            "warning": 50000,  # $50k monthly
            "healthy": 20000,  # $20k monthly
            "type": "lower_better"
        },
        "KF": {
            "critical": 0.5,  # 0.5
            "warning": 0.9,  # 0.9
            "healthy": 1.1,  # 1.1
            "type": "higher_better"
        },
        "GS": {
            "critical": 20000,  # $20k monthly
            "warning": 50000,  # $50k monthly
            "healthy": 150000,  # $150k monthly
            "type": "higher_better"
        },
        "MAU": {
            "critical": 1000,  # 1k users
            "warning": 5000,  # 5k users
            "healthy": 10000,  # 10k users
            "type": "higher_better"
        },
        "NPS": {
            "critical": 20,
            "warning": 40,
            "healthy": 60,
            "type": "higher_better"
        },
        "LTV/CAC": {
            "critical": 1,  # 1:1 ratio
            "warning": 2,  # 2:1 ratio
            "healthy": 3,  # 3:1 ratio
            "type": "higher_better"
        }
    }

    if kpi_name not in kpi_metrics:
        return "Unknown KPI"

    try:
        metric = int(kpi_metrics[kpi_name])

        if metric["type"] == "higher_better":
            if value <= metric["critical"]:
                return "Critical"
            elif value <= metric["warning"]:
                return "High"
            elif value <= metric["healthy"]:
                return "Medium"
            elif value <= metric["healthy"] * 1.5:
                return "Low"
            else:
                return "Minimal"
        else:  # lower_better
            if value >= metric["critical"]:
                return "Critical"
            elif value >= metric["warning"]:
                return "High"
            elif value >= metric["healthy"]:
                return "Medium"
            elif value >= metric["healthy"] * 0.5:
                return "Low"
            else:
                return "Minimal"
    except ValueError:
        return "Unknown"
# use this risk score and previous context, rank the suggestions for the startup

load_dotenv()

def get_risk_rankings(industry: str="", KPI: str="", value: float=0.0) -> list[list[str, int]]:
    api_key = os.environ.get('OPENAI_API_KEY')
    client = openai.OpenAI(
    organization='org-rDJcL7q9nR2pzHnxeN1ipwQF',
    project='proj_Wm3JVHDej00hqCWSR2Ri6wVz',
    api_key=api_key
    )

    # TODO: get suggestions from json file
    suggestions = ""
    risk = get_kpi_risk_level(kpi_name=KPI, value=value)

    my_prompt = """
    Given that my startup is in the %s industry space, and my startup's %s KPI is currently %s risk,
    rank the following suggestions based on risk level of tackling that problem first, from low to high, where 1 is low, and 10 is high:
    %s
    Output in a list of lists of rankings and a 1 sentence description of what risks might be involved (if risk > 5) or what market openings and opportunities there are (if risk < 5),
    Format it this way: [[ranking, description], [ranking, description], ...]
    """ % industry, KPI, risk, suggestions

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": my_prompt}
    ]
    )

    result = {"kpi_status": risk, "risk_levels": completion.choices[0].message.content}
    return result
