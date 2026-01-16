"""
Polymarket API Client
Fetches market data from Polymarket's API
"""
import requests
from typing import List, Dict, Optional


class PolymarketClient:
    """Client for interacting with Polymarket API"""
    
    def __init__(self):
        self.base_url = "https://clob.polymarket.com"
        self.gamma_url = "https://gamma-api.polymarket.com"
        
    def get_markets(self) -> List[Dict]:
        """
        Fetch active markets from Polymarket
        
        Returns:
            List of market dictionaries with standardized format
        """
        try:
            # Get active markets
            response = requests.get(
                f"{self.gamma_url}/markets",
                params={"active": "true", "closed": "false"},
                timeout=10
            )
            response.raise_for_status()
            markets = response.json()
            
            # Standardize the market data format
            standardized_markets = []
            for market in markets[:50]:  # Limit to first 50 markets
                try:
                    standardized_market = self._standardize_market(market)
                    if standardized_market:
                        standardized_markets.append(standardized_market)
                except Exception as e:
                    print(f"Error standardizing market: {e}")
                    continue
                    
            return standardized_markets
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Polymarket data: {e}")
            return []
    
    def _standardize_market(self, market: Dict) -> Optional[Dict]:
        """
        Convert Polymarket data to standardized format
        
        Args:
            market: Raw market data from Polymarket
            
        Returns:
            Standardized market dictionary
        """
        try:
            # Extract the relevant data
            question = market.get('question', '')
            if not question:
                return None
                
            # Get outcome prices (probabilities)
            outcomes = market.get('outcomes', [])
            if not outcomes or len(outcomes) < 2:
                return None
            
            # Typically binary markets have Yes/No outcomes
            yes_price = None
            no_price = None
            
            for outcome in outcomes:
                outcome_name = outcome.get('outcome', '').lower()
                price = float(outcome.get('price', 0))
                
                if 'yes' in outcome_name:
                    yes_price = price
                elif 'no' in outcome_name:
                    no_price = price
            
            if yes_price is None or no_price is None:
                # If not explicitly Yes/No, use first two outcomes
                if len(outcomes) >= 2:
                    yes_price = float(outcomes[0].get('price', 0))
                    no_price = float(outcomes[1].get('price', 0))
            
            return {
                'source': 'Polymarket',
                'market_id': market.get('id', market.get('condition_id', '')),
                'question': question,
                'yes_price': yes_price,
                'no_price': no_price,
                'volume': float(market.get('volume', 0)),
                'end_date': market.get('end_date_iso', ''),
                'description': market.get('description', '')
            }
        except Exception as e:
            print(f"Error in _standardize_market: {e}")
            return None
