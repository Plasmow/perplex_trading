# perplex_trading
"Perplex is a fully on-chain perpetual trading platform built on AO, a next-generation blockchain combining fast execution, low costs and high resilience." 
We are proposing a way Perplex can mitigate extreme contagion or herdin.

# Market Simulation and Trader Behavior Analysis

## Overview
This project is a cryptocurrency market simulator designed to study market dynamics, trader behavior, and liquidation cascades. 
Over a few days, we developed a model incorporating an order book, price evolution mechanics, and trader balance tracking to better understand the impact of different market participants.

## Features
- **Order Book Simulation**: Implements buy/sell order management and execution.
- **Market Price Evolution**: Models price changes based on net order flow and liquidation events.
- **Trader Profiles**: Simulates Market Makers, Swing Traders, and Degen Traders.
- **Liquidation Mechanism**: Tracks trader balances and enforces liquidation rules.
- **Influence Graph**: Uses a graph-based approach to visualize trading interactions.

## Installation
To set up the project locally:
```bash
# Clone the repository
git clone https://github.com/Plasmow/perplex_trading.git

# Navigate into the project directory
cd perplex_trading

# Install dependencies (if applicable)
pip install -r requirements.txt
```

## Usage
Run the simulation script to observe market behavior (perplex_simulation.ipynb)


For a detailed breakdown of the methodology, check out the [report](report.pdf) included in the repository.

## Results
Key insights from our simulation include:
- **Market Makers stabilize the market**, reducing price volatility.
- **Degen Traders increase liquidation risk**, amplifying price fluctuations.
- **Limit orders help mitigate liquidation events** by reducing exposure to sudden price swings.

## Future Improvements
- Implement machine learning models to optimize trading strategies.
- Introduce real-world data feeds for enhanced realism.
- Expand trader profiles with more diverse strategies.

## Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests.

## Contact
For any questions or suggestions, reach out via GitHub.
