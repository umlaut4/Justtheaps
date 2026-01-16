# Justtheaps - Arbitrage Detection System

A real-time arbitrage detection system that identifies profitable opportunities between prediction markets on Polymarket and Kalshi. The system fetches data from both APIs, matches similar markets, and displays arbitrage opportunities through a web dashboard.

## Features

- 🔍 **Real-time Market Data**: Fetches live market data from Polymarket and Kalshi APIs
- 🤝 **Intelligent Market Matching**: Automatically matches similar markets across platforms using text similarity algorithms
- 💰 **Arbitrage Detection**: Identifies profitable arbitrage opportunities when market prices diverge
- 📊 **Web Dashboard**: Clean, modern UI for viewing and analyzing opportunities
- 🔄 **Auto-refresh**: Dashboard automatically updates with fresh data
- 📈 **Statistics**: Track market counts, matches, and opportunity metrics

## How It Works

1. **Data Collection**: The system fetches active markets from both Polymarket and Kalshi APIs
2. **Market Matching**: Markets are matched based on question similarity using text comparison algorithms
3. **Arbitrage Detection**: For matched markets, the system calculates if buying complementary outcomes on different platforms results in guaranteed profit
4. **Display**: Opportunities are ranked by profit percentage and displayed on the web dashboard

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/umlaut4/Justtheaps.git
cd Justtheaps
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

Start the web server:
```bash
python app.py
```

The dashboard will be available at `http://localhost:5000`

### Using the Dashboard

1. Open your browser to `http://localhost:5000`
2. View current arbitrage opportunities displayed on the dashboard
3. Click "🔄 Refresh Data" to manually update market data
4. The dashboard auto-refreshes every 5 minutes

### Understanding Arbitrage Opportunities

Each opportunity card shows:
- **Question**: The market question from both platforms
- **Profit Percentage**: The potential profit as a percentage of investment
- **Strategy**: Which positions to take on each platform
- **Market Details**: Prices and IDs for both markets
- **Total Cost**: Combined cost of both positions
- **Potential Profit**: Guaranteed profit if either outcome occurs
- **Similarity Score**: How closely the markets match (higher is better)

## Architecture

### Components

- **polymarket_client.py**: Fetches and standardizes data from Polymarket API
- **kalshi_client.py**: Fetches and standardizes data from Kalshi API
- **market_matcher.py**: Matches markets across platforms using text similarity
- **arbitrage_detector.py**: Calculates arbitrage opportunities from matched markets
- **app.py**: Flask web server providing API endpoints and serving the dashboard
- **templates/index.html**: Web dashboard UI

### API Endpoints

- `GET /`: Serves the dashboard UI
- `GET /api/opportunities`: Returns current opportunities and statistics
- `GET /api/refresh`: Manually triggers a data refresh

## Configuration

You can adjust detection parameters by modifying the initialization in `app.py`:

```python
# Minimum similarity score to match markets (0.0 to 1.0)
market_matcher = MarketMatcher(similarity_threshold=0.6)

# Minimum profit percentage to display (0.01 = 1%)
arbitrage_detector = ArbitrageDetector(min_profit_threshold=0.01)
```

## Notes

- The system uses public API endpoints that don't require authentication
- Market data is cached to reduce API calls
- Not all matched markets will have arbitrage opportunities
- Arbitrage opportunities may be small or temporary
- Consider transaction fees and execution risk in real trading scenarios

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.