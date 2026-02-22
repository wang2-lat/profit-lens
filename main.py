import typer
from rich.console import Console
from rich.table import Table
from forecasting import forecast_cashflow
from breakeven import calculate_breakeven
from valuation import calculate_valuation

app = typer.Typer(help="CLI tool for small business financial forecasting and valuation analysis")
console = Console()

@app.command()
def cashflow(
    revenue: float = typer.Option(..., help="Average monthly revenue"),
    expenses: float = typer.Option(..., help="Average monthly expenses"),
    current_cash: float = typer.Option(..., help="Current cash balance"),
    months: int = typer.Option(6, help="Number of months to forecast (3-6)"),
    growth_rate: float = typer.Option(0.0, help="Monthly revenue growth rate (e.g., 0.05 for 5%)")
):
    """Forecast cash flow for the next 3-6 months"""
    if months < 3 or months > 6:
        console.print("[red]Months must be between 3 and 6[/red]")
        raise typer.Exit(1)
    
    results = forecast_cashflow(revenue, expenses, current_cash, months, growth_rate)
    
    table = Table(title="Cash Flow Forecast")
    table.add_column("Month", style="cyan")
    table.add_column("Revenue", style="green")
    table.add_column("Expenses", style="yellow")
    table.add_column("Net Cash Flow", style="magenta")
    table.add_column("Ending Balance", style="blue")
    table.add_column("Status", style="bold")
    
    for row in results:
        status = "[red]RISK[/red]" if row['ending_balance'] < 0 else "[green]OK[/green]"
        table.add_row(
            f"Month {row['month']}",
            f"${row['revenue']:,.2f}",
            f"${row['expenses']:,.2f}",
            f"${row['net_cashflow']:,.2f}",
            f"${row['ending_balance']:,.2f}",
            status
        )
    
    console.print(table)
    
    if any(r['ending_balance'] < 0 for r in results):
        console.print("\n[red]WARNING: Cash flow deficit detected in forecast period![/red]")

@app.command()
def breakeven(
    fixed_costs: float = typer.Option(..., help="Monthly fixed costs"),
    variable_cost_per_unit: float = typer.Option(..., help="Variable cost per customer/unit"),
    price_per_unit: float = typer.Option(..., help="Price per customer/unit (MRR for SaaS)")
):
    """Calculate break-even point for SaaS or product business"""
    result = calculate_breakeven(fixed_costs, variable_cost_per_unit, price_per_unit)
    
    if result['error']:
        console.print(f"[red]Error: {result['error']}[/red]")
        raise typer.Exit(1)
    
    console.print("\n[bold cyan]Break-Even Analysis[/bold cyan]")
    console.print(f"Fixed Costs: ${fixed_costs:,.2f}/month")
    console.print(f"Variable Cost per Unit: ${variable_cost_per_unit:,.2f}")
    console.print(f"Price per Unit: ${price_per_unit:,.2f}")
    console.print(f"Contribution Margin: ${result['contribution_margin']:,.2f}")
    console.print(f"\n[bold green]Break-Even Units: {result['breakeven_units']:.0f} customers/units[/bold green]")
    console.print(f"[bold green]Break-Even Revenue: ${result['breakeven_revenue']:,.2f}/month[/bold green]")

@app.command()
def valuation(
    annual_revenue: float = typer.Option(..., help="Annual revenue"),
    annual_profit: float = typer.Option(..., help="Annual net profit"),
    growth_rate: float = typer.Option(0.1, help="Expected annual growth rate (e.g., 0.1 for 10%)"),
    discount_rate: float = typer.Option(0.15, help="Discount rate for DCF (e.g., 0.15 for 15%)"),
    years: int = typer.Option(5, help="Years to project for DCF")
):
    """Calculate company valuation using revenue multiple and DCF methods"""
    result = calculate_valuation(annual_revenue, annual_profit, growth_rate, discount_rate, years)
    
    console.print("\n[bold cyan]Company Valuation Analysis[/bold cyan]")
    console.print(f"Annual Revenue: ${annual_revenue:,.2f}")
    console.print(f"Annual Profit: ${annual_profit:,.2f}")
    console.print(f"Profit Margin: {result['profit_margin']:.1f}%")
    
    console.print("\n[bold yellow]Revenue Multiple Method[/bold yellow]")
    console.print(f"Conservative (1x): ${result['revenue_multiple']['conservative']:,.2f}")
    console.print(f"Moderate (2x): ${result['revenue_multiple']['moderate']:,.2f}")
    console.print(f"Aggressive (3x): ${result['revenue_multiple']['aggressive']:,.2f}")
    
    console.print("\n[bold yellow]Discounted Cash Flow (DCF) Method[/bold yellow]")
    console.print(f"Present Value: ${result['dcf_valuation']:,.2f}")
    
    console.print("\n[bold green]Recommended Acquisition Price Range[/bold green]")
    console.print(f"${result['price_range']['low']:,.2f} - ${result['price_range']['high']:,.2f}")

if __name__ == "__main__":
    app()
