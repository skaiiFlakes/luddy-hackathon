import pandas as pd
from transformers import pipeline
from datetime import datetime
import re
from typing import Dict, List, Optional


class FinancialNewsSentiment:
    def __init__(self):
        """Initialize sentiment analyzer with financial-specific adjustments"""
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="siebert/sentiment-roberta-large-english",
            truncation=True
        )

        # Financial market terms with sentiment context
        self.market_terms = {
            # Strong negative terms (-1.0)
            'crash': -1.0,
            'collapse': -1.0,
            'crisis': -1.0,
            'bankruptcy': -1.0,
            'default': -1.0,

            # Moderate negative terms (-0.7)
            'plunge': -0.7,
            'plummet': -0.7,
            'slump': -0.7,
            'tumble': -0.7,
            'decline': -0.7,
            'drop': -0.7,
            'falls': -0.7,
            'losses': -0.7,
            'downturn': -0.7,
            'recession': -0.7,
            'bearish': -0.7,

            # Mild negative terms (-0.3)
            'dip': -0.3,
            'slip': -0.3,
            'weaken': -0.3,
            'concern': -0.3,
            'volatile': -0.3,
            'uncertainty': -0.3,

            # Strong positive terms (1.0)
            'surge': 1.0,
            'soar': 1.0,
            'record high': 1.0,
            'breakthrough': 1.0,
            'boom': 1.0,

            # Moderate positive terms (0.7)
            'rally': 0.7,
            'gain': 0.7,
            'advance': 0.7,
            'growth': 0.7,
            'profit': 0.7,
            'recovery': 0.7,
            'bullish': 0.7,
            'upgrade': 0.7,
            'outperform': 0.7,

            # Mild positive terms (0.3)
            'rise': 0.3,
            'improve': 0.3,
            'up': 0.3,
            'higher': 0.3,
            'stable': 0.3
        }

        # Magnitude modifiers
        self.magnitude_modifiers = {
            'billion': 1.2,
            'millions': 1.1,
            'massive': 1.3,
            'significant': 1.2,
            'slight': 0.8,
            'minor': 0.7
        }

    def analyze_financial_terms(self, text: str) -> float:
        """Analyze presence and impact of financial terms"""
        text = text.lower()
        score = 0
        magnitude = 1.0

        # Check for magnitude modifiers
        for modifier, mod_value in self.magnitude_modifiers.items():
            if modifier in text:
                magnitude *= mod_value

        # Analyze financial terms
        for term, term_score in self.market_terms.items():
            if term in text:
                score += term_score * magnitude

        return score

    def chunk_article(self, article: str, max_length: int = 512) -> List[str]:
        """Split article into chunks for processing"""
        # Split into sentences (basic implementation)
        sentences = re.split(r'(?<=[.!?])\s+', article)
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_length:
                current_chunk += " " + sentence if current_chunk else sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def analyze_article(self, article: str) -> Dict:
        """Analyze a full article text"""
        # Split article into manageable chunks
        chunks = self.chunk_article(article)

        # Analyze each chunk
        chunk_sentiments = []
        for chunk in chunks:
            base_sentiment = self.sentiment_analyzer(chunk)[0]
            financial_score = self.analyze_financial_terms(chunk)

            chunk_sentiments.append({
                'base_sentiment': base_sentiment,
                'financial_score': financial_score
            })

        # Calculate overall sentiment
        avg_financial_score = sum(c['financial_score'] for c in chunk_sentiments) / len(chunk_sentiments)
        avg_base_score = sum((1 if c['base_sentiment']['label'] == 'POSITIVE' else -1) *
                             c['base_sentiment']['score'] for c in chunk_sentiments) / len(chunk_sentiments)

        # Combine scores with financial terms having higher weight
        combined_score = (avg_financial_score * 0.7 + avg_base_score * 0.3)

        # Determine final sentiment
        if combined_score > 0.1:
            final_sentiment = 'POSITIVE'
        elif combined_score < -0.1:
            final_sentiment = 'NEGATIVE'
        else:
            final_sentiment = 'NEUTRAL'

        return {
            'sentiment': final_sentiment,
            'score': combined_score,
            'financial_term_score': avg_financial_score,
            'base_model_score': avg_base_score,
            'chunk_count': len(chunks)
        }

    def analyze_headline(self, headline: str) -> Dict:
        """Analyze a single financial headline"""
        base_sentiment = self.sentiment_analyzer(headline)[0]
        financial_score = self.analyze_financial_terms(headline)

        combined_score = (financial_score * 0.7 +
                          (1 if base_sentiment['label'] == 'POSITIVE' else -1) *
                          base_sentiment['score'] * 0.3)

        if combined_score > 0.1:
            final_sentiment = 'POSITIVE'
        elif combined_score < -0.1:
            final_sentiment = 'NEGATIVE'
        else:
            final_sentiment = 'NEUTRAL'

        return {
            'headline': headline,
            'sentiment': final_sentiment,
            'score': combined_score,
            'base_model_sentiment': base_sentiment['label'],
            'base_model_score': base_sentiment['score'],
            'financial_term_score': financial_score,
            'timestamp': datetime.now()
        }

    def analyze_news_item(self, headline: str, article: Optional[str] = None) -> Dict:
        """Analyze both headline and article text if provided"""
        headline_analysis = self.analyze_headline(headline)

        if article:
            article_analysis = self.analyze_article(article)

            # Combine headline and article analysis (headline weighted more heavily)
            combined_score = (headline_analysis['score'] * 0.6 +
                              article_analysis['score'] * 0.4)

            if combined_score > 0.1:
                final_sentiment = 'POSITIVE'
            elif combined_score < -0.1:
                final_sentiment = 'NEGATIVE'
            else:
                final_sentiment = 'NEUTRAL'

            return {
                'headline': headline,
                'overall_sentiment': final_sentiment,
                'overall_score': combined_score,
                'headline_analysis': headline_analysis,
                'article_analysis': article_analysis,
                'timestamp': datetime.now()
            }

        return headline_analysis

    def analyze_batch(self, headlines: List[str], articles: Optional[List[str]] = None) -> pd.DataFrame:
        """Analyze a batch of financial news items"""
        results = []

        if articles is not None and len(headlines) != len(articles):
            raise ValueError("Number of headlines must match number of articles")

        for i, headline in enumerate(headlines):
            article = articles[i] if articles else None
            results.append(self.analyze_news_item(headline, article))

        return pd.DataFrame(results)

    def generate_summary(self, df: pd.DataFrame) -> Dict:
        """Generate summary statistics from analysis results"""
        if 'overall_sentiment' in df.columns:
            sentiment_col = 'overall_sentiment'
            score_col = 'overall_score'
        else:
            sentiment_col = 'sentiment'
            score_col = 'score'

        return {
            'total_analyzed': len(df),
            'sentiment_distribution': df[sentiment_col].value_counts().to_dict(),
            'average_sentiment_score': df[score_col].mean(),
            'most_positive': df.loc[df[score_col].idxmax()]['headline'],
            'most_negative': df.loc[df[score_col].idxmin()]['headline'],
            'neutral_count': len(df[df[sentiment_col] == 'NEUTRAL']),
            'timestamp': datetime.now()
        }


# Example usage
if __name__ == "__main__":
    # Initialize analyzer
    analyzer = FinancialNewsSentiment()

    # Test headlines and articles
    test_headlines = [
        "Tech Giant Reports Record Q4 Profits",
        "Market Crashes as Inflation Hits 40-Year High"
    ]

    test_articles = [
        """The company announced unprecedented growth in their fourth quarter, 
        with revenues exceeding analyst expectations by 25%. The strong performance 
        was driven by new product launches and expanding market share...""",

        """Global markets experienced their worst day in months as inflation data 
        showed persistent price pressures. The selloff intensified in the afternoon 
        as traders digested the implications for monetary policy..."""
    ]

    # Analyze with both headlines and articles
    results_df = analyzer.analyze_batch(test_headlines, test_articles)

    # Generate summary
    summary = analyzer.generate_summary(results_df)

    # Print results
    print("\nDetailed Analysis Results:")
    pd.set_option('display.max_columns', None)
    print(results_df)

    print("\nAnalysis Summary:")
    for key, value in summary.items():
        if key != 'timestamp':
            print(f"{key}: {value}")