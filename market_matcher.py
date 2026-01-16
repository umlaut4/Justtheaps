"""
Market Matcher
Matches markets between Polymarket and Kalshi based on similarity
"""
from typing import List, Dict, Tuple
from difflib import SequenceMatcher


class MarketMatcher:
    """Matches markets across different platforms"""
    
    def __init__(self, similarity_threshold: float = 0.6):
        """
        Initialize the market matcher
        
        Args:
            similarity_threshold: Minimum similarity score (0-1) to consider a match
        """
        self.similarity_threshold = similarity_threshold
    
    def match_markets(self, polymarket_markets: List[Dict], 
                     kalshi_markets: List[Dict]) -> List[Tuple[Dict, Dict]]:
        """
        Match markets between Polymarket and Kalshi
        
        Args:
            polymarket_markets: List of Polymarket markets
            kalshi_markets: List of Kalshi markets
            
        Returns:
            List of tuples containing matched market pairs (polymarket, kalshi)
        """
        matches = []
        
        for pm_market in polymarket_markets:
            best_match = None
            best_score = 0
            
            pm_question = self._normalize_text(pm_market.get('question', ''))
            
            for kalshi_market in kalshi_markets:
                kalshi_question = self._normalize_text(kalshi_market.get('question', ''))
                
                # Calculate similarity score
                score = self._calculate_similarity(pm_question, kalshi_question)
                
                if score > best_score and score >= self.similarity_threshold:
                    best_score = score
                    best_match = kalshi_market
            
            if best_match:
                matches.append((pm_market, best_match, best_score))
        
        return matches
    
    def _normalize_text(self, text: str) -> str:
        """
        Normalize text for comparison
        
        Args:
            text: Input text
            
        Returns:
            Normalized text
        """
        # Convert to lowercase and remove extra whitespace
        text = text.lower().strip()
        
        # Remove common punctuation
        for char in ['?', '!', '.', ',', ';', ':', '"', "'"]:
            text = text.replace(char, '')
        
        return text
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two texts
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score between 0 and 1
        """
        # Use SequenceMatcher for basic similarity
        return SequenceMatcher(None, text1, text2).ratio()
