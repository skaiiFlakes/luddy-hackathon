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

            # Positive amplifiers
            'literally': 1.2,
            'actually': 1.1,
            'officially': 1.2,
            'legitimately': 1.2,
            'absolutely': 1.3,

            # Negative amplifiers
            'supposedly': 0.8,
            'apparently': 0.9,
            'allegedly': 0.7,
            'lowkey': 0.9,
            'kinda': 0.8,

            # Trend indicators
            'trending': 1.2,
            'viral': 1.2,
            'breaking': 1.1,
            'exclusive': 1.2,

            # Tech emphasis
            'ai-powered': 1.2,
            'blockchain': 1.1,
            'cloud-based': 1.1,
            'digital': 1.1,

            # Business emphasis
            'enterprise': 1.2,
            'professional': 1.1,
            'corporate': 1.0,
            'startup': 1.1,

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
            '‼️': 1.5,  # Double exclamation
            '⁉️': 1.3,  # Exclamation question
            '✨': 1.2,  # Sparkles (emphasis)
            '❤️': 1.0,  # Love/appreciation
            '👍': 1.0,  # Thumbs up
            '💡': 1.0,  # Idea
            '📊': 0.0
        }

        # Sector-specific lexicons
        self.sector_lexicons = {
            'automotive': {
            # Professional terms
            'recall': -2.0,
            'safety': 1.0,
            'emissions': 0.0,
            'efficiency': 1.0,
            'reliability': 1.5,
            'warranty': 0.5,
            'defect': -1.5,
            'mileage': 0.5,

            # Industry innovation
            'ev': 1.0,
            'autonomous': 1.0,
            'self-driving': 1.0,
            'electric': 1.0,
            'hybrid': 0.5,
            'hydrogen': 0.5,

            # Social media
            'gas guzzler': -1.5,
            'dream car': 2.0,
            'ricer': -1.0,
            'sleeper': 1.5,
            'clean': 1.5,
            'mint': 1.5,
            'beater': -1.0,
            'lemon': -1.5,

            # Emojis
            '🚗': 0.5,
            '🏎️': 1.0,
            '⚡': 1.0,
            '🔋': 0.5,
            '🚙': 0.5,
        },

        'banking': {
            # Professional terms
            'liquidity': 0.5,
            'assets': 0.5,
            'portfolio': 0.0,
            'default': -2.0,
            'leverage': 0.0,
            'yield': 0.5,
            'dividend': 1.0,
            'mortgage': 0.0,

            # Risk terms
            'risk': -0.5,
            'exposure': -0.5,
            'hedge': 0.5,
            'collateral': 0.0,

            # Social media
            'rugpull': -2.0,
            'ponzi': -2.0,
            'printer': -1.0,
            'whale': 1.0,
            'bagholder': -1.5,
            'diamond hands': 1.5,
            'paper hands': -1.0,

            # Emojis
            '🏦': 0.0,
            '💰': 1.0,
            '💸': -1.0,
            '📈': 1.5,
        },

        'construction': {
            # Professional terms
            'development': 0.5,
            'completion': 1.0,
            'delay': -1.5,
            'on-schedule': 1.5,
            'over-budget': -1.5,
            'under-budget': 1.5,
            'permit': 0.0,
            'inspection': 0.0,

            # Quality terms
            'quality': 1.0,
            'defect': -1.5,
            'structurally sound': 1.5,
            'code compliant': 1.0,

            # Social media
            'eyesore': -1.5,
            'beautiful': 1.5,
            'prime location': 1.5,
            'nightmare': -2.0,

            # Emojis
            '🏗️': 0.5,
            '🏢': 0.5,
            '🏠': 0.5,
            '🚧': 0.0,
        },

        'education': {
            # Professional terms
            'accredited': 1.0,
            'enrollment': 0.0,
            'graduation': 1.5,
            'curriculum': 0.0,
            'academic': 0.5,
            'research': 0.5,

            # Performance terms
            'achievement': 1.5,
            'performance': 0.5,
            'grades': 0.0,
            'scores': 0.0,

            # Social media
            'crushing it': 1.5,
            'struggling': -1.0,
            'stress': -1.0,
            'easy a': 1.0,

            # Emojis
            '🎓': 1.0,
            '📚': 0.5,
            '✏️': 0.0,
            '🏫': 0.0,
        },

        'energy': {
            # Professional terms
            'renewable': 1.5,
            'sustainable': 1.5,
            'efficiency': 1.0,
            'capacity': 0.0,
            'grid': 0.0,
            'infrastructure': 0.0,

            # Environmental impact
            'clean': 1.5,
            'emissions': -0.5,
            'carbon': -0.5,
            'green': 1.0,

            # Social media
            'dirty energy': -1.5,
            'clean energy': 1.5,
            'power outage': -1.5,
            'blackout': -2.0,

            # Emojis
            '⚡': 1.0,
            '🔋': 0.5,
            '☀️': 1.0,
            '💨': 0.5,
        },

        'fashion': {
            # Professional terms
            'collection': 0.5,
            'designer': 1.0,
            'sustainable': 1.0,
            'luxury': 1.5,
            'premium': 1.0,
            'fast fashion': -0.5,

            # Trend terms
            'trending': 1.5,
            'viral': 1.5,
            'statement': 1.0,
            'iconic': 2.0,

            # Social media
            'slay': 2.0,
            'fire': 1.5,
            'basic': -1.0,
            'drip': 1.5,

            # Emojis
            '👗': 0.5,
            '👠': 0.5,
            '💅': 1.0,
            '✨': 1.0,
        },

        'food_and_beverage': {
            # Professional terms
            'organic': 1.0,
            'sustainable': 1.0,
            'quality': 1.0,
            'fresh': 1.0,
            'recall': -2.0,
            'contamination': -2.0,

            # Experience terms
            'delicious': 1.5,
            'taste': 0.0,
            'flavor': 0.0,
            'experience': 0.5,

            # Social media
            'bussin': 2.0,
            'mid': -1.0,
            'overrated': -1.0,
            'underrated': 1.0,

            # Emojis
            '🍽️': 0.5,
            '🍷': 0.5,
            '👨‍🍳': 1.0,
            '😋': 1.5,
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