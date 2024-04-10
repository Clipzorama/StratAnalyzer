import pandas as pd  # Data Manipulation and Analysis for CSV Files
import tkinter as tk  # GUI Toolkit
import mplfinance as mpf  # For financial data. Compatible with matplot
# Needed for embeding Matplotlib figure inside a Tkinter window
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import customtkinter as ctk


class TSLACC:

    def __init__(self, csv_file_path):

        self.csv_file_path = csv_file_path

        # Read the CSV file into a DataFrame
        self.ohlc_data = pd.read_csv(
            self.csv_file_path, index_col='timestamp', parse_dates=True)

        # Create a tkinter window
        self.tsla_win = tk.Tk()

        self.tsla_win.title('Candlestick Chart')

        width = self.tsla_win.winfo_screenwidth()
        height = self.tsla_win.winfo_screenheight() - 100
        self.tsla_win.geometry("%dx%d" % (width, height))

        self.tsla_win.configure(bg='#040200')

        self.TSLA_label = tk.Label(self.tsla_win,
                                   text="TSLA Data",
                                   font=("Super Funtime", 26),
                                   bg='#040200',
                                   fg='#f5f5dc')

        self.TSLA_label.pack(pady=10)

        # Matplotlib implements the figure of where I would use the mplfinance library for candlestick chart
        self.fig, self.ax = plt.subplots(figsize=(3, 2), facecolor='#040200')
        self.fig.subplots_adjust(bottom=0.15)

        # Changing the colors of the axis

        self.ax.spines['top'].set_edgecolor('#ad343e')
        self.ax.spines['bottom'].set_edgecolor('#ad343e')
        self.ax.spines['left'].set_edgecolor('#ad343e')
        self.ax.spines['right'].set_edgecolor('#ad343e')

        self.ax.set_facecolor('#040200')

        # Modifying Tick Parameters
        self.ax.tick_params(axis='x', which='both', colors='#f5f5dc')
        self.ax.tick_params(axis='y', which='both', colors='#f5f5dc')

        # Create a canvas for Matplotlib
        self.canvas = FigureCanvasTkAgg(
            self.fig, master=self.tsla_win)  # Reference this window
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Create "Zoom In" and "Zoom Out" buttons
        self.zoom_in_button = ctk.CTkButton(master=self.tsla_win,
                                            text="Zoom In",
                                            command=self.zoom_in,
                                            bg_color='#040200',
                                            fg_color='#ad343e',
                                            text_color='#040200',
                                            height=7,
                                            width=18,
                                            hover_color='#86343e')

        self.zoom_in_button.place(x=240, y=60)

        self.zoom_out_button = ctk.CTkButton(master=self.tsla_win,
                                             text="Zoom Out",
                                             command=self.zoom_out,
                                             bg_color='#040200',
                                             fg_color='#ad343e',
                                             text_color='#040200',
                                             height=7,
                                             width=18,
                                             hover_color='#86343e')

        self.zoom_out_button.place(x=1120, y=60)

        self.spy_button = ctk.CTkButton(master=self.tsla_win,
                                        text="$SPY",
                                        command=self.spy_segue,
                                        bg_color='#040200',
                                        fg_color='#040200',
                                        text_color='#ad343e',
                                        hover_color='#040200',
                                        width=10,
                                        height=4)

        self.spy_button.place(x=110, y=300, anchor='center')

        self.tsla_button = ctk.CTkButton(master=self.tsla_win,
                                         text="$TSLA",
                                         command=self.tsla_segue,
                                         bg_color='#040200',
                                         fg_color='#040200',
                                         text_color='#ad343e',
                                         hover_color='#040200',
                                         width=10,
                                         height=4)

        self.tsla_button.place(x=113, y=350, anchor='center')

        self.nvda_button = ctk.CTkButton(master=self.tsla_win,
                                         text="$NVDA",
                                         command=self.nvda_segue,
                                         bg_color='#040200',
                                         fg_color='#040200',
                                         text_color='#ad343e',
                                         hover_color='#040200',
                                         width=10,
                                         height=4)

        self.nvda_button.place(x=113, y=400, anchor='center')

        self.back_nvda = ctk.CTkButton(master=self.tsla_win,
                                       text="Backtest TSLA",
                                       command=self.tsla_backtest,
                                       bg_color='#040200',
                                       fg_color='#5d382f',
                                       text_color='#f5f5dc',
                                       height=27,
                                       width=38,
                                       hover_color='#86343e')

        self.back_nvda.place(x=65, y=450)

        self.exit_button = ctk.CTkButton(master=self.tsla_win,
                                         text="EXIT",
                                         command=self.exit_program,
                                         bg_color='#040200',
                                         fg_color='#040200',
                                         text_color='#ad343e',
                                         hover_color='#040200',
                                         width=10,
                                         height=4)

        self.exit_button.place(x=113, y=650, anchor='center')

        self.update_chart()

    def update_chart(self):

        try:

            # Clear the existing candlestick chart and plot a new one with real-time data
            self.ax.clear()

            # Plots the candlestick chart with the data from csv file
            mpf.plot(self.ohlc_data, type='candle',
                     title='Candlestick Chart', style='charles', ax=self.ax)

            # Update the canvas
            self.canvas.draw()

        except Exception as e:

            print("An exception occurred:", str(e))

    # Methods for zoom in and out effect in chart --> Module Resource

    def zoom_in(self):

        self.ax.set_xlim(self.ax.get_xlim()[0] + 1, self.ax.get_xlim()[1] - 1)
        self.canvas.draw()

    def zoom_out(self):

        self.ax.set_xlim(self.ax.get_xlim()[0] - 1, self.ax.get_xlim()[1] + 1)
        self.canvas.draw()

    def tsla_segue(self):
        self.tsla_win.destroy()  # Close the current TSLA window
        new_app = TSLACC(self.csv_file_path)
        new_app.run()

    def spy_segue(self):
        from spy import SPYCC
        self.tsla_win.destroy()
        spy_csv = 'Data/SPY_5min_sample.csv'
        app = SPYCC(spy_csv)
        app.run()

    def nvda_segue(self):
        from nvda import NVDACC
        self.tsla_win.destroy()
        nvda_csv = 'Data/NVDA_5min.csv'
        app = NVDACC(nvda_csv)
        app.run()

    def tsla_backtest(self):
        from back_tsla import TSLAWindow, TheAnalyzer
        self.tsla_win.destroy()
        analyzer = TSLAWindow(TheAnalyzer)
        analyzer.run()

    def exit_program(self):
        self.tsla_win.destroy()

    def run(self):
        # Start the tkinter main loop
        self.tsla_win.mainloop()


# tsla_csv = 'Data/TSLA_5min.csv'
# app = TSLACC(tsla_csv)
# app.run()
