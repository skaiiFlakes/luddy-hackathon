import json
from dotenv import load_dotenv
import openai
import os

load_dotenv()

def prompt(inputs):
    api_key = os.environ.get('OPENAI_API_KEY')
    client = openai.OpenAI(
    organization='org-rDJcL7q9nR2pzHnxeN1ipwQF',
    project='proj_Wm3JVHDej00hqCWSR2Ri6wVz',
    api_key=api_key
    )

    kpi = inputs.get('kpi')
    industry = inputs.get('industry')
    current_kpi = inputs.get('currentStatus')
    desired_kpi = inputs.get('targetStatus')
    deadline = inputs.get('deadline')

    try:
        with open(f"preprocessed_files/{industry}_sentiment.txt", "r") as f:
            sentiment_context = f.read()
    except:
        sentiment_context = "No sentiment context available for this industry."

    try:
        with open(f"preprocessed_files/{industry}_financial_analysis.txt", "r") as f:
            financial_context = f.read()
    except:
        financial_context = "No financial context available for this industry."

    # try:
    #     sentiment_context = get_sentiment_context(industry)
    # except Exception as e:
    #     with open("news_sentiment.txt", "r") as f:
            # sentiment_context = f.read()


    my_prompt = """
**Inputs:**
1. **Startup KPIs:**
    - KPI: %s
    - Industry: %s
    - Current KPI performance: %s
    - Desired KPI performance: %s
    - Deadline for improvement: %s
2. **Industry Financial Context:**
    %s
3. **Sentiment Analysis:**
    %s

**Tasks:**

You MUST create EXACTLY 10 main business objectives, each with EXACTLY 3 subtasks (total of 40 tasks). Any response with fewer tasks will be rejected.

1. Create the 10 highly specific, measurable main business objectives that will help achieve the KPI improvement from %s to %s. Each objective MUST:
    - Include specific numerical targets with proper formatting (use commas for thousands)
    - Have a clear metric that can be measured
    - Be directly related to improving the main KPI
    - Reference the provided industry context or sentiment analysis

2. For each main objective, provide EXACTLY 3 practical implementation subtasks that:
    - Are concrete actions that team members can take
    - Don't require numerical targets
    - Describe specific steps to achieve the parent objective

3. For each main objective, provide:
    - TaskID: integers 1-10
    - TaskName: A SMART objective that follows this exact format:
      "[Action Verb] [Specific Metric] from [Current Number with commas] to [Target Number with commas] (include $ if currency)"
      Example formats:
      - "Increase monthly revenue from $1,000,000 to $1,500,000"
      - "Reduce customer churn rate from 15%% to 8%%"
    - Description: 3 concise sentences that MUST:
      1. Draw meaningful inferences from sentiment patterns
      2. Connect industry trends to specific market opportunities
      3. Explain how this objective addresses the market dynamics

4. For each subtask, provide:
    - TaskID: MUST be one of: "A", "B", or "C"
    - TaskName: A specific action item starting with an action verb
    - StartDate: date in ISO format (YYYY-MM-DD)
    - Duration: integer number of days
    - The Duration MUST be used to calculate the end date in the parent task's TaskName

VALIDATION REQUIREMENTS:
1. MUST have EXACTLY 10 main tasks
2. Each main task MUST have EXACTLY 3 subtasks
3. Subtask IDs MUST be "A", "B", or "C"
4. Main task IDs MUST be integers 1-10

CRITICAL: Your response MUST maintain the exact following JSON property names. DO NOT modify, rename, or restructure any properties:

{
    "recommendations": [
        {
            "TaskID": 1,
            "TaskName": "Example task name",
            "Description": "Example description",
            "subtasks": [
                {
                    "TaskID": "A",
                    "TaskName": "Example subtask",
                    "StartDate": "2024-01-01",
                    "Duration": 30
                },
                {
                    "TaskID": "B",
                    "TaskName": "Example subtask",
                    "StartDate": "2024-02-01",
                    "Duration": 30
                },
                {
                    "TaskID": "C",
                    "TaskName": "Example subtask",
                    "StartDate": "2024-03-01",
                    "Duration": 30
                }
            ]
        }
    ]
}""" % (kpi, industry, current_kpi, desired_kpi, deadline, financial_context, sentiment_context, current_kpi, desired_kpi)

    system_prompt = """You are a precise business strategy analyst who MUST create EXACTLY 10 specific business objectives, each with EXACTLY 3 subtasks (total 40 tasks). You excel at:
1. Drawing meaningful inferences from data instead of stating raw numbers
2. Identifying subtle market patterns and their business implications
3. Writing varied, concise sentences without repetitive patterns
4. Using proper number formatting (commas for thousands) and currency symbols ($) for monetary values

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
