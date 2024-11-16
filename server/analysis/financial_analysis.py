import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Global settings
LOOKBACK_PERIOD = '2y'

def get_sector_tickers(sector):
    """Get list of stock tickers for a given sector"""
    sector_tickers = {
           'Automotive': ['TSLA', 'F', 'GM', 'TM', 'VWAGY'],
            'Information Technology': ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA'],
            'Banking': ['JPM', 'BAC', 'GS', 'MS', 'WFC'],
            'Construction': ['X', 'VMC', 'FLR', 'NVR', 'C'],
            'Education': ['EDU', 'APOL', 'STRM', 'LOPE', 'CECO'],
            'Energy': ['XOM', 'CVX', 'COP', 'SLB', 'OXY'],
            'Fashion': ['LVMUY', 'GUESS', 'UAA', 'NKE', 'RL'],
            'Food and Beverage': ['KO', 'PEP', 'MCD', 'PG', 'GIS'],
            'Healthcare': ['JNJ', 'PFE', 'MRK', 'ABBV', 'GILD'],
            'Manufacturing': ['CAT', 'DE', 'HON', 'GE', '3M'],
            'Media and Entertainment': ['DIS', 'NFLX', 'COMS', 'CMCSA', 'VIAC'],
            'Real Estate': ['SPG', 'PLD', 'AMT', 'O', 'DLR'],
            'Retail': ['WMT', 'AMZN', 'TGT', 'M', 'BBY'],
            'Telecommunications': ['VZ', 'T', 'CMCSA', 'DISH', 'LUMN'],
            'Transportation': ['DAL', 'UAL', 'LUV', 'AAL', 'CSX'],
            'Travel and Tourism': ['EXPE', 'TRIP', 'MAR', 'HOT', 'LYV'],
            'Utilities': ['DUK', 'NEE', 'SO', 'AEP', 'XEL'],
            'Wholesale': ['COST', 'WMT', 'M', 'SYY', 'BJS'],
            'Not Specified': ['SPY', 'VTI', 'VOO', 'IVV', 'QQQ']
    }
    return sector_tickers.get(sector, [])

def calculate_growth_metrics(ticker_data):
    """Calculate growth metrics from financial data"""
    try:
        # Get historical data
        stock_data = ticker_data.history(period=LOOKBACK_PERIOD)
        
        # Calculate price growth
        if len(stock_data) > 0:
            price_growth = ((stock_data['Close'][-1] / stock_data['Close'][0]) - 1) * 100
        else:
            price_growth = 0
            
        # Get financial metrics
        try:
            financials = ticker_data.financials
            if not financials.empty:
                revenue_growth = ((financials.iloc[0, 0] / financials.iloc[0, -1]) - 1) * 100
            else:
                revenue_growth = 0
        except:
            revenue_growth = 0
            
        return price_growth, revenue_growth
    except Exception as e:
        print(f"Error calculating metrics: {str(e)}")
        return 0, 0

def get_stock_data(sector):
    """Get financial data for companies in a sector"""
    tickers = get_sector_tickers(sector)
    data = []
    
    print(f"Analyzing {len(tickers)} companies in {sector} sector...")
    
    for ticker in tickers:
        try:
            print(f"Processing {ticker}...")
            stock = yf.Ticker(ticker)
            price_growth, revenue_growth = calculate_growth_metrics(stock)
            
            info = stock.info
            data.append({
                'Company': info.get('longName', ticker),
                'Ticker': ticker,
                'Sector': sector,
                'Revenue Growth': revenue_growth,
                'Stock Price Growth': price_growth,
                'Market Cap': info.get('marketCap', 0),
                'Employees': info.get('fullTimeEmployees', 0)
            })
        except Exception as e:
            print(f"Error processing {ticker}: {str(e)}")
            continue
    
    return pd.DataFrame(data)

def analyze_sector(sector='Information Technology'):
    """Analyze a sector and make predictions"""
    # Get data
    print(f"\nFetching data for {sector} sector...")
    df = get_stock_data(sector)
    
    if len(df) < 3:
        print("Not enough companies found for reliable analysis")
        return
    
    print(f"\nAnalyzing {len(df)} companies...")
    
    # Prepare features
    feature_columns = ['Revenue Growth', 'Stock Price Growth', 'Market Cap', 'Employees']
    
    # Preprocess data
    for col in feature_columns:
        df[col] = df[col].fillna(df[col].median())
    
    df['Market Cap'] = np.log1p(df['Market Cap'])
    df['Employees'] = np.log1p(df['Employees'])
    df['Growth Score'] = (df['Revenue Growth'] + df['Stock Price Growth']) / 2
    
    # Prepare for training
    X = df[feature_columns]
    growth_threshold = df['Growth Score'].quantile(0.7)
    y = df['Growth Score'] > growth_threshold
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Print results
    print("\nCompany Analysis:")
    for _, row in df.iterrows():
        print(f"\n{row['Company']} ({row['Ticker']}):")
        print(f"Revenue Growth: {row['Revenue Growth']:.1f}%")
        print(f"Stock Price Growth: {row['Stock Price Growth']:.1f}%")
        print(f"Market Cap: ${row['Market Cap']:,.0f}")
        print(f"Growth Category: {'High Growth' if row['Growth Score'] > growth_threshold else 'Standard Growth'}")
    
    return model, feature_columns, df

def main():
    # Select sector to analyze
    sector = 'Information Technology'  # Change this to analyze different sectors
    
    # Analyze sector
    model, features, data = analyze_sector(sector)
    
    # Example prediction
    print("\nExample prediction for a new company:")
    new_company = pd.DataFrame({
        'Revenue Growth': [15.0],
        'Stock Price Growth': [20.0],
        'Market Cap': [1e9],
        'Employees': [1000]
    })
    
    # Preprocess new company data
    new_company['Market Cap'] = np.log1p(new_company['Market Cap'])
    new_company['Employees'] = np.log1p(new_company['Employees'])
    
    # Make prediction
    prediction = model.predict(new_company[features])
    print(f"Growth prediction: {'High Growth' if prediction[0] else 'Standard Growth'}")

if __name__ == "__main__":
    main()