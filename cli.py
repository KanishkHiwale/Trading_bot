#!/usr/bin/env python3
"""
CLI interface for Binance Futures Trading Bot
"""
import argparse
import sys
import os
import logging
from typing import Optional

from bot import BinanceFuturesClient, OrderManager, InputValidator, setup_logging

logger = logging.getLogger(__name__)


def print_banner():
    """Print application banner"""
    banner = """
    ╔════════════════════════════════════════════════════════════╗
    ║      Binance Futures Trading Bot - Testnet                 ║
    ║      Python Developer Application Task                     ║
    ╚════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_order_summary(symbol: str, side: str, order_type: str, 
                       quantity: float, price: Optional[float] = None):
    """Print order request summary"""
    print("\n" + "="*60)
    print("ORDER REQUEST SUMMARY")
    print("="*60)
    print(f"Symbol        : {symbol}")
    print(f"Side          : {side}")
    print(f"Order Type    : {order_type}")
    print(f"Quantity      : {quantity}")
    if price:
        print(f"Price         : {price}")
    print("="*60)


def load_api_credentials() -> tuple:
    """
    Load API credentials from environment variables
    
    Returns:
        Tuple of (api_key, api_secret)
        
    Raises:
        ValueError: If credentials are not set
    """
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    
    if not api_key or not api_secret:
        raise ValueError(
            "API credentials not found. Please set BINANCE_API_KEY and "
            "BINANCE_API_SECRET environment variables."
        )
    
    return api_key, api_secret


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Binance Futures Trading Bot - Place orders on Testnet',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Place a market buy order
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

  # Place a limit sell order
  python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 2000

  # Place orders with custom log directory
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --log-dir ./my_logs
        """
    )
    
    # Required arguments
    parser.add_argument(
        '--symbol',
        type=str,
        required=True,
        help='Trading pair symbol (e.g., BTCUSDT, ETHUSDT)'
    )
    
    parser.add_argument(
        '--side',
        type=str,
        required=True,
        choices=['BUY', 'SELL', 'buy', 'sell'],
        help='Order side: BUY or SELL'
    )
    
    parser.add_argument(
        '--type',
        type=str,
        required=True,
        choices=['MARKET', 'LIMIT', 'market', 'limit'],
        help='Order type: MARKET or LIMIT',
        dest='order_type'
    )
    
    parser.add_argument(
        '--quantity',
        type=float,
        required=True,
        help='Order quantity (must be greater than 0)'
    )
    
    # Optional arguments
    parser.add_argument(
        '--price',
        type=float,
        help='Limit price (required for LIMIT orders)'
    )
    
    parser.add_argument(
        '--log-dir',
        type=str,
        default='logs',
        help='Directory for log files (default: logs)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging (DEBUG level)'
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    log_file = setup_logging(log_dir=args.log_dir, log_level=log_level)
    
    try:
        # Load API credentials
        logger.info("Loading API credentials from environment variables")
        api_key, api_secret = load_api_credentials()
        
        # Validate inputs
        logger.info("Validating input parameters")
        validated = InputValidator.validate_all(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price
        )
        
        # Print order summary
        print_order_summary(
            validated['symbol'],
            validated['side'],
            validated['order_type'],
            validated['quantity'],
            validated['price']
        )
        
        # Initialize client
        logger.info("Initializing Binance Futures client")
        client = BinanceFuturesClient(api_key, api_secret)
        
        # Test connectivity
        logger.info("Testing API connectivity")
        if not client.test_connectivity():
            raise ConnectionError("Failed to connect to Binance Futures Testnet")
        
        print("✓ Connected to Binance Futures Testnet")
        
        # Initialize order manager
        order_manager = OrderManager(client)
        
        # Place order
        print(f"\nPlacing {validated['order_type']} order...")
        
        if validated['order_type'] == 'MARKET':
            response = order_manager.place_market_order(
                symbol=validated['symbol'],
                side=validated['side'],
                quantity=validated['quantity']
            )
        else:  # LIMIT
            response = order_manager.place_limit_order(
                symbol=validated['symbol'],
                side=validated['side'],
                quantity=validated['quantity'],
                price=validated['price']
            )
        
        # Print response
        formatted_response = order_manager.format_order_response(response)
        print(formatted_response)
        
        # Success message
        print("\n✓ Order placed successfully!")
        print(f"✓ Order ID: {response.get('orderId')}")
        print(f"✓ Status: {response.get('status')}")
        print(f"\nLog file: {log_file}")
        
        return 0
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        print(f"\n✗ Error: {e}")
        return 1
        
    except ConnectionError as e:
        logger.error(f"Connection error: {e}")
        print(f"\n✗ Connection Error: {e}")
        print("Please check your internet connection and API credentials.")
        return 1
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\n✗ Unexpected Error: {e}")
        print(f"Check log file for details: {log_file}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
