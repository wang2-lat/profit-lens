def calculate_breakeven(fixed_costs, variable_cost_per_unit, price_per_unit):
    """Calculate break-even point"""
    contribution_margin = price_per_unit - variable_cost_per_unit
    
    if contribution_margin <= 0:
        return {
            'error': 'Price must be greater than variable cost per unit',
            'breakeven_units': 0,
            'breakeven_revenue': 0,
            'contribution_margin': contribution_margin
        }
    
    breakeven_units = fixed_costs / contribution_margin
    breakeven_revenue = breakeven_units * price_per_unit
    
    return {
        'error': None,
        'breakeven_units': breakeven_units,
        'breakeven_revenue': breakeven_revenue,
        'contribution_margin': contribution_margin
    }
