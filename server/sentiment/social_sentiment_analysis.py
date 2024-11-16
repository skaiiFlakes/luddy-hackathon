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

            # Reddit/Twitter Tech Enthusiasm
            'based': 1.5,
            'goated': 2.0,
            'fire': 1.5,
            'ship': 1.0,  # as in "shipping features"
            'shipped': 1.0,
            'shipping': 1.0,
            'clutch': 1.5,
            'peak': 1.5,
            'huge': 1.5,
            'massive': 1.5,
            'major': 1.0,
            'elite': 1.5,
            'valid': 1.0,
            'chad': 1.5,

            # Tech/Business Criticism
            'copium': -1.5,
            'hopium': -1.0,
            'mid': -1.0,
            'yikes': -1.5,
            'oof': -1.0,
            'rip': -1.5,
            'dead': -1.5,
            'trash': -2.0,
            'garbage': -2.0,
            'joke': -1.5,
            'scam': -2.0,
            'sus': -1.0,
            'sketchy': -1.5,
            'yeet': -1.0,
            'aged poorly': -1.5,
            'aged like milk': -2.0,
            'aged like wine': 1.5,

            # Tech Community Slang
            'bullish': 1.5,
            'bearish': -1.5,
            'hodl': 1.0,
            'fud': -1.5,
            'shill': -1.0,
            'bagholder': -1.5,
            'paper hands': -1.0,
            'diamond hands': 1.0,
            'moonshot': 1.0,
            'mooning': 1.5,
            'tanking': -1.5,
            'dumping': -1.5,

            # Common Abbreviations
            'tbh': 0.0,
            'imo': 0.0,
            'imho': 0.0,
            'fwiw': 0.0,
            'til': 0.5,
            'eli5': 0.0,
            'tldr': 0.0,
            'afaik': 0.0,
            'iykyk': 0.5,

            # Tech/Business Success
            'w': 1.5,
            'dub': 1.5,
            'win': 1.5,
            'winning': 1.5,
            'stonks': 1.0,
            'banger': 1.5,
            'slaps': 1.5,
            'crushing it': 2.0,
            'killing it': 2.0,
            'smashing it': 2.0,

            # Tech/Business Failure
            'l': -1.5,
            'fail': -1.5,
            'failing': -1.5,
            'flopped': -1.5,
            'trainwreck': -2.0,
            'disaster': -2.0,
            'mess': -1.5,
            'rekt': -1.5,

            # Common Tech Topics
            'collab': 1.0,
            'partnership': 1.0,
            'stack': 0.0,
            'ecosystem': 0.5,
            'community': 0.5,
            'toxic': -1.5,
            'fanboy': -0.5,
            'salty': -1.0,

            # Additional Emojis
            '💎': 1.5,  # Often used for "diamond hands" or valuable
            '🚀': 1.5,  # Strong positive/growth
            '🔥': 1.5,  # Hot/successful
            '🐂': 1.0,  # Bullish
            '🐻': -1.0,  # Bearish
            '🤡': -1.5,  # Mockery
            '💀': -1.0,  # Dead/failed
            '👀': 0.5,  # Interest/attention
            '📈': 1.5,  # Stonks/growth
            '📉': -1.5,  # Decline
            '🎯': 1.0,  # On target
            '🧠': 1.0,  # Smart/intellectual
            '🤝': 1.0,  # Deal/agreement
            '💪': 1.0,  # Strong
            '🏆': 1.5,  # Victory/achievement
            '⭐': 1.0,  # Star/quality
            '💯': 1.5,  # Perfect/complete agreement

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
                'state-of-the-art': 1.5,

                # Tech Community Terms
                'stack': 0.0,
                'repo': 0.0,
                'codebase': 0.0,
                'legacy code': -0.5,
                'technical debt': -1.0,
                'spaghetti code': -1.5,
                'clean code': 1.5,
                'bloated': -1.5,
                'lightweight': 1.5,
                'workaround': -0.5,
                'hack': -0.5,
                'backdoor': -1.5,
                'exploit': -1.5,

                # Tech Product Discussion
                'fanboy': -0.5,
                'ecosystem': 0.5,
                'vendor lock': -1.5,
                'backwards compatible': 1.0,
                'future proof': 1.5,
                'overpriced': -1.5,
                'worth it': 1.5,
                'premium': 1.0,
                'bloatware': -1.5,

                # Development Terms
                'refactor': 0.0,
                'optimize': 1.0,
                'deprecate': -0.5,
                'sunset': -0.5,
                'kill': -1.0,  # as in "killing a feature"
                'deadcode': -1.0,
                'bottleneck': -1.0,
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
                'goals': 0.5,

                # Business Community Terms
                'unicorn': 1.5,
                'cash cow': 1.5,
                'burn rate': -0.5,
                'runway': 0.0,
                'pivot': 0.0,
                'bootstrapped': 1.0,
                'funded': 1.0,
                'series a': 1.0,
                'angel': 1.0,
                'vc': 0.0,

                # Market Discussion
                'bearish': -1.0,
                'bullish': 1.0,
                'priced in': 0.0,
                'undervalued': 1.0,
                'overvalued': -1.0,
                'moat': 1.5,
                'competitive edge': 1.5,

                # Business Performance
                'crushing it': 2.0,
                'killing it': 2.0,
                'bleeding': -1.5,
                'hemorrhaging': -2.0,
                'printing': 1.5,  # as in "printing money"
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

    def summarize_sentiment(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate summary of analyzed posts by grouping similar texts based on their first 4 words.

        Args:
            df (pd.DataFrame): DataFrame with columns 'original_text' and 'sentiment_score'

        Returns:
            pd.DataFrame: DataFrame with columns:
                - group_text: First 4 words of the text
                - average_sentiment_score: Mean sentiment score for the group
                - closest_post: Original text with sentiment closest to group average
                - second_closest_post: Original text with second closest sentiment to group average
        """

        # Extract the first four words of the original text
        def get_first_4_words(text):
            return ' '.join(str(text).split()[:4])

        df['group_text'] = df['original_text'].apply(get_first_4_words)

        # Group by the extracted text and calculate the average sentiment score
        summary = df.groupby('group_text').agg(
            average_sentiment_score=('sentiment_score', 'mean')
        ).reset_index()

        # Merge the average sentiment scores back with the original DataFrame
        df_with_avg = df.merge(summary, on='group_text')

        # Find the closest and second closest posts to the average sentiment score
        def find_closest_posts(group):
            # Calculate absolute difference from average
            avg_score = group['average_sentiment_score'].iloc[0]
            differences = abs(group['sentiment_score'] - avg_score)

            # Get indices of two smallest differences
            closest_indices = differences.nsmallest(2).index

            # Get the corresponding posts
            closest_posts = group.loc[closest_indices, 'original_text'].tolist()

            return pd.Series({
                'closest_post': closest_posts[0] if len(closest_posts) > 0 else None,
                'second_closest_post': closest_posts[1] if len(closest_posts) > 1 else None
            })

        # Apply the function to find closest posts for each group
        closest_posts_df = df_with_avg.groupby('group_text', group_keys=False).apply(find_closest_posts).reset_index()

        # Merge all results
        final_summary = summary.merge(closest_posts_df, on='group_text')

        # Return sorted by average sentiment score
        return final_summary[
            ['group_text', 'average_sentiment_score', 'closest_post', 'second_closest_post']].sort_values(
            'average_sentiment_score', ascending=False
        )


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