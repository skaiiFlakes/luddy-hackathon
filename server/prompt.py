import json
from generate_sentiment import get_sentiment_context
from dotenv import load_dotenv
import openai
import os
import datetime

load_dotenv()

def prompt(inputs):
    api_key = os.environ.get('OPENAI_API_KEY')
    client = openai.OpenAI(
    organization='org-rDJcL7q9nR2pzHnxeN1ipwQF',
    project='proj_Wm3JVHDej00hqCWSR2Ri6wVz',
    api_key=api_key
    )

    business_description = inputs.get('businessDescription')
    kpi = inputs.get('kpi')
    industry = inputs.get('industry')
    current_kpi = inputs.get('currentStatus')
    desired_kpi = inputs.get('targetStatus')
    deadline = inputs.get('deadline')
    start_date = str(datetime.datetime.now())
    print(kpi, current_kpi, desired_kpi, deadline, industry)

    sentiment_context = "Unkown"
    try :
        if os.path.exists("preprocessed_files/" + industry.lower() + "_sentiment.txt"):
            sentiment_file = open("preprocessed_files/" + industry.lower() + "_sentiment.txt", "r")
            sentiment_context = sentiment_file.read()
            sentiment_file.close()
    except Exception as e:
        pass

    financial_context = "Unkown"
    try:
        if os.path.exists("preprocessed_files/" + industry.lower().title().replace(' ','_') + "_financial_analysis.txt"):
            financial_file = open("preprocessed_files/" + industry.lower().title().replace(' ','_') + "_financial_analysis.txt", "r")
            financial_context = financial_file.read()
            financial_file.close()

    except Exception as e:
        pass

    # try:
    #     sentiment_context = get_sentiment_context(industry)
    # except Exception as e:
    #     with open("news_sentiment.txt", "r") as f:
            # sentiment_context = f.read()

    # print(sentiment_context)


    my_prompt = """
**Inputs:**
1. ** BEGIN Startup KPIs:**
    - Business Description: %s
    - KPI: %s
    - Industry: %s
    - Current KPI performance: %s
    - Desired KPI performance: %s
    - Deadline for improvement: %s
    - Overall start date: %s
    ** END Startup KPIs **
2. ** BEGIN Industry Financial Context:**
    %s
   ** END Industry Financial Context **
3. **BEGIN Sentiment Analysis:**
    %s
   **END Sentiment Analysis**

**BEGIN Tasks:**

You MUST create EXACTLY 10 main business objectives, each with EXACTLY 3 subtasks (total of 40 tasks). Any response with fewer tasks will be rejected.

1. Create the 10 highly specific, measurable main business objectives that will help achieve the KPI improvement from %s to %s. Each objective MUST:
    - Include specific numerical targets with proper formatting (use commas for thousands)
    - Have a clear metric that can be measured
    - Be directly related to improving the main KPI
    - Reference the provided industry context or sentiment analysis
    - Include a risk assessment value from 1-5 (1 being lowest risk, 5 being highest risk)

2. For each main objective, provide EXACTLY 3 practical implementation subtasks that:
    - Are concrete actions that team members can take
    - Don't require numerical targets
    - Describe specific steps to achieve the parent objective
    - Include a risk assessment value from 1-5 that correlates with the parent task's risk level
      (If parent task risk is 1-2, subtask risks should be 1-3)
      (If parent task risk is 3, subtask risks should be 2-4)
      (If parent task risk is 4-5, subtask risks should be 3-5)


3. For each main objective, provide:
    - TaskID: integers 1-10
    - TaskName: A SMART objective that follows this exact format:
      "[Action Verb] [Specific Metric] to [Target Number with commas] (include $ if currency)"
      Example formats:
      - "Increase monthly revenue from $1,000,000 to $1,500,000"
      - "Reduce customer churn rate from 15%% to 8%%"
    - Description: 3 concise sentences that MUST:
      1. Draw meaningful inferences from sentiment patterns
      2. Connect industry trends to specific market opportunities
      3. Explain how this objective addresses the market dynamics
      4. Use varied sentence structures without repetitive patterns
    - RiskLevel: integer from 1-5 indicating implementation risk
    - Main Objectives should be made in sequential order



4. For each subtask, provide:
    - TaskID: MUST be one of: "A", "B", or "C"
    - TaskName: A specific action item starting with an action verb
    - StartDate: date in ISO format (YYYY-MM-DD)
    - Duration: integer number of days to complete the subtask
    - RiskLevel: integer from 1-5 that correlates with parent task risk level
**END Tasks**


**BEGIN VALIDATION REQUIREMENTS:**
1. MUST have EXACTLY 10 main tasks
2. Each main task MUST have EXACTLY 3 subtasks
3. Subtask IDs MUST be "A", "B", or "C"
4. Main task IDs MUST be integers 1-10
5. Risk levels MUST be integers 1-5
6. Subtask risk levels MUST correlate with parent task risk level according to the specified ranges
7. The start date of the FIRST main task MUST be the current date
8. The end date of the LAST main task MUST NOT exceed the provided deadline
**END VALIDATION REQUIREMENTS**

CRITICAL: Your response MUST maintain the exact following JSON property names. DO NOT modify, rename, or restructure any properties:

{
    "recommendations": [
        {
            "TaskID": 1,
            "TaskName": "Example task name",
            "Description": "Example description",
            "RiskLevel": int,
            "subtasks": [
                {
                    "TaskID": "A",
                    "TaskName": "Example subtask",
                    "StartDate": "YYYY-MM-DD",
                    "Duration": int,
                    "RiskLevel": int
                },
                {
                    "TaskID": "B",
                    "TaskName": "Example subtask",
                    "StartDate": "YYYY-MM-DD",
                    "Duration": int,
                    "RiskLevel": int
                },
                {
                    "TaskID": "C",
                    "TaskName": "Example subtask",
                    "StartDate": "YYYY-MM-DD",
                    "Duration": int,
                    "RiskLevel": int
                }
            ]
        }
    ]
}""" % (business_description, kpi, industry, current_kpi, desired_kpi, deadline, start_date, financial_context, sentiment_context, current_kpi, desired_kpi)

    system_prompt = """You are a precise business strategy analyst who MUST create EXACTLY 10 specific business objectives, each with EXACTLY 3 subtasks (total 40 tasks). You excel at:
1. Drawing meaningful inferences from data instead of stating raw numbers
2. Identifying subtle market patterns and their business implications
3. Writing varied, concise sentences without repetitive patterns
4. Using proper number formatting (commas for thousands) and currency symbols ($) for monetary values
5. Creating SMART objectives with specific, measurable, achievable, relevant, and time-bound targets
6. Assessing implementation risks and their cascading effects on subtasks
7. Creating timelines to complete all main objectives by the desired deadline
8. Create tasking with realistic multi-month durations that fill the time from start to the deadline

STRICT REQUIREMENTS:
- Generate EXACTLY 10 main tasks (no more, no less)
- Generate EXACTLY 3 subtasks per main task (no more, no less)
- Use task IDs 1-10 for main tasks
- Use task IDs A, B, C for subtasks
- All property names in the JSON response MUST be enclosed in double quotes

Your response MUST be a valid JSON object with all property names in double quotes. Return only the JSON object."""

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": my_prompt}
        ]
    )

    # Ensure we're getting clean JSON without any markdown
    response_text = completion.choices[0].message.content.strip()
    print(response_text)
    if response_text.startswith('```'):
        response_text = response_text.split('```')[1]
        if response_text.startswith('json'):
            response_text = response_text[4:]
    response_text = response_text.strip()

    # Parse and validate the JSON before returning
    try:
        return json.loads(response_text)
    except json.JSONDecodeError as e:
        print(f"JSON Error: {e}")
        print(f"Problematic JSON: {response_text}")
        raise

if __name__ == "__main__":
    inputs = {
        "kpi": "Gross Sales",
        "industry": "Fashion",
        "currentStatus": 1000,
        "targetStatus": 100000,
        "deadline": "2025-11-17T16:12:16+0000"
    }
    prompt(inputs)
