import openai
import tiktoken
import os

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

api_key = os.environ.get('OPENAI_API_KEY')

client = openai.OpenAI(
  organization='org-rDJcL7q9nR2pzHnxeN1ipwQF',
  project='proj_Wm3JVHDej00hqCWSR2Ri6wVz',
  api_key=api_key
)

my_prompt = """
    ```
**Inputs:**

1. **Startup KPIs:**
    - Current KPI performance: [Provide details].
    - Desired KPI performance: [Provide details].
    - Deadline for improvement: [Provide details].
2. **Industry Context:**
    - Industry name: [Provide details].
    - Financial health: Overall industry averages and top competitor metrics [Provide details].
3. **Sentiment Analysis:**
    - Social media sentiment and key phrases: [Provide details].
    - News sentiment and key phrases: [Provide details].
    - Financial headline sentiment and key phrases: [Provide details].

**Tasks:**

1. Analyze the provided inputs to identify key performance gaps and opportunities.
2. Recommend the top 10 actionable strategies that the startup can implement to improve its KPIs to the desired level within the stated timeline.
3. For each strategy, provide:
    - **Task Name:** A concise, descriptive name for the recommendation.
    - **Summary:** A one-sentence summary of the strategy.
    - **Details:** 2-5 sentences explaining the rationale behind the recommendation and its expected impact.
    - **Timeline:** A suggested start and end date for each task that aligns with the deadline.
4. Output the results in a JSON format structured as follows:

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
        "task": "Task Name",
        "summary": "One-sentence summary",
        "details": "Detailed rationale for the recommendation.",
        "timeline": { "start": "YYYY-MM-DD", "end": "YYYY-MM-DD" }
      }
      ... repeat for 10 tasks total
    ]
  }
}
```

**Notes:**

- Ensure the recommendations are actionable and prioritize tasks based on the provided data and urgency.
- The timeline should align with the stated KPI improvement deadline and consider dependencies or sequencing of tasks.
- Focus on strategies that leverage positive sentiment trends, address financial or competitive gaps, and align with industry benchmarks.

## **Sample JSON response:**

```jsx
{
  "inputs": {
    "KPIs": {
      "current": {
        "metric1": { "value": 45, "unit": "%" },
        "metric2": { "value": 3000, "unit": "users" }
      },
      "desired": {
        "metric1": { "value": 70, "unit": "%" },
        "metric2": { "value": 5000, "unit": "users" }
      },
      "deadline": "2024-12-31"
    },
    "industry": {
      "name": "Technology - SaaS",
      "financial_health": {
        "industry_average": { "revenue_growth": 15, "profit_margin": 12 },
        "top_competitors": [
          { "name": "Competitor A", "revenue_growth": 20, "profit_margin": 18 },
          { "name": "Competitor B", "revenue_growth": 18, "profit_margin": 15 }
        ]
      }
    },
    "sentiment_analysis": {
      "social_media": { "sentiment": "positive", "key_phrases": ["user-friendly", "innovative features"] },
      "news": { "sentiment": "neutral", "key_phrases": ["market challenges", "growth potential"] },
      "financial_headlines": { "sentiment": "positive", "key_phrases": ["investment opportunities", "expanding market"] }
    }
  },
  "outputs": {
    "recommendations": [
      {
        "task": "Enhance Product Features",
        "summary": "Improve user retention by launching innovative features.",
        "details": "Based on positive sentiment around innovation, prioritize adding features aligned with user feedback.",
        "timeline": { "start": "2024-01-01", "end": "2024-04-30" }
      },
      {
        "task": "Optimize Marketing Spend",
        "summary": "Redirect marketing budget towards channels with higher ROI.",
        "details": "Shift focus to digital channels with measurable success, especially those with strong user sentiment.",
        "timeline": { "start": "2024-01-15", "end": "2024-03-15" }
      },
      {
        "task": "Expand Customer Support",
        "summary": "Enhance customer experience with improved support systems.",
        "details": "Address common user complaints and leverage AI tools for scalable customer interaction.",
        "timeline": { "start": "2024-02-01", "end": "2024-06-30" }
      },
      {
        "task": "Partnerships for Market Expansion",
        "summary": "Collaborate with industry leaders for cross-promotional benefits.",
        "details": "Identify partners in related industries to increase visibility and shared growth.",
        "timeline": { "start": "2024-01-01", "end": "2024-05-31" }
      },
      {
        "task": "Invest in Employee Training",
        "summary": "Boost productivity by upskilling employees.",
        "details": "Focus on training related to current market trends and technological advancements.",
        "timeline": { "start": "2024-03-01", "end": "2024-06-30" }
      },
      {
        "task": "Refine Sales Funnel",
        "summary": "Streamline the sales process to increase conversion rates.",
        "details": "Analyze drop-off points and optimize lead nurturing campaigns.",
        "timeline": { "start": "2024-01-10", "end": "2024-03-30" }
      },
      {
        "task": "Launch a Referral Program",
        "summary": "Encourage current users to invite new customers.",
        "details": "Implement a program offering rewards for successful referrals to drive organic growth.",
        "timeline": { "start": "2024-02-01", "end": "2024-03-31" }
      },
      {
        "task": "Target New Geographies",
        "summary": "Expand into high-potential markets.",
        "details": "Analyze market research to identify regions with unmet demand.",
        "timeline": { "start": "2024-04-01", "end": "2024-12-31" }
      },
      {
        "task": "Increase Content Marketing",
        "summary": "Build brand authority with high-quality content.",
        "details": "Produce blogs, case studies, and videos highlighting the product's unique selling points.",
        "timeline": { "start": "2024-01-15", "end": "2024-06-30" }
      },
      {
        "task": "Analyze and Act on Feedback",
        "summary": "Use user feedback to guide iterative improvements.",
        "details": "Implement feedback loops for faster adaptation to user needs.",
        "timeline": { "start": "2024-01-01", "end": "2024-12-31" }
      }
    ]
  }
}
```
)
"""

# sample_text = my_prompt
# token_count = count_tokens(sample_text)
# print(f"Number of tokens: {token_count}")

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are an expert business strategist and data analyst. Your task is to analyze a startup's provided context and recommend the top 10 actionable strategies to help improve their KPIs to desired levels within a specified deadline. Use the provided information on the startup’s industry, financial metrics, competitor benchmarks, and sentiment analysis to guide your recommendations."},
    {"role": "user", "content": my_prompt}
  ]
)
print(completion.choices[0].message.content)
print(type(completion.choices[0].message.content))
