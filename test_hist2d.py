import tkinter as tk
from hist2d import Hist2D


def main():
    root = tk.Tk()
    app = Hist2D(root)

    def run_tests():
        try:
            assert app.ticker_entry.get() == ""
            assert app.x_var.get() == ""
            assert app.y_var.get() == ""
            assert app.bins_entry.get() == "150"
            assert app.cmap_var.get() == "Blues"
            print("initial test passed.")

            app.ticker_entry.insert(0, "Invalidticker")
            try:
                app.fetch_data()
                assert app.data is None
                print("invalid ticker test passed")
            except Exception as e:
                print(f"expected error for invalid ticker: {e}")

            app.ticker_entry.delete(0, tk.END)
            app.ticker_entry.insert(0, "AAPL")
            try:
                app.fetch_data()
                assert app.data is not None
                assert 'Close' in app.x_dropdown['values']
                assert 'Close' in app.y_dropdown['values']
                print("ticker test passed")
            except Exception as e:
                print(f"unexpected error for valid ticker {e}")

            app.x_var.set("")
            app.y_var.set("")
            app.plot_data()
            assert app.ax.get_title() == ""
            print("plot without data test passed")

            if app.data is not None:
                app.x_var.set("Close")
                app.y_var.set("Volume")
                app.plot_data()
                assert app.ax.get_title() == "2D Histogram of Close vs Volume"
                print("plot with data test passed")
            else:
                print("skipping plot with data test: No data fetched")

        except Exception as e:
            print(f"error occurred during testing {e}")
        finally:
            root.destroy()

    root.after(1000, run_tests)
    root.mainloop()


if __name__ == "__main__":
    main()
