"""
Kalshi API Client
Fetches market data from Kalshi's API
"""
import requests
from typing import List, Dict, Optional


class KalshiClient:
    """Client for interacting with Kalshi API"""
    
    # Configuration constants
    MAX_EVENTS = 20  # Maximum number of events to fetch
    PRICE_DIVISOR = 100  # Kalshi prices are in cents, divide by 100 for dollars
    
    def __init__(self):
        self.base_url = "https://api.elections.kalshi.com/trade-api/v2"
        
    def get_markets(self) -> List[Dict]:
        """
        Fetch active markets from Kalshi
        
        Returns:
            List of market dictionaries with standardized format
        """
        try:
            # Get active events
            response = requests.get(
                f"{self.base_url}/events",
                params={"status": "open", "limit": 100},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            events = data.get('events', [])
            
            # Get markets for each event
            standardized_markets = []
            for event in events[:self.MAX_EVENTS]:  # Limit events using constant
                try:
                    event_ticker = event.get('event_ticker', '')
                    if not event_ticker:
                        continue
                    
                    # Get markets for this event
                    markets_response = requests.get(
                        f"{self.base_url}/markets",
                        params={"event_ticker": event_ticker, "status": "open"},
                        timeout=10
                    )
                    markets_response.raise_for_status()
                    markets_data = markets_response.json()
                    
                    markets = markets_data.get('markets', [])
                    for market in markets:
                        standardized_market = self._standardize_market(market, event)
                        if standardized_market:
                            standardized_markets.append(standardized_market)
                            
                except Exception as e:
                    print(f"Error fetching markets for event: {e}")
                    continue
            
            return standardized_markets
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Kalshi data: {e}")
            return []
    
    def _standardize_market(self, market: Dict, event: Dict) -> Optional[Dict]:
        """
        Convert Kalshi data to standardized format
        
        Args:
            market: Raw market data from Kalshi
            event: Event data associated with the market
            
        Returns:
            Standardized market dictionary
        """
        try:
            # Extract market data
            ticker = market.get('ticker', '')
            title = market.get('title', event.get('title', ''))
            
            if not title:
                return None
            
            # Get yes/no prices
            yes_bid = market.get('yes_bid', 0)
            yes_ask = market.get('yes_ask', 0)
            no_bid = market.get('no_bid', 0)
            no_ask = market.get('no_ask', 0)
            
            # Use mid prices (average of bid and ask)
            # Kalshi prices are in cents, divide by PRICE_DIVISOR to get dollar amounts
            yes_price = (yes_bid + yes_ask) / 2 / self.PRICE_DIVISOR if (yes_bid + yes_ask) > 0 else 0
            no_price = (no_bid + no_ask) / 2 / self.PRICE_DIVISOR if (no_bid + no_ask) > 0 else 0
            
            # Ensure prices sum to ~1 for arbitrage calculations
            if yes_price == 0 and no_price == 0:
                return None
            
            if yes_price == 0:
                yes_price = 1 - no_price
            if no_price == 0:
                no_price = 1 - yes_price
            
            return {
                'source': 'Kalshi',
                'market_id': ticker,
                'question': title,
                'yes_price': yes_price,
                'no_price': no_price,
                'volume': float(market.get('volume', 0)),
                'end_date': market.get('close_time', ''),
                'description': event.get('category', '')
            }
        except Exception as e:
            print(f"Error in _standardize_market: {e}")
            return None
