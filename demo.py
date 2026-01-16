"""
Demo script to test arbitrage detection with mock data
This demonstrates the system functionality with simulated market data
"""
from polymarket_client import PolymarketClient
from kalshi_client import KalshiClient
from market_matcher import MarketMatcher
from arbitrage_detector import ArbitrageDetector


def create_mock_polymarket_data():
    """Create mock Polymarket market data"""
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


def create_mock_kalshi_data():
    """Create mock Kalshi market data with arbitrage opportunities"""
    return [
        {
            'source': 'Kalshi',
            'market_id': 'KALSHI-PRES-2024',
            'question': 'Will Democrats win the 2024 Presidential Election',
            'yes_price': 0.46,  # Lower than Polymarket - arbitrage opportunity!
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
            'yes_price': 0.55,  # Higher than Polymarket - arbitrage opportunity!
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


def main():
    """Run the demo"""
    print("=" * 70)
    print("ARBITRAGE DETECTION DEMO - Using Mock Data")
    print("=" * 70)
    print()
    
    # Create mock data
    print("Creating mock market data...")
    polymarket_markets = create_mock_polymarket_data()
    kalshi_markets = create_mock_kalshi_data()
    
    print(f"✓ Created {len(polymarket_markets)} Polymarket markets")
    print(f"✓ Created {len(kalshi_markets)} Kalshi markets")
    print()
    
    # Initialize matcher and detector
    matcher = MarketMatcher(similarity_threshold=0.6)
    detector = ArbitrageDetector(min_profit_threshold=0.01)
    
    # Match markets
    print("Matching markets across platforms...")
    matched_markets = matcher.match_markets(polymarket_markets, kalshi_markets)
    print(f"✓ Found {len(matched_markets)} matched market pairs")
    print()
    
    # Display matches
    print("Matched Markets:")
    print("-" * 70)
    for pm, kalshi, score in matched_markets:
        print(f"Similarity: {score:.1%}")
        print(f"  Polymarket: {pm['question'][:60]}")
        print(f"  Kalshi:     {kalshi['question'][:60]}")
        print()
    
    # Detect arbitrage
    print("Detecting arbitrage opportunities...")
    opportunities = detector.detect_arbitrage(matched_markets)
    print(f"✓ Found {len(opportunities)} arbitrage opportunities")
    print()
    
    # Display opportunities
    if opportunities:
        print("=" * 70)
        print("ARBITRAGE OPPORTUNITIES")
        print("=" * 70)
        print()
        
        for i, opp in enumerate(opportunities, 1):
            print(f"{i}. {opp['question']}")
            print(f"   Strategy: {opp['strategy']}")
            print(f"   Total Cost: ${opp['total_cost']:.4f}")
            print(f"   Guaranteed Profit: ${opp['potential_profit']:.4f}")
            print(f"   Profit Percentage: {opp['profit_percentage']*100:.2f}%")
            print(f"   Similarity Score: {opp['similarity_score']*100:.1f}%")
            print()
            print(f"   Market 1 ({opp['market1']['source']}): {opp['market1']['market_id']}")
            print(f"     Yes: ${opp['market1']['yes_price']:.4f}, No: ${opp['market1']['no_price']:.4f}")
            print()
            print(f"   Market 2 ({opp['market2']['source']}): {opp['market2']['market_id']}")
            print(f"     Yes: ${opp['market2']['yes_price']:.4f}, No: ${opp['market2']['no_price']:.4f}")
            print()
            print("-" * 70)
            print()
    else:
        print("No arbitrage opportunities found with current threshold.")
    
    print("=" * 70)
    print("Demo completed!")
    print("=" * 70)


if __name__ == '__main__':
    main()
