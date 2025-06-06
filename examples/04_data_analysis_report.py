"""FlowCard Example 04: Data Analysis Report

This example demonstrates creating a data analysis report with synthetic
business data, showcasing practical usage for data science workflows.
"""

# Standard Library
import io
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

# Third Party
try:
    import matplotlib.pyplot as plt
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️  Matplotlib/NumPy not installed. Install with: pip install matplotlib numpy")

# Flowcard
import flowcard as fc


def generate_sales_data() -> Dict[str, List]:
    """Generate synthetic sales data for demonstration.
    
    Returns:
        Dictionary containing sales metrics over time.
    """
    # Generate 30 days of data
    dates = []
    sales = []
    customers = []
    
    base_date = datetime.now() - timedelta(days=30)
    
    for i in range(30):
        current_date = base_date + timedelta(days=i)
        dates.append(current_date.strftime("%Y-%m-%d"))
        
        # Simulate sales with weekend/weekday patterns
        if current_date.weekday() >= 5:  # Weekend
            daily_sales = random.randint(800, 1200)
            daily_customers = random.randint(40, 70)
        else:  # Weekday
            daily_sales = random.randint(1200, 2000)
            daily_customers = random.randint(60, 100)
        
        # Add some trend and noise
        trend_factor = 1 + (i * 0.01)  # Slight upward trend
        daily_sales = int(daily_sales * trend_factor)
        daily_customers = int(daily_customers * trend_factor)
        
        sales.append(daily_sales)
        customers.append(daily_customers)
    
    return {
        "dates": dates,
        "sales": sales,
        "customers": customers
    }


def create_sales_chart(data: Dict[str, List]) -> bytes:
    """Create a sales analysis visualization.
    
    Args:
        data: Dictionary containing sales data.
        
    Returns:
        PNG image data as bytes.
    """
    if not MATPLOTLIB_AVAILABLE:
        return b"sales_chart_placeholder"
    
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(12, 8))
    
    # Sales trend
    ax1.plot(range(len(data["sales"])), data["sales"], 
             color='green', linewidth=2, marker='o', markersize=4)
    ax1.set_title("Daily Sales Revenue ($)", fontsize=14, fontweight='bold')
    ax1.set_ylabel("Revenue ($)")
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    
    # Customer count
    ax2.plot(range(len(data["customers"])), data["customers"], 
             color='blue', linewidth=2, marker='s', markersize=4)
    ax2.set_title("Daily Customer Count", fontsize=14, fontweight='bold')
    ax2.set_xlabel("Days (Last 30)")
    ax2.set_ylabel("Customers")
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Convert to bytes
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='PNG', dpi=150, bbox_inches='tight')
    plt.close()
    
    return img_buffer.getvalue()


def calculate_metrics(data: Dict[str, List]) -> Dict[str, float]:
    """Calculate key business metrics.
    
    Args:
        data: Sales data dictionary.
        
    Returns:
        Dictionary of calculated metrics.
    """
    sales = data["sales"]
    customers = data["customers"]
    
    # Calculate revenue growth comparing last week to first week
    if MATPLOTLIB_AVAILABLE:
        first_week_avg = np.mean(sales[:7])
        last_week_avg = np.mean(sales[-7:])
        revenue_growth = ((last_week_avg / first_week_avg) - 1) * 100
    else:
        revenue_growth = 5.2  # Placeholder value
    
    return {
        "total_revenue": sum(sales),
        "avg_daily_revenue": sum(sales) / len(sales),
        "total_customers": sum(customers),
        "avg_daily_customers": sum(customers) / len(customers),
        "avg_order_value": sum(sales) / sum(customers),
        "max_daily_sales": max(sales),
        "min_daily_sales": min(sales),
        "revenue_growth": revenue_growth
    }


def main() -> None:
    """Create a comprehensive data analysis report."""
    print("📊 Creating Data Analysis Report...")
    
    # Generate synthetic data
    sales_data = generate_sales_data()
    metrics = calculate_metrics(data=sales_data)
    
    # Create FlowCard document
    card = fc.Flowcard()
    
    # Main title
    card.title("📈 Sales Performance Dashboard")
    
    # Add sales chart
    if MATPLOTLIB_AVAILABLE:
        chart_data = create_sales_chart(data=sales_data)
        card.image(image_data=chart_data)
        print("✅ Generated sales visualization")
    else:
        print("⚠️  Skipping chart generation (matplotlib not available)")
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Save the report
    card.save(filepath="output/sales_analysis_report.html")
    card.save(filepath="output/sales_analysis_report.md")
    
    print("✅ Sales Analysis Report completed!")
    print("📁 Generated files:")
    print("   - output/sales_analysis_report.html")
    print("   - output/sales_analysis_report.md")
    
    # Display key metrics
    print("\n💰 Key Metrics (Last 30 Days):")
    print(f"   - Total Revenue: ${metrics['total_revenue']:,.2f}")
    print(f"   - Average Daily Revenue: ${metrics['avg_daily_revenue']:,.2f}")
    print(f"   - Total Customers: {metrics['total_customers']:,}")
    print(f"   - Average Order Value: ${metrics['avg_order_value']:,.2f}")
    print(f"   - Highest Daily Sales: ${metrics['max_daily_sales']:,.2f}")
    print(f"   - Revenue Growth: {metrics['revenue_growth']:+.1f}%")


if __name__ == "__main__":
    main()