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
from datetime import datetime

app = Flask(__name__)

# Initialize clients
polymarket_client = PolymarketClient()
kalshi_client = KalshiClient()
market_matcher = MarketMatcher(similarity_threshold=0.6)
arbitrage_detector = ArbitrageDetector(min_profit_threshold=0.01)

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


if __name__ == '__main__':
    # Update opportunities on startup
    print("Starting Arbitrage Detection System...")
    update_opportunities()
    
    # Start Flask app
    print("Starting web server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
