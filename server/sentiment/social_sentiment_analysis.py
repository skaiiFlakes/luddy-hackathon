import pandas as pd
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import emoji
import re
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Optional, Union


class SocialSentiment:
    def __init__(self, sector: str = "tech"):
        """
        Initialize sentiment analyzer with tech/business-specific lexicon

        Args:
            sector (str): Specific sector to analyze ('tech', 'business', 'fintech', 'enterprise')
        """
        import nltk
        try:
            nltk.data.find('sentiment/vader_lexicon.zip')
        except LookupError:
            nltk.download('vader_lexicon')

        self.vader = SentimentIntensityAnalyzer()

        # Professional social media lexicon
        self.professional_lexicon = {
            # General professional terms
            'innovative': 2.0,
            'disrupting': 1.5,
            'revolutionary': 2.0,
            'breakthrough': 2.0,
            'seamless': 1.5,
            'streamlined': 1.5,
            'optimized': 1.5,
            'efficient': 1.5,
            'inefficient': -1.5,
            'robust': 1.5,
            'scalable': 1.5,
            'sustainable': 1.5,
            'resilient': 1.5,

            # Performance indicators
            'outperform': 2.0,
            'underperform': -2.0,
            'exceeded': 2.0,
            'missed': -1.5,
            'surpassed': 2.0,
            'lagging': -1.5,
            'leading': 1.5,
            'impressive': 1.5,
            'disappointing': -1.5,

            # Business impact
            'profitable': 2.0,
            'unprofitable': -2.0,
            'revenue': 0.0,
            'growth': 1.5,
            'decline': -1.5,
            'expansion': 1.5,
            'contraction': -1.5,
            'acquisition': 0.5,
            'merger': 0.5,
            'partnership': 1.0,
            'collaboration': 1.0,

            # Professional social media terms
            'masterclass': 2.0,
            'gamechanging': 2.0,
            'gamechanger': 2.0,
            'outstanding': 2.0,
            'stellar': 2.0,
            'subpar': -1.5,
            'underwhelming': -1.5,
            'promising': 1.5,
            'concerning': -1.5,

            # Market position
            'marketleader': 2.0,
            'marketshare': 0.0,
            'competitive': 1.0,
            'dominant': 1.5,
            'niche': 0.0,

            # Common emojis in professional context
            '📈': 1.5,
            '📊': 0.0,
            '🚀': 1.5,
            '💡': 1.0,
            '🎯': 1.0,
            '🤝': 1.0,
            '💪': 1.0,
            '📉': -1.5,
        }

        # Sector-specific lexicons
        self.sector_lexicons = {
            'tech': {
                # Product Development
                'bugfix': 0.5,
                'patch': 0.0,
                'release': 0.5,
                'launch': 1.0,
                'beta': 0.0,
                'stable': 1.0,
                'unstable': -1.5,
                'deployment': 0.0,
                'rollout': 0.0,

                # Technical Performance
                'latency': -1.0,
                'downtime': -2.0,
                'uptime': 1.5,
                'reliable': 2.0,
                'unreliable': -2.0,
                'scalable': 1.5,
                'responsive': 1.5,
                'unresponsive': -1.5,

                # Features & Integration
                'integration': 1.0,
                'compatibility': 1.0,
                'incompatible': -1.5,
                'functionality': 0.0,
                'feature': 0.5,
                'interface': 0.0,
                'api': 0.0,
                'sdk': 0.0,

                # Tech Innovation
                'ai': 0.5,
                'ml': 0.5,
                'cloud': 0.5,
                'blockchain': 0.5,
                'quantum': 0.5,
                'innovation': 1.5,
                'cutting-edge': 1.5,
                'state-of-the-art': 1.5
            },

            'business': {
                # Financial Performance
                'profitable': 2.0,
                'unprofitable': -2.0,
                'margin': 0.0,
                'revenue': 0.0,
                'profit': 1.5,
                'loss': -1.5,
                'valuation': 0.0,
                'roi': 0.0,

                # Market Performance
                'marketshare': 0.0,
                'competitive': 1.0,
                'competition': 0.0,
                'industry': 0.0,
                'sector': 0.0,
                'market': 0.0,

                # Operations
                'efficiency': 1.5,
                'inefficiency': -1.5,
                'productivity': 1.5,
                'operational': 0.0,
                'logistics': 0.0,
                'supply': 0.0,
                'demand': 0.0,

                # Strategy
                'strategy': 0.0,
                'strategic': 0.5,
                'roadmap': 0.5,
                'vision': 0.5,
                'mission': 0.5,
                'goals': 0.5
            },

            'fintech': {
                # Financial Technology
                'payment': 0.0,
                'transaction': 0.0,
                'processing': 0.0,
                'settlement': 0.0,
                'encryption': 1.0,
                'security': 1.0,
                'breach': -2.0,
                'fraud': -2.0,

                # Performance
                'throughput': 0.0,
                'volume': 0.0,
                'capacity': 0.0,
                'compliance': 1.0,
                'non-compliant': -1.5,
                'regulatory': 0.0,

                # User Experience
                'user-friendly': 1.5,
                'intuitive': 1.5,
                'friction': -1.0,
                'frictionless': 1.5,
                'seamless': 1.5
            },

            'enterprise': {
                # Enterprise Solutions
                'solution': 0.5,
                'enterprise': 0.0,
                'infrastructure': 0.0,
                'platform': 0.0,
                'service': 0.0,

                # Implementation
                'implementation': 0.0,
                'deployment': 0.0,
                'adoption': 0.5,
                'migration': 0.0,
                'integration': 0.5,

                # Support
                'support': 0.5,
                'maintenance': 0.0,
                'upgrade': 0.5,
                'downgrade': -0.5,
                'sla': 0.0,

                # Security
                'security': 1.0,
                'vulnerability': -1.5,
                'patch': 0.5,
                'update': 0.5,
                'breach': -2.0
            }
        }

        # Add sector-specific lexicon
        if sector in self.sector_lexicons:
            self.vader.lexicon.update(self.sector_lexicons[sector])

        # Add professional lexicon
        self.vader.lexicon.update(self.professional_lexicon)

    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess professional social media text"""
        if not isinstance(text, str):
            return ''

        # Convert to lowercase
        text = text.lower()

        # Convert emojis to text
        text = emoji.demojize(text)

        # Handle hashtags - keep the text but remove #
        text = re.sub(r'#(\w+)', r'\1', text)

        # Handle mentions - keep for context but clean format
        text = re.sub(r'@(\w+)', r'\1', text)

        # Handle URLs
        text = re.sub(r'http\S+|www.\S+', '', text)

        # Handle common business abbreviations
        abbreviations = {
            'roi': 'return on investment',
            'saas': 'software as a service',
            'b2b': 'business to business',
            'b2c': 'business to consumer',
            'kpi': 'key performance indicator',
            'api': 'application programming interface',
            'ai': 'artificial intelligence',
            'ml': 'machine learning',
            'ar': 'augmented reality',
            'vr': 'virtual reality',
            'iot': 'internet of things'
        }

        for abbr, expanded in abbreviations.items():
            text = re.sub(r'\b' + abbr + r'\b', expanded, text)

        # Handle multiple spaces
        text = ' '.join(text.split())

        return text

    def analyze_text(self, text: str, include_raw: bool = False) -> Dict:
        """
        Analyze sentiment of a single piece of text

        Args:
            text (str): Text to analyze
            include_raw (bool): Include raw VADER and TextBlob scores
        """
        cleaned_text = self.preprocess_text(text)

        # Get VADER sentiment
        vader_scores = self.vader.polarity_scores(cleaned_text)

        # Get TextBlob sentiment
        blob = TextBlob(cleaned_text)
        textblob_sentiment = blob.sentiment

        # Combine scores with VADER weighted more heavily
        combined_score = (vader_scores['compound'] * 0.7 +
                          textblob_sentiment.polarity * 0.3)

        result = {
            'original_text': text,
            'cleaned_text': cleaned_text,
            'sentiment_score': combined_score,
            'sentiment': self._get_sentiment_label(combined_score),
            'timestamp': datetime.now()
        }

        if include_raw:
            result.update({
                'vader_scores': vader_scores,
                'textblob_polarity': textblob_sentiment.polarity,
                'textblob_subjectivity': textblob_sentiment.subjectivity
            })

        return result

    def _get_sentiment_label(self, score: float) -> str:
        """Convert score to sentiment label"""
        if score >= 0.5:
            return 'STRONGLY POSITIVE'
        elif 0.1 <= score < 0.5:
            return 'POSITIVE'
        elif -0.1 < score < 0.1:
            return 'NEUTRAL'
        elif -0.5 <= score < -0.1:
            return 'NEGATIVE'
        else:
            return 'STRONGLY NEGATIVE'

    def analyze_batch(self, texts: List[str], include_raw: bool = False) -> pd.DataFrame:
        """Analyze a batch of texts"""
        results = [self.analyze_text(text, include_raw) for text in texts]
        return pd.DataFrame(results)

    def analyze_with_metrics(self, text: str, company: Optional[str] = None,
                             metrics: Optional[List[str]] = None) -> Dict:
        """
        Analyze text with focus on business metrics

        Args:
            text (str): Text to analyze
            company (str, optional): Company name for context
            metrics (list, optional): List of metrics to track (e.g., ['revenue', 'growth', 'market_share'])
        """
        result = self.analyze_text(text, include_raw=True)

        if metrics:
            metric_mentions = defaultdict(list)
            for metric in metrics:
                # Find mentions of metric with nearby numbers
                pattern = rf'\b{metric}\b[^.]*?(?:\d+(?:\.\d+)?(?:\s*%)?)'
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    metric_mentions[metric] = matches

            result['metrics'] = dict(metric_mentions)

        if company:
            result['company_mentions'] = len(re.findall(rf'\b{company}\b', text, re.IGNORECASE))

        return result


# Example usage
if __name__ == "__main__":
    # Initialize analyzer for tech sector
    analyzer = SocialSentiment(sector='tech')

    # Test posts
    test_posts = [
        "Excited to announce our new AI-powered platform has achieved 99.9% uptime! 🚀 #TechInnovation",
        "Q2 results show 45% YoY growth in enterprise customers. Strong momentum in cloud adoption. 📈",
        "Recent service disruption impacted 5% of users. Working on permanent fix. We appreciate your patience.",
        "Our latest release introduces seamless integration with major cloud providers. #Enterprise #Cloud"
    ]

    # Analyze posts
    results_df = analyzer.analyze_batch(test_posts, include_raw=True)

    # Print results
    print("\nSentiment Analysis Results:")
    print(results_df[['original_text', 'sentiment', 'sentiment_score']])

    # Example with metrics
    metrics_analysis = analyzer.analyze_with_metrics(
        "Q2 revenue grew 40% to $100M, with cloud services showing 60% growth in market share",
        metrics=['revenue', 'growth', 'market share']
    )

    print("\nMetrics Analysis Example:")
    print(metrics_analysis)