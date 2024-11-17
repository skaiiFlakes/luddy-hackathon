import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np
from datetime import datetime, timedelta


class IndustryAnalyzer:
    def __init__(self, industry_tickers, lookback_period=365):
        self.industry_tickers = industry_tickers
        self.lookback_period = lookback_period
        self.rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()

    def fetch_financial_data(self):
        """Fetch financial data and metrics for industry analysis"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=self.lookback_period)

        industry_data = {}
        for ticker in self.industry_tickers:
            stock = yf.Ticker(ticker)

            # Get financial ratios and metrics
            try:
                financials = stock.financials
                info = stock.info

                # Calculate key metrics
                industry_data[ticker] = {
                    'revenue_growth': self._calculate_growth(financials.loc['Total Revenue']),
                    'profit_margin': info.get('profitMargins', 0),
                    'operating_margin': info.get('operatingMargins', 0),
                    'roa': info.get('returnOnAssets', 0),
                    'current_ratio': info.get('currentRatio', 0),
                    'debt_to_equity': info.get('debtToEquity', 0),
                    'market_cap': info.get('marketCap', 0),
                }
            except:
                continue

        return pd.DataFrame(industry_data).T

    def _calculate_growth(self, series):
        """Calculate year-over-year growth rate"""
        if len(series) >= 2:
            return (series.iloc[0] - series.iloc[1]) / series.iloc[1]
        return 0

    def classify_performance(self, data):
        """Classify companies based on their performance metrics"""
        # Create performance labels based on revenue growth and profitability
        data['performance_label'] = pd.qcut(
            data['revenue_growth'] * data['profit_margin'],
            q=3,
            labels=['Struggling', 'Stable', 'High-Performing']
        )

        # Prepare features for classification
        features = ['revenue_growth', 'profit_margin', 'operating_margin', 'roa',
                    'current_ratio', 'debt_to_equity']
        X = data[features]
        y = data['performance_label']

        # Train classifier
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        X_train_scaled = self.scaler.fit_transform(X_train)
        self.rf_classifier.fit(X_train_scaled, y_train)

        return self.rf_classifier, self.scaler

    def generate_analysis_text(self, company_metrics):
        """Generate structured text analysis based on company metrics and industry context"""
        # Scale the input metrics
        scaled_metrics = self.scaler.transform([company_metrics])
        performance_class = self.rf_classifier.predict(scaled_metrics)[0]

        # Get feature importance
        feature_importance = dict(zip(
            ['revenue_growth', 'profit_margin', 'operating_margin', 'roa',
             'current_ratio', 'debt_to_equity'],
            self.rf_classifier.feature_importances_
        ))

        # Generate structured analysis text
        analysis = f"""
INDUSTRY ANALYSIS AND RECOMMENDATIONS
===================================

Performance Classification: {performance_class}

Key Metrics Summary:
------------------
- Revenue Growth: {company_metrics[0]:.2%}
- Profit Margin: {company_metrics[1]:.2%}
- Operating Margin: {company_metrics[2]:.2%}
- Return on Assets: {company_metrics[3]:.2%}
- Current Ratio: {company_metrics[4]:.2f}
- Debt to Equity: {company_metrics[5]:.2f}

Critical Areas (Based on Feature Importance):
------------------------------------------
{self._format_feature_importance(feature_importance)}

Market Position:
--------------
{self._generate_market_position(company_metrics, performance_class)}

Industry Context:
---------------
{self._generate_industry_context(company_metrics)}
"""
        return analysis

    def _format_feature_importance(self, feature_importance):
        """Format feature importance for text output"""
        sorted_features = sorted(
            feature_importance.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return '\n'.join([
            f"- {feature[0].replace('_', ' ').title()}: {feature[1]:.3f} importance score"
            for feature in sorted_features
        ])

    def _generate_market_position(self, metrics, performance_class):
        """Generate market position analysis"""
        if performance_class == 'High-Performing':
            return "Company shows strong market positioning with above-average metrics."
        elif performance_class == 'Stable':
            return "Company maintains stable market position with room for optimization."
        else:
            return "Company faces significant challenges requiring immediate attention."

    def _generate_industry_context(self, metrics):
        """Generate industry context analysis"""
        industry_data = self.fetch_financial_data()
        avg_revenue_growth = industry_data['revenue_growth'].mean()
        avg_profit_margin = industry_data['profit_margin'].mean()

        return f"""Industry averages:
