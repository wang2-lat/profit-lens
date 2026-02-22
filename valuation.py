def calculate_valuation(annual_revenue, annual_profit, growth_rate, discount_rate, years):
    """Calculate company valuation using multiple methods"""
    profit_margin = (annual_profit / annual_revenue * 100) if annual_revenue > 0 else 0
    
    # Revenue multiple method
    revenue_multiple = {
        'conservative': annual_revenue * 1,
        'moderate': annual_revenue * 2,
        'aggressive': annual_revenue * 3
    }
    
    # DCF method
    dcf_value = 0
    for year in range(1, years + 1):
        projected_profit = annual_profit * ((1 + growth_rate) ** year)
        present_value = projected_profit / ((1 + discount_rate) ** year)
        dcf_value += present_value
    
    # Price range recommendation
    low_price = min(revenue_multiple['conservative'], dcf_value * 0.8)
    high_price = max(revenue_multiple['moderate'], dcf_value * 1.2)
    
    return {
        'profit_margin': profit_margin,
        'revenue_multiple': revenue_multiple,
        'dcf_valuation': dcf_value,
        'price_range': {
            'low': low_price,
            'high': high_price
        }
    }
