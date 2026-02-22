def forecast_cashflow(revenue, expenses, current_cash, months, growth_rate):
    """Forecast cash flow for specified months"""
    results = []
    balance = current_cash
    
    for month in range(1, months + 1):
        month_revenue = revenue * ((1 + growth_rate) ** (month - 1))
        net_cashflow = month_revenue - expenses
        balance += net_cashflow
        
        results.append({
            'month': month,
            'revenue': month_revenue,
            'expenses': expenses,
            'net_cashflow': net_cashflow,
            'ending_balance': balance
        })
    
    return results
