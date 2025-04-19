import tkinter as tk
from tkinter import messagebox
import json
import os
import numpy as np
import matplotlib.pyplot as plt

HISTORICAL_DATA_FILE = "historical_data.json"

investment_entries = []

def fractional_knapsack(budget, investments):
    investments.sort(key=lambda x: x[1] / x[0], reverse=True)
    total_returns = 0.0
    breakdown = []
    
    for cost, returns in investments:
        if budget >= cost:
            budget -= cost
            total_returns += returns
            breakdown.append(f"Included 100% of investment with cost {cost} and return {returns}")
        else:
            total_returns += returns * (budget / cost)
            breakdown.append(f"Included {budget / cost * 100:.2f}% of investment with cost {cost} and return {returns}")
            break

    return total_returns, breakdown

def validate_input(value):
    try:
        val = float(value)
        if val <= 0:
            raise ValueError
        return val
    except ValueError:
        return None

def save_historical_data(investments):
    if os.path.exists(HISTORICAL_DATA_FILE):
        with open(HISTORICAL_DATA_FILE, 'r') as file:
            data = json.load(file)
    else:
        data = []

    data.append(investments)

    with open(HISTORICAL_DATA_FILE, 'w') as file:
        json.dump(data, file)

def load_historical_data():
    if os.path.exists(HISTORICAL_DATA_FILE):
        with open(HISTORICAL_DATA_FILE, 'r') as file:
            return json.load(file)
    else:
        return []

def add_investment_fields(num_investments):
    # Clear previous investment fields
    for entry in investment_entries:
        entry[0].destroy()
        entry[1].destroy()
    investment_entries.clear()

    for i in range(num_investments):
        cost_label = tk.Label(root, text=f"Investment {i + 1} - Cost:", font=font_style, bg="#e0f7fa")
        cost_label.grid(row=len(investment_entries) + 2, column=0, padx=padx, pady=pady)
        
        cost_entry = tk.Entry(root, font=entry_font, width=10)
        cost_entry.grid(row=len(investment_entries) + 2, column=1, padx=padx, pady=pady)
        
        return_label = tk.Label(root, text=f"Investment {i + 1} - Return:", font=font_style, bg="#e0f7fa")
        return_label.grid(row=len(investment_entries) + 2, column=2, padx=padx, pady=pady)
        
        return_entry = tk.Entry(root, font=entry_font, width=10)
        return_entry.grid(row=len(investment_entries) + 2, column=3, padx=padx, pady=pady)

        investment_entries.append((cost_entry, return_entry))

def calculate_returns():
    try:
        budget = validate_input(budget_entry.get().strip())
        if budget is None:
            raise ValueError("Budget must be a positive number.")

        investments = []
        for cost_entry, return_entry in investment_entries:
            cost = validate_input(cost_entry.get().strip())
            returns = validate_input(return_entry.get().strip())
            if cost is None or returns is None:
                raise ValueError("Costs and returns must be positive numbers.")
            investments.append((cost, returns))

        greedy_result, breakdown = fractional_knapsack(budget, investments)

        results_text.delete(1.0, tk.END)
        results_text.insert(tk.END, f"Maximum return: {greedy_result:.2f}\n")
        results_text.insert(tk.END, "\n".join(breakdown))

        # Save current investments to historical data
        save_historical_data(investments)

        # Plot comparison with historical data
        plot_comparison_with_historical(greedy_result)

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

def plot_comparison_with_historical(current_return):
    historical_data = load_historical_data()
    
    # Calculate average historical return if there's any historical data
    if historical_data:
        historical_returns = [sum(inv[1] for inv in entry) for entry in historical_data]
        average_historical_return = np.mean(historical_returns)
        labels = ['Current Return', 'Average Historical Return']
        values = [current_return, average_historical_return]

        # Plotting
        plt.figure(figsize=(8, 5))
        plt.bar(labels, values, color=['skyblue', 'lightgreen'])
        plt.title('Current Return vs Average Historical Return')
        plt.ylabel('Return Amount')
        plt.ylim(0, max(current_return, average_historical_return) * 1.2)  # Set y-limit for better visualization
        plt.grid(axis='y')
        plt.show()
    else:
        messagebox.showinfo("No Historical Data", "No historical data available for comparison.")
