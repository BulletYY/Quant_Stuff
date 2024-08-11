import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime


def main_func(symbol, start_date='2023-01-01'):  # tutaj mozna wybrac dowolną start date
    data_2 = yf.download(symbol, start=start_date,
                         end=datetime.today().strftime('%Y-%m-%d'))
    data_2['SMA15'] = data_2['Close'].rolling(window=15).mean()
    data_2['SMA30'] = data_2['Close'].rolling(window=30).mean()

    def RSI(data, window=14):
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    data_2['RSI'] = RSI(data_2)

    data_2['Daily Return'] = data_2['Close'].pct_change()

    plt.figure(figsize=(15, 12))

    plt.subplot(3, 1, 1)
    plt.plot(data_2.index, data_2['Close'],
             label='Stock Price', color='blue')
    plt.plot(data_2.index, data_2['SMA15'],
             label='SMA15', color='red', linestyle='--')
    plt.plot(data_2.index, data_2['SMA30'],
             label='SMA30', color='green', linestyle='--')

    cross_points = []
    for i in range(1, len(data_2)):
        if data_2['SMA15'].iloc[i] > data_2['SMA30'].iloc[i] and data_2['SMA15'].iloc[i - 1] <= data_2['SMA30'].iloc[i - 1]:
            cross_points.append((data_2.index[i], 'Golden Cross'))
        elif data_2['SMA15'].iloc[i] < data_2['SMA30'].iloc[i] and data_2['SMA15'].iloc[i - 1] >= data_2['SMA30'].iloc[i - 1]:
            cross_points.append((data_2.index[i], 'Death Cross'))

    for cross_point in cross_points:
        plt.scatter(cross_point[0], data_2.loc[cross_point[0]]['Close'],
                    marker='o', color='black' if cross_point[1] == 'Golden Cross' else 'red')

    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.legend()
    plt.title(f'{symbol} Stock price and Moving Averages')
    plt.ylabel('Bond Price')

    plt.subplot(3, 1, 2)
    plt.plot(data_2.index, data_2['RSI'], label='RSI', color='purple')
    plt.axhline(y=70, color='r', linestyle='--', label='Overbought (70)')
    plt.axhline(y=30, color='g', linestyle='--', label='Oversold (30)')
    plt.fill_between(data_2.index, data_2['RSI'], 70, where=(
        data_2['RSI'] >= 70), color='red', alpha=0.3)
    plt.fill_between(data_2.index, data_2['RSI'], 30, where=(
        data_2['RSI'] <= 30), color='green', alpha=0.3)
    plt.title('RSI Analysis')
    plt.xlabel('Date')
    plt.ylabel('RSI')
    plt.grid(True)
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(data_2.index,
             data_2['Daily Return'], label='Daily Return', color='orange')
    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    plt.fill_between(data_2.index, data_2['Daily Return'], 0, where=(
        data_2['Daily Return'] >= 0), color='green', alpha=0.3)
    plt.fill_between(data_2.index, data_2['Daily Return'], 0, where=(
        data_2['Daily Return'] < 0), color='red', alpha=0.3)
    plt.title('Daily Returns')
    plt.xlabel('Date')
    plt.ylabel('Daily Return')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()


# WYBRANIE DOWOLNEJ SPOLKI W celu analizy MACD15 MACD130 i RSI
main_func('TSLA')  # TSLA NVIDA ETC
