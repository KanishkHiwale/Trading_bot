"""
Order placement and management logic
"""
from typing import Dict, Any, Optional
import logging
from .client import BinanceFuturesClient

logger = logging.getLogger(__name__)


class OrderManager:
    """Manages order placement and validation"""
    
    def __init__(self, client: BinanceFuturesClient):
        """
        Initialize OrderManager
        
        Args:
            client: BinanceFuturesClient instance
        """
        self.client = client
        
    def place_market_order(self, symbol: str, side: str, quantity: float) -> Dict[str, Any]:
        """
        Place a market order
        
        Args:
            symbol: Trading pair symbol
            side: Order side (BUY/SELL)
            quantity: Order quantity
            
        Returns:
            Order response
        """
        logger.info(f"Placing MARKET {side} order: {quantity} {symbol}")
        
        try:
            response = self.client.place_order(
                symbol=symbol,
                side=side,
                order_type='MARKET',
                quantity=quantity
            )
            logger.info(f"Market order placed successfully: Order ID {response.get('orderId')}")
            return response
            
        except Exception as e:
            logger.error(f"Failed to place market order: {e}")
            raise
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, 
                         price: float) -> Dict[str, Any]:
        """
        Place a limit order
        
        Args:
            symbol: Trading pair symbol
            side: Order side (BUY/SELL)
            quantity: Order quantity
            price: Limit price
            
        Returns:
            Order response
        """
        logger.info(f"Placing LIMIT {side} order: {quantity} {symbol} @ {price}")
        
        try:
            response = self.client.place_order(
                symbol=symbol,
                side=side,
                order_type='LIMIT',
                quantity=quantity,
                price=price
            )
            logger.info(f"Limit order placed successfully: Order ID {response.get('orderId')}")
            return response
            
        except Exception as e:
            logger.error(f"Failed to place limit order: {e}")
            raise
    
    def format_order_response(self, response: Dict[str, Any]) -> str:
        """
        Format order response for display
        
        Args:
            response: Order response from API
            
        Returns:
            Formatted string
        """
        output = "\n" + "="*60 + "\n"
        output += "ORDER RESPONSE\n"
        output += "="*60 + "\n"
        
        fields = [
            ('Order ID', 'orderId'),
            ('Symbol', 'symbol'),
            ('Side', 'side'),
            ('Type', 'type'),
            ('Status', 'status'),
            ('Quantity', 'origQty'),
            ('Executed Quantity', 'executedQty'),
            ('Price', 'price'),
            ('Average Price', 'avgPrice'),
            ('Time in Force', 'timeInForce'),
            ('Update Time', 'updateTime'),
        ]
        
        for label, key in fields:
            value = response.get(key, 'N/A')
            if value != 'N/A' and value != '0' and value != 0:
                output += f"{label:20}: {value}\n"
        
        output += "="*60 + "\n"
        return output