- Revenue Growth: {avg_revenue_growth:.2%}
- Profit Margin: {avg_profit_margin:.2%}
Company performance relative to industry benchmarks can inform strategic decisions."""


def process_tickers(tickers: list[str] = [], industry: str = "") -> None:
    # Initialize analyzer
    analyzer = IndustryAnalyzer(tickers)

    # Fetch and prepare data
    industry_data = analyzer.fetch_financial_data()

    # Train classifier
    try:
        classifier, scaler = analyzer.classify_performance(industry_data)
    except KeyError as e:
        print(f"KeyError: {e}. Some required columns are missing in the data.")
        classifier, scaler = None, None

    # Open file for writing
    with open(f"{industry}_financial_analysis.txt", 'w', encoding='utf-8') as file:
        # Generate analysis text for each company
        for ticker in tickers:
            stock = yf.Ticker(ticker)
            info = stock.info
            try:
                company_metrics = [
                    industry_data.loc[ticker, 'revenue_growth'],
                    industry_data.loc[ticker, 'profit_margin'],
                    industry_data.loc[ticker, 'operating_margin'],
                    industry_data.loc[ticker, 'roa'],
                    industry_data.loc[ticker, 'current_ratio'],
                    industry_data.loc[ticker, 'debt_to_equity']
                ]
                if classifier and scaler:
                    scaled_metrics = scaler.transform([company_metrics])
                    performance_class = classifier.predict(scaled_metrics)[0]
                else:
                    performance_class = "Unknown"
            except KeyError as e:
                print(f"KeyError: {e}. Skipping ticker {ticker} due to missing data.")
                performance_class = "Unknown"
                company_metrics = [0, 0, 0, 0, 0, 0]

            analysis_text = analyzer.generate_analysis_text(company_metrics)
            file.write(f"Analysis for {info.get('longName', ticker)} ({ticker}):\n{analysis_text}\n")
            file.write(f"Predicted Performance Class: {performance_class}\n\n")


if __name__ == "__main__":
    # Example tickers for software industry
    industry_tickers = [
        # ['Automotive', ['TSLA', 'TM', 'F', 'GM', 'STLA']],
        # ['Banking', ['JPM', 'BAC', 'WFC', 'C', 'GS']],
        # ['Construction', ['CAT', 'DE', 'VMC', 'MLM', 'URI']],
        # ['Education', ['CHGG', 'LRN', 'STR', 'BFAM']],
        # ['Energy', ['XOM', 'CVX', 'COP', 'SLB', 'EOG']],
        # ['Fashion', ['LULU', 'NKE', 'TPR', 'RL', 'VFC']],
        # ['Food and Beverage', ['KO', 'PEP', 'MDLZ', 'KHC', 'HSY']],
        # ['Healthcare', ['JNJ', 'UNH', 'LLY', 'PFE', 'ABT']],
        # ['Information Technology', ['AAPL', 'MSFT', 'NVDA', 'ORCL', 'CRM']],
        # ['Manufacturing', ['HON', 'MMM', 'GE', 'ITW', 'EMR']],
        # ['Media and Entertainment', ['DIS', 'NFLX', 'CMCSA', 'PARA', 'WBD']],
        # ['Real Estate', ['PLD', 'AMT', 'EQIX', 'CCI', 'PSA']],
        # ['Retail', ['WMT', 'COST', 'TGT', 'HD', 'AMZN']],
        # ['Telecommunications', ['VZ', 'T', 'TMUS', 'TEF', 'AMX']],
        # ['Transportation', ['UNP', 'UPS', 'CSX', 'FDX', 'NSC']],
        ['Travel and Tourism', ['MAR', 'HLT', 'CCL', 'RCL', 'BKNG']],
        ['Utilities', ['NEE', 'DUK', 'SO', 'AEP', 'XEL']],
        ['Wholesale', ['PFGC', 'UNFI', 'CHEF', 'SPTN']],
        ['Not Specified', ['SPY', 'QQQ', 'DIA', 'IWM', 'VTI']]  # Using major ETFs for non-specified
    ]

    for industry, tickers in industry_tickers:
        process_tickers(tickers, industry)