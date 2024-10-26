import tkinter as tk
from tkinter import messagebox
from brain5 import ReplyBrain
from Speak2 import Speak

def get_stock_price():
    ticker = entry.get()
    if ticker:
        result = ReplyBrain(f"stock price of",ticker)
        output_text.set(result)
    else:
        messagebox.showerror("Input Error", "Please enter a valid company name.")

def get_stock_news():
    company = entry.get()
    if company:
        result = ReplyBrain(f"news of",company)
        output_text.set(result)
    else:
        messagebox.showerror("Input Error", "Please enter a valid company name.")

def get_stock_sentiment():
    company = entry.get()
    if company:
        result = ReplyBrain(f"stock analysis of",company)
        output_text.set(result)
    else:
        messagebox.showerror("Input Error", "Please enter a valid company name.")

def predict_stock():
    company = entry.get()
    if company:
        result = ReplyBrain(f"predict stock of",company)
        output_text.set(result)
    else:
        messagebox.showerror("Input Error", "Please enter a valid company name.")

root = tk.Tk()
root.title("Stock-a-chance")

root.geometry("500x400")

label = tk.Label(root, text="Stock-a-chance", font=("Helvetica", 16))
label.pack(pady=10)

entry_label = tk.Label(root, text="Enter Company Name:")
entry_label.pack(pady=5)
entry = tk.Entry(root, width=40)
entry.pack(pady=5)

price_button = tk.Button(root, text="Get Stock Price", command=get_stock_price)
price_button.pack(pady=5)

news_button = tk.Button(root, text="Get Stock News", command=get_stock_news)
news_button.pack(pady=5)

sentiment_button = tk.Button(root, text="Get Stock Sentiment Analysis", command=get_stock_sentiment)
sentiment_button.pack(pady=5)

predict_button = tk.Button(root, text="Predict Stock Price", command=predict_stock)
predict_button.pack(pady=5)

output_text = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text, wraplength=400, justify="left")
output_label.pack(pady=10)

root.mainloop()
