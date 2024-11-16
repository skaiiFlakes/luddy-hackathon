import pandas as pd
from transformers import pipeline
from datetime import datetime
from typing import Dict, List
import os


class HeadlineSentimentAnalyzer:
    def __init__(self):
        """Initialize sentiment analyzer for headlines"""
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="siebert/sentiment-roberta-large-english",
            truncation=True
        )

        # Keep the same news terms dictionary from the original code
        self.news_terms = {
            # Strong negative terms (-1.0)
            'crash': -1.0,
            'collapse': -1.0,
            'crisis': -1.0,
            'bankruptcy': -1.0,
            'default': -1.0,
            'disaster': -1.0,
            'catastrophe': -1.0,
            'tragedy': -1.0,
            'death': -1.0,
            'fatal': -1.0,
            'war': -1.0,
            'devastating': -1.0,

            # [... Keep all the terms from the original code ...]
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
            'conflict': -0.7,
            'controversy': -0.7,
            'scandal': -0.7,
            'protest': -0.7,
            'lawsuit': -0.7,
            'investigation': -0.7,
            'outbreak': -0.7,
            'shortage': -0.7,
            'violation': -0.7,

            # Mild negative terms (-0.3)
            'dip': -0.3,
            'slip': -0.3,
            'weaken': -0.3,
            'concern': -0.3,
            'volatile': -0.3,
            'uncertainty': -0.3,
            'dispute': -0.3,
            'tension': -0.3,
            'risk': -0.3,
            'warning': -0.3,
            'delay': -0.3,
            'criticism': -0.3,
            'challenge': -0.3,
            'problem': -0.3,

            # Strong positive terms (1.0)
            'surge': 1.0,
            'soar': 1.0,
            'record high': 1.0,
            'breakthrough': 1.0,
            'boom': 1.0,
            'triumph': 1.0,
            'revolutionary': 1.0,
            'milestone': 1.0,
            'victory': 1.0,
            'success': 1.0,
            'achievement': 1.0,

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
            'innovation': 0.7,
            'progress': 0.7,
            'agreement': 0.7,
            'partnership': 0.7,
            'celebration': 0.7,
            'approval': 0.7,
            'discovery': 0.7,
            'improvement': 0.7,

            # Mild positive terms (0.3)
            'rise': 0.3,
            'improve': 0.3,
            'up': 0.3,
            'higher': 0.3,
            'stable': 0.3,
            'support': 0.3,
            'launch': 0.3,
            'expansion': 0.3,
            'development': 0.3,
            'collaboration': 0.3,
            'opportunity': 0.3,

            # Industry terms
            # Automotive (-1.0 to 1.0)
            'recall': -1.0,
            'malfunction': -1.0,
            'defect': -1.0,
            'electric vehicle': 0.7,
            'autonomous': 0.7,
            'fuel-efficient': 0.7,
            'horsepower': 0.3,
            'mileage': 0.3,
            'hybrid': 0.3,

            # Banking (-1.0 to 1.0)
            'default': -1.0,
            'foreclosure': -1.0,
            'fraud': -1.0,
            'debt': -0.7,
            'delinquency': -0.7,
            'overdraft': -0.7,
            'deposit': 0.3,
            'dividend': 0.7,
            'refinance': 0.3,

            # Construction
            'delay': -0.7,
            'overbudget': -0.7,
            'unsafe': -1.0,
            'renovation': 0.3,
            'expansion': 0.7,
            'development': 0.3,

            # Education
            'dropout': -0.7,
            'underperform': -0.7,
            'tuition increase': -0.7,
            'scholarship': 0.7,
            'graduation': 1.0,
            'achievement': 1.0,

            # Energy
            'blackout': -1.0,
            'shortage': -1.0,
            'spill': -1.0,
            'renewable': 0.7,
            'sustainable': 0.7,
            'efficient': 0.7,

            # Fashion
            'outdated': -0.3,
            'unfashionable': -0.3,
            'clearance': -0.3,
            'trending': 0.7,
            'designer': 0.3,
            'exclusive': 0.7,

            # Food and Beverage
            'recall': -1.0,
            'contamination': -1.0,
            'spoilage': -1.0,
            'organic': 0.3,
            'fresh': 0.7,
            'award-winning': 1.0,

            # Healthcare
            'outbreak': -1.0,
            'epidemic': -1.0,
            'malpractice': -1.0,
            'treatment': 0.3,
            'cure': 1.0,
            'breakthrough': 1.0,

            # Information Technology
            'bug': -0.7,
            'vulnerability': -1.0,
            'hack': -1.0,
            'upgrade': 0.7,
            'innovation': 1.0,
            'ai': 0.7,

            # Manufacturing
            'defect': -1.0,
            'shutdown': -1.0,
            'malfunction': -1.0,
            'automation': 0.7,
            'efficiency': 0.7,
            'productivity': 0.7,

            # Media and Entertainment
            'flop': -0.7,
            'cancel': -0.7,
            'controversy': -0.7,
            'blockbuster': 1.0,
            'award': 1.0,
            'hit': 0.7,

            # Real Estate
            'foreclosure': -1.0,
            'bubble': -0.7,
            'vacancy': -0.7,
            'luxury': 0.7,
            'prime location': 1.0,
            'appreciate': 0.7,

            # Retail
            'bankrupt': -1.0,
            'closeout': -0.7,
            'liquidation': -0.7,
            'bestseller': 1.0,
            'expansion': 0.7,
            'exclusive': 0.7,

            # Telecommunications
            'outage': -1.0,
            'disruption': -0.7,
            'interference': -0.7,
            '5g': 0.7,
            'coverage': 0.3,
            'bandwidth': 0.3,

            # Transportation
            'delay': -0.7,
            'accident': -1.0,
            'congestion': -0.7,
            'express': 0.7,
            'on-time': 0.7,
            'efficient': 0.7,

            # Travel and Tourism
            'cancellation': -0.7,
            'overbooked': -0.7,
            'stranded': -1.0,
            'luxury': 1.0,
            'destination': 0.7,
            'resort': 0.7,

            # Utilities
            'outage': -1.0,
            'blackout': -1.0,
            'shortage': -1.0,
            'renewable': 0.7,
            'reliable': 0.7,
            'efficient': 0.7,

            # Wholesale
            'surplus': -0.3,
            'oversupply': -0.7,
            'shortage': -0.7,
            'bulk': 0.3,
            'distributor': 0.3,
            'partnership': 0.7
        }

        # Keep the same magnitude modifiers
        self.magnitude_modifiers = {
            'billion': 1.2,
            'millions': 1.1,
            'thousands': 1.05,
            'massive': 1.3,
            'significant': 1.2,
            'substantial': 1.2,
            'major': 1.2,
            'critical': 1.2,
            'unprecedented': 1.3,
            'historic': 1.25,
            'global': 1.2,
            'worldwide': 1.2,
            'slight': 0.8,
            'minor': 0.7,
            'small': 0.8,
            'limited': 0.7,
            'partial': 0.8,
            'moderate': 0.9,

            # Scale indicators
            'industry-leading': 1.3,
            'market-leading': 1.3,
            'cutting-edge': 1.2,
            'next-generation': 1.2,
            'revolutionary': 1.3,
            'disruptive': 1.2,

            # Market position
            'dominant': 1.2,
            'leading': 1.2,
            'premium': 1.1,
            'budget': 0.8,
            'discount': 0.7,
            'economy': 0.8,

            # Growth/Scale
            'rapid': 1.2,
            'exponential': 1.3,
            'steady': 1.1,
            'gradual': 0.9,
            'incremental': 0.8,

            # Implementation
            'seamless': 1.2,
            'integrated': 1.1,
            'comprehensive': 1.2,
            'partial': 0.8,
            'pilot': 0.9,
            'beta': 0.8,

            # Market response
            'overwhelming': 1.3,
            'strong': 1.2,
            'moderate': 0.9,
            'mixed': 0.8,
            'limited': 0.7,

            # Innovation
            'breakthrough': 1.3,
            'innovative': 1.2,
            'advanced': 1.2,
            'traditional': 0.9,
            'conventional': 0.9,
            'legacy': 0.8
        }

    def analyze_headline(self, headline: str, source: str) -> Dict:
        """Analyze a single headline"""
        base_sentiment = self.sentiment_analyzer(headline)[0]
        term_score = self._analyze_terms(headline.lower())

        # Combine scores (70% term-based, 30% ML-based)
        combined_score = (term_score * 0.7 +
                          (1 if base_sentiment['label'] == 'POSITIVE' else -1) *
                          base_sentiment['score'] * 0.3)

        # Determine sentiment category
        if combined_score > 0.1:
            final_sentiment = 'POSITIVE'
        elif combined_score < -0.1:
            final_sentiment = 'NEGATIVE'
        else:
            final_sentiment = 'NEUTRAL'

        return {
            'headline': headline,
            'source': source,
            'sentiment': final_sentiment,
            'score': combined_score,
            'term_score': term_score,
            'ml_sentiment': base_sentiment['label'],
            'ml_score': base_sentiment['score']
        }

    def _analyze_terms(self, text: str) -> float:
        """Analyze presence and impact of news terms"""
        score = 0
        magnitude = 1.0

        # Apply magnitude modifiers
        for modifier, mod_value in self.magnitude_modifiers.items():
            if modifier in text:
                magnitude *= mod_value

        # Calculate term-based score
        for term, term_score in self.news_terms.items():
            if term in text:
                score += term_score * magnitude

        return score

    def process_csv_files(self, news_csv: str, financial_csv: str) -> None:
        """Process headlines from both CSV files with specific formats"""
        try:
            # Read financial CSV (format: ticker,title,publisher,date,link)
            financial_df = pd.read_csv(financial_csv,
                                       names=['ticker', 'title', 'publisher', 'date', 'link'])

            # Read news CSV (format: company,headline)
            news_df = pd.read_csv(news_csv,
                                  names=['company', 'headline'])

            # Process headlines
            results = []

            # Process financial news (using 'title' column)
            for _, row in financial_df.iterrows():
                analysis = self.analyze_headline(row['title'], 'financial_news')
                analysis['ticker'] = row['ticker']
                analysis['publisher'] = row['publisher']
                analysis['date'] = row['date']
                results.append(analysis)

            # Process general news (using 'headline' column)
            for _, row in news_df.iterrows():
                analysis = self.analyze_headline(row['headline'], 'general_news')
                analysis['company'] = row['company']
                results.append(analysis)

            # Convert results to DataFrame
            results_df = pd.DataFrame(results)

            # Generate summary statistics
            summary_stats = self._generate_summary(results_df)

            # Write results to file
            self._write_results(results_df, summary_stats)

        except FileNotFoundError as e:
            print(f"Error: Could not find CSV file - {str(e)}")
        except pd.errors.EmptyDataError:
            print("Error: One or both CSV files are empty")
        except Exception as e:
            print(f"Error processing CSV files: {str(e)}")
            raise

    def _generate_summary(self, df: pd.DataFrame) -> Dict:
        """Generate summary statistics with additional grouping"""
        summary = {
            'total_headlines': len(df),
            'sentiment_distribution': df.groupby(['source', 'sentiment']).size().to_dict(),
            'average_scores': df.groupby('source')['score'].mean().to_dict(),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # Add financial-specific summary
        financial_news = df[df['source'] == 'financial_news']
        if not financial_news.empty:
            summary['financial'] = {
                'by_ticker': financial_news.groupby('ticker')['score'].mean().to_dict(),
                'by_publisher': financial_news.groupby('publisher')['score'].mean().to_dict(),
                'most_positive': {
                    'headline': financial_news.loc[financial_news['score'].idxmax()]['headline'],
                    'ticker': financial_news.loc[financial_news['score'].idxmax()]['ticker'],
                    'score': financial_news['score'].max()
                },
                'most_negative': {
                    'headline': financial_news.loc[financial_news['score'].idxmin()]['headline'],
                    'ticker': financial_news.loc[financial_news['score'].idxmin()]['ticker'],
                    'score': financial_news['score'].min()
                }
            }

        # Add general news summary
        general_news = df[df['source'] == 'general_news']
        if not general_news.empty:
            summary['general'] = {
                'by_company': general_news.groupby('company')['score'].mean().to_dict(),
                'most_positive': {
                    'headline': general_news.loc[general_news['score'].idxmax()]['headline'],
                    'company': general_news.loc[general_news['score'].idxmax()]['company'],
                    'score': general_news['score'].max()
                },
                'most_negative': {
                    'headline': general_news.loc[general_news['score'].idxmin()]['headline'],
                    'company': general_news.loc[general_news['score'].idxmin()]['company'],
                    'score': general_news['score'].min()
                }
            }

        return summary

    def _write_results(self, results_df: pd.DataFrame, summary: Dict) -> None:
        """Write summary analysis results to file"""
        with open('news_sentiment.txt', 'w', encoding='utf-8') as f:
            # Write header and general summary
            f.write("=== News Sentiment Analysis Summary ===\n\n")
            f.write(f"Analysis Timestamp: {summary['timestamp']}\n")
            f.write(f"Total Headlines Analyzed: {summary['total_headlines']}\n\n")

            # Write sentiment distribution
            f.write("=== Sentiment Distribution ===\n")
            for (source, sentiment), count in sorted(summary['sentiment_distribution'].items()):
                f.write(f"{source} - {sentiment}: {count}\n")

            # Write average sentiment scores
            f.write("\n=== Average Sentiment Scores ===\n")
            for source, score in sorted(summary['average_scores'].items()):
                f.write(f"{source}: {score:.3f}\n")

            # Write financial news summary
            if 'financial' in summary:
                f.write("\n=== Financial News Analysis ===\n")

                f.write("\nBy Ticker (Average Sentiment):\n")
                for ticker, score in sorted(summary['financial']['by_ticker'].items()):
                    f.write(f"{ticker}: {score:.3f}\n")

                f.write("\nBy Publisher (Average Sentiment):\n")
                for publisher, score in sorted(summary['financial']['by_publisher'].items()):
                    f.write(f"{publisher}: {score:.3f}\n")

                f.write("\nMost Positive Financial Headline:\n")
                f.write(f"Ticker: {summary['financial']['most_positive']['ticker']}\n")
                f.write(f"Headline: {summary['financial']['most_positive']['headline']}\n")
                f.write(f"Score: {summary['financial']['most_positive']['score']:.3f}\n")

                f.write("\nMost Negative Financial Headline:\n")
                f.write(f"Ticker: {summary['financial']['most_negative']['ticker']}\n")
                f.write(f"Headline: {summary['financial']['most_negative']['headline']}\n")
                f.write(f"Score: {summary['financial']['most_negative']['score']:.3f}\n")

            # Write general news summary
            if 'general' in summary:
                f.write("\n=== General News Analysis ===\n")

                f.write("\nBy Company (Average Sentiment):\n")
                for company, score in sorted(summary['general']['by_company'].items()):
                    f.write(f"{company}: {score:.3f}\n")

                f.write("\nMost Positive General News Headline:\n")
                f.write(f"Company: {summary['general']['most_positive']['company']}\n")
                f.write(f"Headline: {summary['general']['most_positive']['headline']}\n")
                f.write(f"Score: {summary['general']['most_positive']['score']:.3f}\n")

                f.write("\nMost Negative General News Headline:\n")
                f.write(f"Company: {summary['general']['most_negative']['company']}\n")
                f.write(f"Headline: {summary['general']['most_negative']['headline']}\n")
                f.write(f"Score: {summary['general']['most_negative']['score']:.3f}\n")


if __name__ == "__main__":
    # Initialize analyzer
    analyzer = HeadlineSentimentAnalyzer()

    # Process CSV files
    try:
        analyzer.process_csv_files(
            news_csv='../general_news.csv',
            financial_csv='../financial_news.csv'
        )
        print("Analysis complete. Results written to news_sentiment.txt")
    except Exception as e:
        print(f"Error: {str(e)}")