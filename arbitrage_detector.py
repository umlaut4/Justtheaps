"""
Arbitrage Detector
Identifies arbitrage opportunities between matched markets
"""
from typing import List, Dict, Tuple


class ArbitrageDetector:
    """Detects arbitrage opportunities between matched markets"""
    
    def __init__(self, min_profit_threshold: float = 0.01):
        """
        Initialize the arbitrage detector
        
        Args:
            min_profit_threshold: Minimum profit percentage to report (0.01 = 1%)
        """
        self.min_profit_threshold = min_profit_threshold
    
    def detect_arbitrage(self, matched_markets: List[Tuple[Dict, Dict, float]]) -> List[Dict]:
        """
        Detect arbitrage opportunities from matched markets
        
        Args:
            matched_markets: List of tuples (polymarket, kalshi, similarity_score)
            
        Returns:
            List of arbitrage opportunities with details
        """
        opportunities = []
        
        for pm_market, kalshi_market, similarity in matched_markets:
            # Get prices from both markets
            pm_yes = pm_market.get('yes_price', 0)
            pm_no = pm_market.get('no_price', 0)
            kalshi_yes = kalshi_market.get('yes_price', 0)
            kalshi_no = kalshi_market.get('no_price', 0)
            
            # Skip if any price is missing or invalid
            if not all([pm_yes, pm_no, kalshi_yes, kalshi_no]):
                continue
            
            # Check for arbitrage opportunities
            # Opportunity 1: Buy Yes on PM, Buy No on Kalshi
            opportunity_1 = self._calculate_opportunity(
                pm_yes, kalshi_no, pm_market, kalshi_market,
                "Buy YES on Polymarket, Buy NO on Kalshi",
                similarity
            )
            
            # Opportunity 2: Buy No on PM, Buy Yes on Kalshi
            opportunity_2 = self._calculate_opportunity(
                pm_no, kalshi_yes, pm_market, kalshi_market,
                "Buy NO on Polymarket, Buy YES on Kalshi",
                similarity
            )
            
            # Add opportunities if they meet the profit threshold
            if opportunity_1 and opportunity_1['profit_percentage'] >= self.min_profit_threshold:
                opportunities.append(opportunity_1)
            
            if opportunity_2 and opportunity_2['profit_percentage'] >= self.min_profit_threshold:
                opportunities.append(opportunity_2)
        
        # Sort by profit percentage (highest first)
        opportunities.sort(key=lambda x: x['profit_percentage'], reverse=True)
        
        return opportunities
    
    def _calculate_opportunity(self, price1: float, price2: float, 
                               market1: Dict, market2: Dict,
                               strategy: str, similarity: float) -> Dict:
        """
        Calculate if there's an arbitrage opportunity
        
        Args:
            price1: Price on first market
            price2: Price on second market
            market1: First market data
            market2: Second market data
            strategy: Description of the trading strategy
            similarity: Similarity score between markets
            
        Returns:
            Dictionary with opportunity details or None
        """
        # Total cost to buy both outcomes
        total_cost = price1 + price2
        
        # Profit if both outcomes pay $1
        payout = 1.0
        profit = payout - total_cost
        profit_percentage = profit / total_cost if total_cost > 0 else 0
        
        # Only return if there's a profit
        if profit <= 0:
            return None
        
        return {
            'market1': market1,
            'market2': market2,
            'strategy': strategy,
            'total_cost': round(total_cost, 4),
            'potential_profit': round(profit, 4),
            'profit_percentage': round(profit_percentage, 4),
            'similarity_score': round(similarity, 4),
            'question': market1.get('question', 'Unknown')
        }
