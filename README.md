
# StratAnalyzer

StratAnalyzer is a comprehensive backtesting tool designed to evaluate the effectiveness of trading strategies using historical data. Built with Python, it employs a user-friendly interface created with Tkinter and CustomTkinter, enabling users to easily navigate and operate the tool.

## Features

- **Data Visualization:** Utilize matplot and mpfinance for detailed visualization of price actions to backtest trading strategies.
- **Strategy Testing:** Employ TaLib and backtesting.py to build and test trading strategies, identify potential entry, and exit points on historical price data.
- **Technical Indicators:** The tool includes the RSI indicator and dual EMA indicators for robust confirmation signals.
- **Pattern Recognition:** Advanced pattern recognition algorithms to help identify Overbought/Supply and Demand zones, crucial for market analysis.

## Customization

StratAnalyzer is built for flexibility, allowing developers to modify or entirely replace the logic of the predefined trading strategy. By personalizing the strategy logic, you can test its efficiency against the ohlc charts to suit your analytical needs.

## Getting Started

To get started with StratAnalyzer:

1. Clone the repository to your local machine.
2. Ensure you have Python installed, along with the necessary libraries: Tkinter, CustomTkinter, matplot, mpfinance, TaLib, and backtesting.py.
3. Run the main application file to launch the interface.
4. Input your historical data and select the indicators you wish to test.
5. Analyze the results and adjust your strategy accordingly.

## Contributions

Contributions to StratAnalyzer are welcome! Whether it's improving the code, enhancing the UI, or adding new features, your input is valuable. Please feel free to fork the repository, make your changes, and submit a pull request.

## Security

StratAnalyzer takes security seriously:

- **Hashing:** User credentials are secured using hashing. Before using the application, set up your user account.

## User Account Setup

To create your user account for StratAnalyzer:

1. Navigate to the `login.py` file in the repository.
2. Follow the instructions within to create a new user with a hashed password.
3. Once set up, use these credentials to sign in to the StratAnalyzer application.
