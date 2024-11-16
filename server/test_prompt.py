import openai
import tiktoken
import os
from dotenv import load_dotenv
import generate_sentiment as gs

def count_tokens(text, model="gpt-3.5-turbo"):
    """
    Count tokens for a given text using the specified model's encoding.

    Args:
        text (str): The text to count tokens for
        model (str): The model to use for encoding (default: gpt-3.5-turbo)

    Returns:
        int: Number of tokens in the text
    """
    encoding = tiktoken.encoding_for_model(model)

    # For chat models, we need to account for message formatting
    if model.startswith("gpt-3.5-turbo") or model.startswith("gpt-4"):
        # Add tokens for message formatting
        messages = [
            {"role": "system", "content": "You are a helpful business strategist and data analyst."},
            {"role": "user", "content": text}
        ]

        num_tokens = 0
        for message in messages:
            # Every message follows <im_start>{role/name}\n{content}<im_end>\n
            num_tokens += 4
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
        num_tokens += 2  # Every reply is primed with <im_start>assistant
        return num_tokens

    # For non-chat models, simply encode and count
    return len(encoding.encode(text))

load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')
client = openai.OpenAI(
  organization='org-rDJcL7q9nR2pzHnxeN1ipwQF',
  project='proj_Wm3JVHDej00hqCWSR2Ri6wVz',
  api_key=api_key
)

kpi = "customer base"
current_kpi = "5000"
desired_kpi = "2000000"
deadline = "6 months"
industry = "Technology"
financial_metrics = "10% revenue growth, 15% profit margin"
social_media_sentiment = "Positive sentiment, key phrases: 'great product', 'excellent service'"
news_sentiment = "Neutral sentiment, key phrases: 'new product launch', 'industry trends'"
financial_headline_sentiment = "Negative sentiment, key phrases: 'declining revenue', 'increased competition'"
sentiments = gs.get_sentiment_context(industry)

my_prompt = """
**Inputs:**
1. **Startup KPIs:**
    - KPI: %s.
    - Current KPI performance: %s.
    - Desired KPI performance: %s.
    - Deadline for improvement: %s.
2. **Industry Context:**
    - Industry name: %s.
    - Financial health: %s.
3. **Sentiment Analysis:**
    - Social media, news, and financial headline sentiment analysis: %s

**Tasks:**

1. Analyze the provided inputs to identify key performance gaps and opportunities.
2. Recommend the top 10 main tasks that the startup can implement to improve its KPIs to the desired level within the stated timeline. Include 3 subtasks for every strategy/main task. There must be a total of 40 tasks.
3. For each main task, provide:
    - TaskID: an integer
    - TaskName**:** A concise, descriptive name for the recommendation.
    - Description**:** 2-5 sentences explaining the recommendation and its expected impact.
4. For each subtask, provide:
    - TaskID: an integer
    - TaskName**:** A concise, descriptive name for the recommendation.
    - Description**:** 2-5 sentences explaining the recommendation and its expected impact.
    - StartDate: date object
    - Duration: integer in days
5. Output the results in a JSON format structured as follows:

```json
{
  "inputs": {
    "KPIs": { ... },
    "industry": { ... },
    "sentiment_analysis": { ... }
  },
  "outputs": {
    "recommendations": [
      {
	      "TaskID": 1,
        "TaskName": "Task Name",
        "Description": "Description",
        "subtasks": [
		      {
		        "TaskID": 2,
		        "TaskName": "Task Name",
		        "Description": "Description",
		        "StartDate": new Date('04/03/2020'),
		        "Duration": 3, //in days
		      }
		      //include 2 more, for 3 total subtasks per main task
        ]
      }
    ]
  }
}
```

**Notes:**

- Ensure the recommendations are actionable and prioritize tasks based on the provided data and urgency.
- The timeline should align with the stated KPI improvement deadline and consider dependencies or sequencing of tasks.
- Focus on strategies that leverage positive sentiment trends, address financial or competitive gaps, and align with industry benchmarks
""" % (kpi, current_kpi, desired_kpi, deadline, industry, financial_metrics, sentiments)

# sample_text = my_prompt
# token_count = count_tokens(sample_text)
# print(f"Number of tokens: {token_count}")

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are an expert business strategist and data analyst. Your task is to analyze a startup's provided context and recommend the top 10 actionable strategies, each with 3 subtasks to help improve their KPIs to desired levels within a specified deadline. Use the provided information on the startup’s industry, financial metrics, competitor benchmarks, and sentiment analysis to guide your recommendations."},
    {"role": "user", "content": my_prompt}
  ]
)
# Save completion to a file
print(completion.choices[0].message.content)
print(type(completion.choices[0].message.content))

with open('recommendations.json', 'w') as file:
  file.write(completion.choices[0].message.content)
