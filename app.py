"""
Flask Web Application for Arbitrage Detection
Provides API endpoints and serves the dashboard UI
"""
from flask import Flask, render_template, jsonify
from polymarket_client import PolymarketClient
from kalshi_client import KalshiClient
from market_matcher import MarketMatcher
from arbitrage_detector import ArbitrageDetector
import time
import os
from datetime import datetime

app = Flask(__name__)

# Initialize clients
polymarket_client = PolymarketClient()
kalshi_client = KalshiClient()
market_matcher = MarketMatcher(similarity_threshold=0.6)
arbitrage_detector = ArbitrageDetector(min_profit_threshold=0.01)

# Use demo mode if environment variable is set
USE_DEMO_DATA = os.environ.get('USE_DEMO_DATA', 'false').lower() == 'true'

# Cache for market data
cache = {
    'opportunities': [],
    'last_updated': None,
    'polymarket_count': 0,
    'kalshi_count': 0,
    'matched_count': 0
}


@app.route('/')
def index():
    """Serve the dashboard UI"""
    return render_template('index.html')


@app.route('/api/opportunities')
def get_opportunities():
    """
    API endpoint to get current arbitrage opportunities
    
    Returns:
        JSON response with opportunities and metadata
    """
    return jsonify({
        'opportunities': cache['opportunities'],
        'last_updated': cache['last_updated'],
        'stats': {
            'polymarket_markets': cache['polymarket_count'],
            'kalshi_markets': cache['kalshi_count'],
            'matched_markets': cache['matched_count'],
            'arbitrage_opportunities': len(cache['opportunities'])
        }
    })


@app.route('/api/refresh')
def refresh_data():
    """
    API endpoint to manually refresh market data
    
    Returns:
        JSON response with updated opportunities
    """
    update_opportunities()
    return jsonify({
        'success': True,
        'message': 'Data refreshed successfully',
        'opportunities_count': len(cache['opportunities'])
    })


def update_opportunities():
    """
    Fetch market data and detect arbitrage opportunities
    Updates the global cache with results
    """
    print("Fetching market data...")
    start_time = time.time()
    
    # Fetch markets from both platforms
    if USE_DEMO_DATA:
        print("Using demo data...")
        polymarket_markets = get_demo_polymarket_data()
        kalshi_markets = get_demo_kalshi_data()
    else:
        print("Fetching Polymarket markets...")
        polymarket_markets = polymarket_client.get_markets()
        print(f"Found {len(polymarket_markets)} Polymarket markets")
        
        print("Fetching Kalshi markets...")
        kalshi_markets = kalshi_client.get_markets()
        print(f"Found {len(kalshi_markets)} Kalshi markets")
    
    # Match markets
    print("Matching markets...")
    matched_markets = market_matcher.match_markets(polymarket_markets, kalshi_markets)
    print(f"Matched {len(matched_markets)} markets")
    
    # Detect arbitrage opportunities
    print("Detecting arbitrage opportunities...")
    opportunities = arbitrage_detector.detect_arbitrage(matched_markets)
    print(f"Found {len(opportunities)} arbitrage opportunities")
    
    # Update cache
    cache['opportunities'] = opportunities
    cache['last_updated'] = datetime.now().isoformat()
    cache['polymarket_count'] = len(polymarket_markets)
    cache['kalshi_count'] = len(kalshi_markets)
    cache['matched_count'] = len(matched_markets)
    
    elapsed_time = time.time() - start_time
    print(f"Update completed in {elapsed_time:.2f} seconds")


def get_demo_polymarket_data():
    """Create demo Polymarket market data"""
    return [
        {
            'source': 'Polymarket',
            'market_id': 'PM-2024-ELECTION-001',
            'question': 'Will the Democrats win the 2024 Presidential Election?',
            'yes_price': 0.52,
            'no_price': 0.48,
            'volume': 15000000,
            'end_date': '2024-11-05T00:00:00Z',
            'description': 'Presidential election outcome'
        },
        {
            'source': 'Polymarket',
            'market_id': 'PM-FED-RATE-002',
            'question': 'Will the Federal Reserve raise interest rates in March 2024?',
            'yes_price': 0.35,
            'no_price': 0.65,
            'volume': 5000000,
            'end_date': '2024-03-20T00:00:00Z',
            'description': 'Federal Reserve policy decision'
        },
        {
            'source': 'Polymarket',
            'market_id': 'PM-CRYPTO-BTC-003',
            'question': 'Will Bitcoin reach $100,000 by end of 2024?',
            'yes_price': 0.42,
            'no_price': 0.58,
            'volume': 8000000,
            'end_date': '2024-12-31T23:59:59Z',
            'description': 'Bitcoin price prediction'
        },
        {
            'source': 'Polymarket',
            'market_id': 'PM-SPORTS-SB-004',
            'question': 'Will the Kansas City Chiefs win the Super Bowl?',
            'yes_price': 0.28,
            'no_price': 0.72,
            'volume': 3000000,
            'end_date': '2024-02-11T00:00:00Z',
            'description': 'Super Bowl winner'
        }
    ]


def get_demo_kalshi_data():
    """Create demo Kalshi market data with arbitrage opportunities"""
    return [
        {
            'source': 'Kalshi',
            'market_id': 'KALSHI-PRES-2024',
            'question': 'Will Democrats win the 2024 Presidential Election',
            'yes_price': 0.46,
            'no_price': 0.54,
            'volume': 12000000,
            'end_date': '2024-11-05T00:00:00Z',
            'description': 'Politics'
        },
        {
            'source': 'Kalshi',
            'market_id': 'KALSHI-FED-MARCH',
            'question': 'Federal Reserve rate increase in March 2024',
            'yes_price': 0.38,
            'no_price': 0.62,
            'volume': 4000000,
            'end_date': '2024-03-20T00:00:00Z',
            'description': 'Finance'
        },
        {
            'source': 'Kalshi',
            'market_id': 'KALSHI-BTC-100K',
            'question': 'Bitcoin to reach $100000 by end of 2024',
            'yes_price': 0.55,
            'no_price': 0.45,
            'volume': 6000000,
            'end_date': '2024-12-31T23:59:59Z',
            'description': 'Crypto'
        },
        {
            'source': 'Kalshi',
            'market_id': 'KALSHI-NFL-KC',
            'question': 'Kansas City Chiefs Super Bowl win',
            'yes_price': 0.30,
            'no_price': 0.70,
            'volume': 2500000,
            'end_date': '2024-02-11T00:00:00Z',
            'description': 'Sports'
        }
    ]


if __name__ == '__main__':
    # Update opportunities on startup
    print("Starting Arbitrage Detection System...")
    update_opportunities()
    
    # Start Flask app
    print("Starting web server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
