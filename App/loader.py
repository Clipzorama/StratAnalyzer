import tkinter as tk


class LoaderPage():

    def __init__(self):

        self.loader = tk.Tk()

        # Had to move this to the top since it ignores the geometry for the window.
        self.loader.overrideredirect(1)

        # Dimensions of the window
        width_of_window = 427
        height_of_window = 250

        # Fixed screen dimensions
        screen_width = self.loader.winfo_screenwidth()
        screen_height = self.loader.winfo_screenheight()

        # Calculate x and y coordinates for the window to be in the center and not just touching the center point
        x_coordinate = (screen_width // 2) - (width_of_window // 2)
        y_coordinate = (screen_height // 2) - (height_of_window // 2)

        # Set the geometry
        self.loader.geometry(
            "%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))

        tk.Frame(self.loader, width=427, height=250,
                 bg='#040200').place(x=0, y=0)
        label1 = tk.Label(self.loader, text='Trading Assistant',
                          fg='#f5f5dc', bg='#040200')  # decorate it
        # You need to install this font in your PC or try another one
        label1.configure(font=("Super Funtime", 24, "bold"))
        label1.place(x=110, y=90)

        label2 = tk.Label(self.loader, text='Loading...',
                          fg='#f5f5dc', bg='#040200')  # decorate it
        label2.configure(font=("Super Funtime", 11))
        label2.place(x=10, y=215)

    def segue(self, func):
        self.loader.after(3000, func)
        self.loader.after_cancel()

    def start(self):
        self.loader.mainloop()

    def close(self):
        self.loader.destroy()
