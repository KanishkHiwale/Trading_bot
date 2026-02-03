"""
Input validation for trading parameters
"""
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class InputValidator:
    """Validates trading input parameters"""
    
    VALID_SIDES = ['BUY', 'SELL']
    VALID_ORDER_TYPES = ['MARKET', 'LIMIT']
    
    @staticmethod
    def validate_symbol(symbol: str) -> str:
        """
        Validate trading symbol
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            Validated symbol in uppercase
            
        Raises:
            ValueError: If symbol is invalid
        """
        if not symbol or not isinstance(symbol, str):
            raise ValueError("Symbol must be a non-empty string")
        
        symbol = symbol.upper().strip()
        
        if len(symbol) < 3:
            raise ValueError("Symbol is too short")
        
        logger.debug(f"Symbol validated: {symbol}")
        return symbol
    
    @staticmethod
    def validate_side(side: str) -> str:
        """
        Validate order side
        
        Args:
            side: Order side (BUY/SELL)
            
        Returns:
            Validated side in uppercase
            
        Raises:
            ValueError: If side is invalid
        """
        if not side or not isinstance(side, str):
            raise ValueError("Side must be a non-empty string")
        
        side = side.upper().strip()
        
        if side not in InputValidator.VALID_SIDES:
            raise ValueError(f"Side must be one of {InputValidator.VALID_SIDES}")
        
        logger.debug(f"Side validated: {side}")
        return side
    
    @staticmethod
    def validate_order_type(order_type: str) -> str:
        """
        Validate order type
        
        Args:
            order_type: Order type (MARKET/LIMIT)
            
        Returns:
            Validated order type in uppercase
            
        Raises:
            ValueError: If order type is invalid
        """
        if not order_type or not isinstance(order_type, str):
            raise ValueError("Order type must be a non-empty string")
        
        order_type = order_type.upper().strip()
        
        if order_type not in InputValidator.VALID_ORDER_TYPES:
            raise ValueError(f"Order type must be one of {InputValidator.VALID_ORDER_TYPES}")
        
        logger.debug(f"Order type validated: {order_type}")
        return order_type
    
    @staticmethod
    def validate_quantity(quantity: float) -> float:
        """
        Validate order quantity
        
        Args:
            quantity: Order quantity
            
        Returns:
            Validated quantity
            
        Raises:
            ValueError: If quantity is invalid
        """
        try:
            quantity = float(quantity)
        except (TypeError, ValueError):
            raise ValueError("Quantity must be a valid number")
        
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        
        logger.debug(f"Quantity validated: {quantity}")
        return quantity
    
    @staticmethod
    def validate_price(price: Optional[float], order_type: str) -> Optional[float]:
        """
        Validate order price
        
        Args:
            price: Order price
            order_type: Order type (MARKET/LIMIT)
            
        Returns:
            Validated price or None for MARKET orders
            
        Raises:
            ValueError: If price is invalid
        """
        if order_type == 'MARKET':
            return None
        
        if price is None:
            raise ValueError("Price is required for LIMIT orders")
        
        try:
            price = float(price)
        except (TypeError, ValueError):
            raise ValueError("Price must be a valid number")
        
        if price <= 0:
            raise ValueError("Price must be greater than 0")
        
        logger.debug(f"Price validated: {price}")
        return price
    
    @classmethod
    def validate_all(cls, symbol: str, side: str, order_type: str, 
                    quantity: float, price: Optional[float] = None) -> dict:
        """
        Validate all order parameters
        
        Args:
            symbol: Trading pair symbol
            side: Order side
            order_type: Order type
            quantity: Order quantity
            price: Order price (optional)
            
        Returns:
            Dictionary of validated parameters
            
        Raises:
            ValueError: If any parameter is invalid
        """
        validated = {
            'symbol': cls.validate_symbol(symbol),
            'side': cls.validate_side(side),
            'order_type': cls.validate_order_type(order_type),
            'quantity': cls.validate_quantity(quantity),
            'price': cls.validate_price(price, order_type)
        }
        
        logger.info("All parameters validated successfully")
        return validated
