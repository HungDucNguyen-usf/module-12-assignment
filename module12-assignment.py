# Module 12 Assignment: Business Analytics Fundamentals and Applications
# GreenGrocer Data Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Welcome message
print("=" * 60)
print("GREENGROCER BUSINESS ANALYTICS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Set seed for reproducibility
np.random.seed(42)

# Store information
stores = ["Tampa", "Orlando", "Miami", "Jacksonville", "Gainesville"]
store_data = {
    "Store": stores,
    "SquareFootage": [15000, 12000, 18000, 10000, 8000],
    "StaffCount": [45, 35, 55, 30, 25],
    "YearsOpen": [5, 3, 7, 2, 1],
    "WeeklyMarketingSpend": [2500, 2000, 3000, 1800, 1500]
}

# Create store dataframe
store_df = pd.DataFrame(store_data)

# Product categories and departments
departments = ["Produce", "Dairy", "Bakery", "Grocery", "Prepared Foods"]
categories = {
    "Produce": ["Organic Vegetables", "Organic Fruits", "Fresh Herbs"],
    "Dairy": ["Milk & Cream", "Cheese", "Yogurt"],
    "Bakery": ["Bread", "Pastries", "Cakes"],
    "Grocery": ["Grains", "Canned Goods", "Snacks"],
    "Prepared Foods": ["Hot Bar", "Salad Bar", "Sandwiches"]
}

# Generate sales data for each store
sales_data = []
dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")

# Base performance factors for each store (relative scale)
store_performance = {
    "Tampa": 1.0, 
    "Orlando": 0.85, 
    "Miami": 1.2, 
    "Jacksonville": 0.75, 
    "Gainesville": 0.65
}

# Base performance factors for each department (relative scale)
dept_performance = {
    "Produce": 1.2,
    "Dairy": 1.0,
    "Bakery": 0.85,
    "Grocery": 0.95,
    "Prepared Foods": 1.1
}

# Generate daily sales data for each store, department, and category
for date in dates:
    # Seasonal factor (higher in summer and December)
    month = date.month
    seasonal_factor = 1.0
    if month in [6, 7, 8]:  # Summer
        seasonal_factor = 1.15
    elif month == 12:  # December
        seasonal_factor = 1.25
    elif month in [1, 2]:  # Winter
        seasonal_factor = 0.9
    
    # Day of week factor (weekends are busier)
    dow_factor = 1.3 if date.dayofweek >= 5 else 1.0  # Weekend vs weekday
    
    for store in stores:
        store_factor = store_performance[store]
        
        for dept in departments:
            dept_factor = dept_performance[dept]
            
            for category in categories[dept]:
                # Base sales amount
                base_sales = np.random.normal(loc=500, scale=100)
                
                # Calculate final sales with all factors and some randomness
                sales_amount = base_sales * store_factor * dept_factor * seasonal_factor * dow_factor
                sales_amount = sales_amount * np.random.normal(loc=1.0, scale=0.1)  # Add noise
                
                # Calculate profit margin (different base margins for departments)
                base_margin = {
                    "Produce": 0.25,
                    "Dairy": 0.22,
                    "Bakery": 0.35,
                    "Grocery": 0.20,
                    "Prepared Foods": 0.40
                }[dept]
                profit_margin = base_margin * np.random.normal(loc=1.0, scale=0.05)
                profit_margin = max(min(profit_margin, 0.5), 0.15)  # Keep within reasonable range
                
                # Calculate profit
                profit = sales_amount * profit_margin
                
                # Add record
                sales_data.append({
                    "Date": date,
                    "Store": store,
                    "Department": dept,
                    "Category": category,
                    "Sales": round(sales_amount, 2),
                    "ProfitMargin": round(profit_margin, 4),
                    "Profit": round(profit, 2)
                })

# Create sales dataframe
sales_df = pd.DataFrame(sales_data)

# Generate customer data
customer_data = []
total_customers = 5000

# Age distribution parameters
age_mean, age_std = 42, 15

# Income distribution parameters (in $1000s)
income_mean, income_std = 85, 30

# Create customer segments (will indirectly influence spending)
segments = ["Health Enthusiast", "Gourmet Cook", "Family Shopper", "Budget Organic", "Occasional Visitor"]
segment_probabilities = [0.25, 0.20, 0.30, 0.15, 0.10]

# Store preference probabilities (matches store performance somewhat)
store_probs = {
    "Tampa": 0.25,
    "Orlando": 0.20,
    "Miami": 0.30,
    "Jacksonville": 0.15,
    "Gainesville": 0.10
}

for i in range(total_customers):
    # Basic demographics
    age = int(np.random.normal(loc=age_mean, scale=age_std))
    age = max(min(age, 85), 18)  # Keep age in reasonable range
    
    gender = np.random.choice(["M", "F"], p=[0.48, 0.52])
    
    income = int(np.random.normal(loc=income_mean, scale=income_std))
    income = max(income, 20)  # Minimum income
    
    # Customer segment
    segment = np.random.choice(segments, p=segment_probabilities)
    
    # Preferred store
    preferred_store = np.random.choice(stores, p=list(store_probs.values()))
    
    # Shopping behavior - influenced by segment
    if segment == "Health Enthusiast":
        visit_frequency = np.random.randint(8, 15)  # Visits per month
        avg_basket = np.random.normal(loc=75, scale=15)
    elif segment == "Gourmet Cook":
        visit_frequency = np.random.randint(4, 10)
        avg_basket = np.random.normal(loc=120, scale=25)
    elif segment == "Family Shopper":
        visit_frequency = np.random.randint(5, 12)
        avg_basket = np.random.normal(loc=150, scale=30)
    elif segment == "Budget Organic":
        visit_frequency = np.random.randint(6, 10)
        avg_basket = np.random.normal(loc=60, scale=10)
    else:  # Occasional Visitor
        visit_frequency = np.random.randint(1, 5)
        avg_basket = np.random.normal(loc=45, scale=15)
    
    # Ensure values are reasonable
    visit_frequency = max(min(visit_frequency, 30), 1)
    avg_basket = max(avg_basket, 15)
    
    # Loyalty tier based on combination of frequency and spending
    monthly_spend = visit_frequency * avg_basket
    if monthly_spend > 1000:
        loyalty_tier = "Platinum"
    elif monthly_spend > 500:
        loyalty_tier = "Gold"
    elif monthly_spend > 200:
        loyalty_tier = "Silver"
    else:
        loyalty_tier = "Bronze"
    
    # Add to customer data
    customer_data.append({
        "CustomerID": f"C{i+1:04d}",
        "Age": age,
        "Gender": gender,
        "Income": income * 1000,  # Convert to actual income
        "Segment": segment,
        "PreferredStore": preferred_store,
        "VisitsPerMonth": visit_frequency,
        "AvgBasketSize": round(avg_basket, 2),
        "MonthlySpend": round(visit_frequency * avg_basket, 2),
        "LoyaltyTier": loyalty_tier
    })

# Create customer dataframe
customer_df = pd.DataFrame(customer_data)

# Create some calculated operational metrics for stores
operational_data = []

for store in stores:
    # Get store details
    store_row = store_df[store_df["Store"] == store].iloc[0]
    square_footage = store_row["SquareFootage"]
    staff_count = store_row["StaffCount"]
    
    # Calculate store metrics
    store_sales = sales_df[sales_df["Store"] == store]["Sales"].sum()
    store_profit = sales_df[sales_df["Store"] == store]["Profit"].sum()
    
    # Calculate derived metrics
    sales_per_sqft = store_sales / square_footage
    profit_per_sqft = store_profit / square_footage
    sales_per_staff = store_sales / staff_count
    inventory_turnover = np.random.uniform(12, 18) * store_performance[store]
    customer_satisfaction = min(5, np.random.normal(loc=4.0, scale=0.3) * 
                                (store_performance[store] ** 0.5))
    
    # Add to operational data
    operational_data.append({
        "Store": store,
        "AnnualSales": round(store_sales, 2),
        "AnnualProfit": round(store_profit, 2),
        "SalesPerSqFt": round(sales_per_sqft, 2),
        "ProfitPerSqFt": round(profit_per_sqft, 2),
        "SalesPerStaff": round(sales_per_staff, 2),
        "InventoryTurnover": round(inventory_turnover, 2),
        "CustomerSatisfaction": round(customer_satisfaction, 2)
    })

# Create operational dataframe
operational_df = pd.DataFrame(operational_data)

# Print data info
print("\nDataframes created successfully. Ready for analysis!")
print(f"Sales data shape: {sales_df.shape}")
print(f"Customer data shape: {customer_df.shape}")
print(f"Store data shape: {store_df.shape}")
print(f"Operational data shape: {operational_df.shape}")

# Print sample of each dataframe
print("\nSales Data Sample:")
print(sales_df.head(3))
print("\nCustomer Data Sample:")
print(customer_df.head(3))
print("\nStore Data Sample:")
print(store_df)
print("\nOperational Data Sample:")
print(operational_df)
# ----- END OF DATA CREATION -----


# TODO 1: Descriptive Analytics - Overview of Current Performance
# 1.1 Calculate and display basic descriptive statistics for sales and profit
# REQUIRED: Store results in variables for testing
def analyze_sales_performance():
    """
    Analyze overall sales performance with descriptive statistics
    REQUIRED: Create and return dictionary with keys:
    - 'total_sales': float
    - 'total_profit': float
    - 'avg_profit_margin': float
    - 'sales_by_store': pandas Series
    - 'sales_by_dept': pandas Series
    """
    # Your code here
    total_sales = sales_df["Sales"].sum() #sum of sales
    total_profit = sales_df["Profit"].sum() #sum profit
    avg_profit_margin = sales_df["ProfitMargin"].mean() #mean of margin
    sales_by_store = sales_df.groupby("Store")["Sales"].sum() #group by store, then sum
    sales_by_dept = sales_df.groupby("Department")["Sales"].sum() #group by department, then sum
    
    print(f"Total sales: ${total_sales:,.2f}") #make it looks nicer
    print(f"Total profit: ${total_profit:,.2f}")#make it looks nicer
    print(f"Average profit margin: {avg_profit_margin:.2%}")#make it looks nicer
    print(f"Sales by store:") #put the df below for cleanliness
    print(sales_by_store)
    print(f"Sales by departments:")#put the df below for cleanliness
    print(sales_by_dept)
    return { #return the dict
        'total_sales': total_sales,
        'total_profit': total_profit,
        'avg_profit_margin': avg_profit_margin,
        'sales_by_store': sales_by_store,
        'sales_by_dept': sales_by_dept
        }
# 1.2 Create visualizations showing sales distribution by store, department, and time
# REQUIRED: Return matplotlib figures
def visualize_sales_distribution():
    """
    Create visualizations showing how sales are distributed
    REQUIRED: Return tuple of three figures (store_fig, dept_fig, time_fig)
    """
    # Your code here
    store_fig, ax = plt.subplots() 
    store_sales = sales_df.groupby("Store")["Sales"].sum() #make a df for each store group and its sales
    store_sales.plot(kind = "bar", ax = ax) #plot, bar, using the ax
    ax.set_title("Sales by Store")
    ax.set_xlabel("Store")
    ax.set_ylabel("Sales ($)")
    ax.tick_params(axis="x", rotation=0)
    plt.tight_layout()
    
    dept_fig, ax = plt.subplots() #similar to above, group each department and total sales
    dept_sales = sales_df.groupby("Department")["Sales"].sum()
    dept_sales.plot(kind = "bar", ax = ax)
    ax.set_title("Sales by Departments")
    ax.set_xlabel("Department")
    ax.set_ylabel("Sales ($)")
    ax.tick_params(axis="x", rotation=0)
    plt.tight_layout()
    
    time_fig, ax = plt.subplots() #group each month
    sales_per_month = sales_df.groupby(sales_df["Date"].dt.month)["Sales"].sum()
    sales_per_month.plot(kind = "bar", ax = ax)
    ax.set_title("Sales by Months")
    ax.set_xlabel("Months")
    ax.set_ylabel("Sales ($)")
    ax.tick_params(axis="x", rotation=0)
    plt.tight_layout()

    return (store_fig, dept_fig, time_fig)
    

# 1.3 Analyze customer segments and their spending patterns
# REQUIRED: Return analysis results
def analyze_customer_segments():
    """
    Analyze customer segments and their relationship to spending
    REQUIRED: Return dictionary with keys:
    - 'segment_counts': pandas Series
    - 'segment_avg_spend': pandas Series
    - 'segment_loyalty': pandas DataFrame
    """
    # Your code here
    segment_counts = customer_df["Segment"].value_counts() #count the total values in each segment
    #group by the segments and take the mean of the spending
    segment_avg_spend = customer_df.groupby("Segment")["MonthlySpend"].mean()
    #crosstab, make a DF on segment and loyalty tier
    segment_loyalty = pd.crosstab(customer_df["Segment"],customer_df["LoyaltyTier"]) 
    print("Segment counts:")
    print(segment_counts)
    print("Average segment spending:")
    print(segment_avg_spend)
    print("average segment loyalty")
    print(segment_loyalty)
    
    return{
        "segment_counts": segment_counts,
        "segment_avg_spend": segment_avg_spend,
        "segment_loyalty": segment_loyalty
        }
# TODO 2: Diagnostic Analytics - Understanding Relationships
# 2.1 Identify factors correlated with sales performance
# REQUIRED: Return correlation results
def analyze_sales_correlations():
    """
    Analyze correlations between various factors and sales performance
    REQUIRED: Return dictionary with keys:
    - 'store_correlations': pandas DataFrame
    - 'top_correlations': list of tuples (factor, correlation)
    - 'correlation_fig': matplotlib figure
    """
    # Your code here
    #Merge the store df with the operational df on the store to see the correlations for it
    store_factors_performance_df = pd.merge(store_df, operational_df, on = "Store")
    #correlate only the numeric values
    correlation = store_factors_performance_df.corr(numeric_only = True)
    #take a annual sales to see the top  highest correlations
    annual_sales_corr = correlation["AnnualSales"].sort_values(ascending = False)
    #make a list for the top 5 correlations
    top_corr = list(annual_sales_corr.drop(["AnnualSales", "AnnualProfit", "ProfitPerSqFt", "SalesPerSqFt", "SalesPerStaff"]).head(5).items())
    #creating a plot
    fig, ax = plt.subplots(figsize=(10, 5))
    #drop the annual profit and sales since they don't contribute to the sales itself
    annual_sales_corr.drop(["AnnualSales", "AnnualProfit", "ProfitPerSqFt", "SalesPerSqFt", "SalesPerStaff"]).plot(kind="bar", ax=ax)
    ax.set_title("Correlations by stores")
    ax.set_xlabel("Factors")
    ax.set_ylabel("Coefficient")
    ax.tick_params(axis="x", rotation=0)
    plt.tight_layout()
    
    print("Top correlations with Annual Sales:")
    for factor, corr in top_corr:
        print(f"-{factor}: {corr:.5f}")
    
    return {
    "store_correlations": correlation,
    "top_correlations": top_corr,
    "correlation_fig": fig
    }

# 2.2 Compare stores based on operational metrics
# REQUIRED: Return comparison results
def compare_store_performance():
    """
    Compare stores across different operational metrics
    REQUIRED: Return dictionary with keys:
    - 'efficiency_metrics': pandas DataFrame (with SalesPerSqFt, SalesPerStaff)
    - 'performance_ranking': pandas Series (ranked by profit)
    - 'comparison_fig': matplotlib figure
    """
    # Your code here
    #efficiency metrics is counted with salespersqft, salesperstagg with store
    eff_metrics = operational_df[["Store", "SalesPerSqFt", "SalesPerStaff"]]
    #rank performance based on annual profit from the top down
    performance_ranking = operational_df.set_index("Store")["AnnualProfit"].sort_values(ascending=False)
    #creating a plot
    fig, ax = plt.subplots(1,2,figsize = (12,5))
    #get a sales per sq ft for stores
    eff_metrics.set_index("Store")["SalesPerSqFt"].plot(kind="bar", ax=ax[0])
    ax[0].set_title("Sales ($) per Sq Ft")
    ax[0].set_xlabel("Store")
    ax[0].set_ylabel("Sales ($)")
    ax[0].tick_params(axis="x", rotation=0)
    #get a sales per staff for stores
    eff_metrics.set_index("Store")["SalesPerStaff"].plot(kind="bar", ax=ax[1])
    ax[1].set_title("Sales ($) per Staff")
    ax[1].set_xlabel("Store")
    ax[1].set_ylabel("Sales ($)")
    ax[1].tick_params(axis="x", rotation=0)
    plt.tight_layout()
    
    print("Performance Ranking by Profit:")
    print(performance_ranking)
    
    return {
    "efficiency_metrics": eff_metrics,
    "performance_ranking": performance_ranking,
    "comparison_fig": fig
    }

# 2.3 Analyze seasonal patterns and their impact
# REQUIRED: Return seasonal analysis
def analyze_seasonal_patterns():
    """
    Identify and visualize seasonal patterns in sales data
    REQUIRED: Return dictionary with keys:
    - 'monthly_sales': pandas Series
    - 'dow_sales': pandas Series (day of week)
    - 'seasonal_fig': matplotlib figure
    """
    # Your code here
    #group the monthly sales by extracting the months
    monthly_sales = sales_df.groupby(sales_df["Date"].dt.month)["Sales"].sum()
    #group the day of the week sales by extracting the DOW
    dow_sales = sales_df.groupby(sales_df["Date"].dt.dayofweek)["Sales"].sum()
    #creating subplots
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    #plot monthly sales
    monthly_sales.plot(kind="bar", ax=ax[0])
    ax[0].set_title("Monthly sales")
    ax[0].set_xlabel("Months of years")
    ax[0].set_ylabel("Sales ($)")
    ax[0].tick_params(axis="x", rotation=0)
    #plot dow sales
    dow_sales.plot(kind="bar", ax=ax[1])
    ax[1].set_title("Day of week sales")
    ax[1].set_xlabel("Day of week")
    ax[1].set_ylabel("Sales ($)")
    ax[1].tick_params(axis="x", rotation=0)
    plt.tight_layout()
    
    print("Monthly Sales:")
    print(monthly_sales)
    print("Day of Week Sales:")
    print(dow_sales)
    
    return {
    "monthly_sales": monthly_sales,
    "dow_sales": dow_sales,
    "seasonal_fig": fig
    }
# TODO 3: Predictive Analytics - Basic Forecasting
# 3.1 Create a simple linear regression model to predict store sales
# REQUIRED: Return model results
def predict_store_sales():
    """
    Use linear regression to predict store sales based on store characteristics
    REQUIRED: Return dictionary with keys:
    - 'coefficients': dict (feature: coefficient)
    - 'r_squared': float
    - 'predictions': pandas Series
    - 'model_fig': matplotlib figure
    """
    # Your code here
    #merge the df to have the sales and its factors
    sales_charac_df = pd.merge(store_df, operational_df, on="Store")
    #get x as the staff count prediction
    x = sales_charac_df["StaffCount"]
    #y as the sales
    y = sales_charac_df["AnnualSales"]
    #scipy lingress for stats
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    #get the r^2 value
    r_squared = r_value ** 2
    #make a prediction line y = ax + b
    predictions = slope * x + intercept
    #scatter plot the graph
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(x, y, label="Reality", color="blue") #rgb, reality vs prediction
    ax.plot(x, predictions, label="Prediction", color="red")
    ax.set_title(f"Sales Prediction (R²={r_squared:.3f})")
    ax.set_xlabel("Staff Count")
    ax.set_ylabel("Annual Sales ($)")
    ax.legend()
    plt.tight_layout()
    
    print(f"Slope: {slope:,.2f}")
    print(f"Intercept: {intercept:,.2f}")
    print(f"R-squared: {r_squared:.3f}")
    
    return {
        "coefficients": {"StaffCount": slope, "intercept": intercept},
        "r_squared": r_squared,
        "predictions": predictions,
        "model_fig": fig
    }
# 3.2 Forecast departmental sales trends
# REQUIRED: Return forecast results
def forecast_department_sales():
    """
    Analyze and forecast departmental sales trends
    REQUIRED: Return dictionary with keys:
    - 'dept_trends': pandas DataFrame
    - 'growth_rates': pandas Series
    - 'forecast_fig': matplotlib figure
    """
    # Your code here
    #get the total sales of the df that's grouped by month and departments to see the trends
    #ustack so that the department becomes a row with multiple columns of each department having the sales values
    dept_trends = sales_df.groupby([sales_df["Date"].dt.month, "Department"])["Sales"].sum().unstack()
    #get the first and last month
    first_month = dept_trends.loc[1]
    last_month = dept_trends.loc[12]
    #calculate growth rate
    growth_rate = (last_month - first_month)/first_month
    #plot
    fig, ax = plt.subplots()
    #plot the line
    dept_trends.plot(kind="line", ax=ax)
    ax.set_title("Forcast for department trends")
    ax.set_xlabel("Month")
    ax.set_ylabel("Sales ($)")
    ax.legend()
    plt.tight_layout()
    
    print("Department Growth Rates:")
    print(growth_rate)
    
    return {
        "dept_trends": dept_trends,
        "growth_rates" : growth_rate,
        "forecast_fig": fig
        }

# TODO 4: Integrated Analysis - Business Insights and Recommendations
# 4.1 Identify the most profitable combinations of store, department, and customer segments
# REQUIRED: Return opportunity analysis
def identify_profit_opportunities():
    """
    Identify the most profitable combinations and potential opportunities
    REQUIRED: Return dictionary with keys:
    - 'top_combinations': pandas DataFrame (top 10 store-dept combinations)
    - 'underperforming': pandas DataFrame (bottom 10)
    - 'opportunity_score': pandas Series (by store)
    """
    # Your code here
    #top combination = get the sum of profit after grouped, reset index to fix it from a series to a df
    top_comb = sales_df.groupby(["Store", "Department"])["Profit"].sum().reset_index()
    #sort them descending top to bot
    top_comb_sorted = top_comb.sort_values("Profit", ascending=False)
    #get the best 10 and worst 10
    top_combinations = top_comb_sorted.head(10)
    underperforming = top_comb_sorted.tail(10)
    #check the store profit, sort to make it look cleaner
    oppo_score = sales_df.groupby("Store")["Profit"].sum().sort_values(ascending=False)
    
    print("Top 10 Store-Department combinations:")
    print(top_combinations)
    print("\nBottom 10 underperforming combinations:")
    print(underperforming)
    
    return {
        "top_combinations":top_combinations,
        "underperforming":underperforming,
        "opportunity_score":oppo_score
        }
    
# 4.2 Develop recommendations for improving performance
# REQUIRED: Return list of recommendations
def develop_recommendations():
    """
    Develop actionable recommendations based on the analysis
    REQUIRED: Return list of at least 5 recommendation strings
    """
    # Your code here
    rec = []
    rec.append("Gainesville is the worst performing store, improve the Bakery and Produce departments")
    rec.append("Produce is the best performing department, focus more on it")
    rec.append("The weekend is when people go and purchase the most, get more advertisements, deals on weekend")
    rec.append("Family Shopper Segment is has the most Platinum loyalty tier, give them more deals, discounts, tend to them")
    rec.append("Family Shopper Segment is also the highest spending segment, focus more on them")
    
    print("Recommendations:")
    for i, r in enumerate(rec, 1):
        print(f"  {i}. {r}")
    
    return rec

# TODO 5: Summary Report
# REQUIRED: Generate comprehensive summary
def generate_executive_summary():
    """
    Generate an executive summary of key findings and recommendations
    REQUIRED: Print executive summary with sections:
    - Overview (1 paragraph)
    - Key Findings (3-5 bullet points)
    - Recommendations (3-5 bullet points)
    - Expected Impact (1 paragraph)
    """
    # Your code here
    print("\nOVERVIEW:")
    print("GreenGrocer is a franchise of organic grocery stores across Florida, this is the findings from their data in the past year")
    print("\nKEY FINDINGS:")
    print("o The store in Miami makes the highest profit in the past year")
    print("o Family Shopper Segment makes up the most spending")
    print("o Produce and Prepared Foods are the highest sales departments")
    print("o The franchise has made 4 million dollars in profit")
    print("\nRECOMMENDATIONS:")
    print("o Get more advertisements, deals on weekend")
    print("o Invest in Gainesville's Bakery and Produce departments to close the performance gap")
    print("o Focus more on Family Shopper Segment")
    print("\nEXPECTED IMPACT:")
    print("these recommendations will not only improve the weakest link - Gainsville - to improve overall sales, but also make sure that the highest paying customers and departments are being improved to generate more impact")
    
# Main function to execute all analyses
# REQUIRED: Do not modify function name
def main():
    print("\n" + "=" * 60)
    print("GREENGROCER BUSINESS ANALYTICS RESULTS")
    print("=" * 60)
    
    # Execute analyses in a logical order
    # REQUIRED: Store all results for potential testing
    
    print("\n--- DESCRIPTIVE ANALYTICS: CURRENT PERFORMANCE ---")
    sales_metrics = analyze_sales_performance()
    dist_figs = visualize_sales_distribution()
    customer_analysis = analyze_customer_segments()
    
    print("\n--- DIAGNOSTIC ANALYTICS: UNDERSTANDING RELATIONSHIPS ---")
    correlations = analyze_sales_correlations()
    store_comparison = compare_store_performance()
    seasonality = analyze_seasonal_patterns()
    
    print("\n--- PREDICTIVE ANALYTICS: FORECASTING ---")
    sales_model = predict_store_sales()
    dept_forecast = forecast_department_sales()
    
    print("\n--- BUSINESS INSIGHTS AND RECOMMENDATIONS ---")
    opportunities = identify_profit_opportunities()
    recommendations = develop_recommendations()
    
    print("\n--- EXECUTIVE SUMMARY ---")
    generate_executive_summary()
    
    # Show all figures
    plt.show()
    
    # Return results for testing purposes
    return {
        'sales_metrics': sales_metrics,
        'customer_analysis': customer_analysis,
        'correlations': correlations,
        'store_comparison': store_comparison,
        'seasonality': seasonality,
        'sales_model': sales_model,
        'dept_forecast': dept_forecast,
        'opportunities': opportunities,
        'recommendations': recommendations
    }

# Run the main function
if __name__ == "__main__":
    results = main()