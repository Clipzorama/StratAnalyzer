
# Plot small parts of a trading strategy inside of the program

import talib
from backtesting import Backtest, Strategy
import pandas as pd
from backtesting.lib import crossover
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk


class TheAnalyzer(Strategy):

    upper_bound = 70
    lower_bound = 30
    n1 = 8
    n2 = 21
    rsi_default = 14

    # Backtesting module initiates this method first and then the next method.
    def init(self):

        self.rsi = self.I(talib.RSI, self.data.Close, 14)
        self.ema8 = self.I(talib.EMA, self.data.Close, timeperiod=self.n1)
        self.ema21 = self.I(talib.EMA, self.data.Close, timeperiod=self.n2)
        # returns 100 if discovered and 0, otherwise.
        self.demand_zone = self.I(
            talib.CDL3WHITESOLDIERS, self.data.Open, self.data.High, self.data.Low, self.data.Close)
        # Same for plotting the supply zone
        self.supply_zone = self.I(
            talib.CDL3BLACKCROWS, self.data.Open, self.data.High, self.data.Low, self.data.Close)

    # Traversing through each candlestick here

    def next(self):

        # Check for RSI and EMA crossovers

        ema_bullish_crossover = crossover(self.ema8, self.ema21)
        ema_bearish_crossover = crossover(self.ema21, self.ema8)
        # Demand zone pattern recognition
        demand_zone_signal = self.demand_zone[-1] != 0
        rsi_in_range = 30 <= self.rsi[-1] <= 70  # RSI between 30 and 70

        # For sell conditions
        rsi_overbought = self.rsi[-1] > 70  # RSI over 70
        supply_zone_signal = self.supply_zone[-1] != 0

        # print(f"Current Bar: {self.data.index[-1]}")
        # print(f"EMA8: {self.ema8[-1]}, EMA21: {self.ema21[-1]}")
        # print(f"RSI: {self.rsi[-1]}")
        # print(f"Bullish Crossover: {ema_bullish_crossover}")
        # print(f"Bearish Crossover: {ema_bearish_crossover}")
        # print(f"Demand Zone Signal: {demand_zone_signal}")
        # print(f"Supply Zone Signal: {supply_zone_signal}")
        # print(f"RSI Overbought: {rsi_overbought}")
        # print(f"RSI in Range: {rsi_in_range}")

        # Buy conditions
        # For Demand zone, we need to get the last candlestick from the pattern which is why we put -1, and > 0 checks if pattern was found
        if (ema_bullish_crossover or demand_zone_signal) and rsi_in_range and not self.position:
            self.buy()

        # Sell conditions
        if self.position and (rsi_overbought or supply_zone_signal or ema_bearish_crossover):
            self.sell()


class NVDAWindow:

    def __init__(self):

        self.nvdabt_win = tk.Tk()

        self.nvdabt_win.title("NVDA Backtest Results")

        self.width = self.nvdabt_win.winfo_screenwidth()
        self.height = self.nvdabt_win.winfo_screenheight() - 100
        self.nvdabt_win.geometry("%dx%d" % (self.width, self.height))

        self.result_label = tk.Label(self.nvdabt_win, text="Backtest Results for :", font=(
            'Super Funtime', 28), fg='#f5f5dc', bg='#040200')
        self.result_label.place(x=60, y=100)

        # For the Symbol
        self.image = Image.open("Pics/nvda.png")
        self.preferred_size = (100, 100)
        self.resized_image = self.image.resize(self.preferred_size)
        self.tk_image = ImageTk.PhotoImage(self.resized_image)

        image_label = tk.Label(
            self.nvdabt_win, image=self.tk_image, bg='#040200')
        image_label.place(x=380, y=100)

        # For the plot

        self.plot_image = Image.open("Pics/nvda_plot.png")
        self.plot_size = (800, 500)
        self.rsplot_image = self.plot_image.resize(self.plot_size)
        self.tkplot_image = ImageTk.PhotoImage(self.rsplot_image)

        plot_label = tk.Label(self.nvdabt_win, image=self.tkplot_image)
        plot_label.place(x=500, y=90)

        self.data = pd.read_csv('Data/NVDA_5min.csv',
                                parse_dates=True, index_col='timestamp')

        # Renaming the columns here so they match the columns for the TA LIB

        self.data = self.data.rename(columns={
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'volume': 'Volume'  # only if volume exists in your data
        })

        self.data.sort_index(inplace=True)
        start_date = pd.Timestamp('2023-09-27')
        self.data = self.data[self.data.index >= start_date]

        print(self.data.head())

        # Checks if you put 5000 on a position

        self.bt = Backtest(self.data, TheAnalyzer, cash=5_000)

        result_text = tk.Text(self.nvdabt_win, width=45, height=40, bg='#040200',
                              fg='#f5f5dc', highlightbackground='#040200', highlightcolor='#040200')
        result_text.insert(tk.END, str(self.bt.run()))
        result_text.place(x=60, y=170)
        self.nvdabt_win.configure(bg='#040200')

        back_button = ctk.CTkButton(master=self.nvdabt_win,
                                    text="Go Back",
                                    command=self.nvda_segue,
                                    bg_color='#040200',
                                    fg_color='#ad343e',
                                    text_color='#040200',
                                    height=7,
                                    width=18,
                                    hover_color='#86343e')
        back_button.place(x=180, y=640)

        backtest_button = ctk.CTkButton(master=self.nvdabt_win,
                                        text="NVDA Plot Diagram",
                                        command=self.strategy_plot,
                                        bg_color='#040200',
                                        fg_color='#5d382f',
                                        font=('Super Funtime', 28),
                                        text_color='#f5f5dc',
                                        height=49,
                                        width=54,
                                        hover_color='#5d382f')

        backtest_button.place(x=850, y=650)

    def nvda_segue(self):
        self.nvdabt_win.destroy()
        from nvda import NVDACC
        nvda_csv = 'Data/NVDA_5min.csv'
        app = NVDACC(nvda_csv)
        app.run()

    def strategy_plot(self):
        self.bt.plot()

    def run(self):
        self.nvdabt_win.mainloop()


# Gonna add the plot on the same page

# app = NVDAWindow()

# app.run()
