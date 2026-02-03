"""
Binance Futures Testnet API Client
Handles authentication and API communication
"""
import hashlib
import hmac
import time
import requests
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class BinanceFuturesClient:
    """Client for interacting with Binance Futures Testnet API"""
    
    def __init__(self, api_key: str, api_secret: str):
        """
        Initialize the Binance Futures client
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://testnet.binancefuture.com"
        self.session = requests.Session()
        self.session.headers.update({
            'X-MBX-APIKEY': self.api_key
        })
        
    def _generate_signature(self, params: Dict[str, Any]) -> str:
        """
        Generate HMAC SHA256 signature for authenticated requests
        
        Args:
            params: Request parameters
            
        Returns:
            Hex signature string
        """
        query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, 
                 signed: bool = False) -> Dict[str, Any]:
        """
        Make HTTP request to Binance API
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Request parameters
            signed: Whether request needs signature
            
        Returns:
            API response as dictionary
            
        Raises:
            requests.exceptions.RequestException: On network errors
            ValueError: On API errors
        """
        url = f"{self.base_url}{endpoint}"
        params = params or {}
        
        if signed:
            params['timestamp'] = int(time.time() * 1000)
            params['signature'] = self._generate_signature(params)
        
        logger.info(f"Making {method} request to {endpoint}")
        logger.debug(f"Request params: {params}")
        
        try:
            response = self.session.request(method, url, params=params)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Request successful: {response.status_code}")
            logger.debug(f"Response data: {data}")
            
            return data
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP Error: {e.response.status_code}"
            try:
                error_data = e.response.json()
                error_msg += f" - {error_data.get('msg', 'Unknown error')}"
                logger.error(f"API Error: {error_data}")
            except:
                logger.error(f"HTTP Error: {e}")
            raise ValueError(error_msg)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network Error: {e}")
            raise
    
    def test_connectivity(self) -> bool:
        """
        Test API connectivity
        
        Returns:
            True if connection successful
        """
        try:
            self._request('GET', '/fapi/v1/ping')
            logger.info("Connectivity test passed")
            return True
        except Exception as e:
            logger.error(f"Connectivity test failed: {e}")
            return False
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get account information
        
        Returns:
            Account information dictionary
        """
        return self._request('GET', '/fapi/v2/account', signed=True)
    
    def get_exchange_info(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """
        Get exchange trading rules and symbol information
        
        Args:
            symbol: Optional specific symbol to query
            
        Returns:
            Exchange information dictionary
        """
        params = {}
        if symbol:
            params['symbol'] = symbol
        return self._request('GET', '/fapi/v1/exchangeInfo', params=params)
    
    def place_order(self, symbol: str, side: str, order_type: str, 
                    quantity: float, price: Optional[float] = None,
                    time_in_force: str = 'GTC') -> Dict[str, Any]:
        """
        Place an order on Binance Futures
        
        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            side: Order side (BUY or SELL)
            order_type: Order type (MARKET or LIMIT)
            quantity: Order quantity
            price: Order price (required for LIMIT orders)
            time_in_force: Time in force (default: GTC - Good Till Cancel)
            
        Returns:
            Order response dictionary
            
        Raises:
            ValueError: If parameters are invalid
        """
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity,
        }
        
        if order_type == 'LIMIT':
            if price is None:
                raise ValueError("Price is required for LIMIT orders")
            params['price'] = price
            params['timeInForce'] = time_in_force
        
        logger.info(f"Placing {order_type} {side} order for {quantity} {symbol}")
        
        return self._request('POST', '/fapi/v1/order', params=params, signed=True)
