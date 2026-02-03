# Binance Futures Trading Bot - Testnet

A Python-based trading bot for placing orders on Binance Futures Testnet (USDT-M). Built as part of the Python Developer application task.

## Features

- ✅ Place **MARKET** and **LIMIT** orders on Binance Futures Testnet
- ✅ Support for both **BUY** and **SELL** sides
- ✅ Clean CLI interface with input validation
- ✅ Comprehensive logging to file
- ✅ Structured, modular code architecture
- ✅ Proper error handling and user-friendly messages

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py           # Package initialization
│   ├── client.py             # Binance API client wrapper
│   ├── orders.py             # Order placement logic
│   ├── validators.py         # Input validation
│   └── logging_config.py     # Logging configuration
├── cli.py                    # CLI entry point
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── logs/                     # Log files (created automatically)
```

## Setup

### 1. Prerequisites

- Python 3.7 or higher
- Binance Futures Testnet account with API credentials

### 2. Get Binance Testnet API Credentials

1. Visit [Binance Futures Testnet](https://testnet.binancefuture.com/)
2. Register/login with your email
3. Generate API Key and Secret from your account dashboard
4. **Important**: Keep your API Secret secure and never commit it to version control

### 3. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd trading_bot

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure API Credentials

Set your API credentials as environment variables:

**Linux/Mac:**
```bash
export BINANCE_API_KEY="your_api_key_here"
export BINANCE_API_SECRET="your_api_secret_here"
```

**Windows (Command Prompt):**
```cmd
set BINANCE_API_KEY=your_api_key_here
set BINANCE_API_SECRET=your_api_secret_here
```

**Windows (PowerShell):**
```powershell
$env:BINANCE_API_KEY="your_api_key_here"
$env:BINANCE_API_SECRET="your_api_secret_here"
```

## Usage

### Basic Command Structure

```bash
python cli.py --symbol SYMBOL --side SIDE --type TYPE --quantity QUANTITY [--price PRICE]
```

### Required Arguments

- `--symbol`: Trading pair (e.g., BTCUSDT, ETHUSDT)
- `--side`: Order side (BUY or SELL)
- `--type`: Order type (MARKET or LIMIT)
- `--quantity`: Order quantity (must be > 0)

### Optional Arguments

- `--price`: Limit price (required for LIMIT orders)
- `--log-dir`: Custom log directory (default: logs)
- `--verbose`: Enable debug logging

### Examples

#### 1. Place a Market Buy Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**Expected Output:**
```
╔════════════════════════════════════════════════════════════╗
║      Binance Futures Trading Bot - Testnet                 ║
║      Python Developer Application Task                     ║
╚════════════════════════════════════════════════════════════╝

============================================================
ORDER REQUEST SUMMARY
============================================================
Symbol        : BTCUSDT
Side          : BUY
Order Type    : MARKET
Quantity      : 0.001
============================================================
✓ Connected to Binance Futures Testnet

Placing MARKET order...

============================================================
ORDER RESPONSE
============================================================
Order ID            : 123456789
Symbol              : BTCUSDT
Side                : BUY
Type                : MARKET
Status              : FILLED
Quantity            : 0.001
Executed Quantity   : 0.001
Average Price       : 45000.50
============================================================

✓ Order placed successfully!
✓ Order ID: 123456789
✓ Status: FILLED

Log file: logs/trading_bot_20260203_143022.log
```

#### 2. Place a Limit Sell Order

```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 2000
```

#### 3. Using Verbose Logging

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --verbose
```

#### 4. Custom Log Directory

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --log-dir ./my_logs
```

## Input Validation

The bot validates all inputs before placing orders:

- **Symbol**: Must be a valid non-empty string
- **Side**: Must be BUY or SELL
- **Order Type**: Must be MARKET or LIMIT
- **Quantity**: Must be a positive number
- **Price**: Required for LIMIT orders, must be a positive number

Invalid inputs will be rejected with clear error messages.

## Logging

All operations are logged to timestamped files in the `logs/` directory:

- **Filename format**: `trading_bot_YYYYMMDD_HHMMSS.log`
- **Log contents**: API requests, responses, errors, and all operations
- **Console output**: User-friendly summary of operations

Example log entry:
```
2026-02-03 14:30:22 - bot.client - INFO - Making POST request to /fapi/v1/order
2026-02-03 14:30:22 - bot.client - DEBUG - Request params: {'symbol': 'BTCUSDT', 'side': 'BUY', ...}
2026-02-03 14:30:23 - bot.client - INFO - Request successful: 200
2026-02-03 14:30:23 - bot.orders - INFO - Market order placed successfully: Order ID 123456789
```

## Error Handling

The bot handles various error scenarios:

- **Missing API credentials**: Clear message to set environment variables
- **Invalid input**: Validation errors with specific reasons
- **Network errors**: Connection failure messages
- **API errors**: HTTP error codes and API error messages
- **Unexpected errors**: Logged with full traceback for debugging

## Code Architecture

### 1. Separation of Concerns

- **client.py**: Low-level API communication
- **orders.py**: Business logic for order placement
- **validators.py**: Input validation logic
- **logging_config.py**: Centralized logging setup
- **cli.py**: User interface layer

### 2. Design Principles

- Clean, readable code with docstrings
- Type hints for better code quality
- Single Responsibility Principle
- Proper error handling at each layer
- Comprehensive logging

## Testing on Testnet

This bot is configured exclusively for **Binance Futures Testnet**:

- **Base URL**: `https://testnet.binancefuture.com`
- **No real money**: All orders use testnet funds
- **Safe testing**: Perfect for development and testing

## Assumptions

1. **API Credentials**: Stored in environment variables for security
2. **Network**: Stable internet connection required
3. **Testnet Funds**: User has sufficient testnet balance
4. **Order Execution**: Testnet may have different liquidity than production
5. **Symbols**: User provides valid trading pairs supported by Binance Futures

## Common Issues & Solutions

### Issue: "API credentials not found"
**Solution**: Set BINANCE_API_KEY and BINANCE_API_SECRET environment variables

### Issue: "Price is required for LIMIT orders"
**Solution**: Add --price argument when placing LIMIT orders

### Issue: "Connection Error"
**Solution**: Check internet connection and verify testnet is accessible

### Issue: "Invalid symbol"
**Solution**: Use valid Binance Futures symbols like BTCUSDT, ETHUSDT

## Future Enhancements (Bonus Ideas)

- Stop-Limit orders
- OCO (One-Cancels-Other) orders
- Position management
- Interactive CLI menu
- Order history tracking
- Enhanced UI with Rich library
