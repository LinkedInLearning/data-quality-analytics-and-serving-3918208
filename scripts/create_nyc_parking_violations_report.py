import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import sys
sys.path.append("..")

from scripts.utils import DuckdbUtils
duckdb_utils = DuckdbUtils()


class NYC_Parking_Violations_Report:
    """
    A comprehensive reporting tool for NYC parking violations data analysis.
    
    This class generates and visualizes a set of metrics derived from NYC
    parking violation data stored in a data warehouse. It uses SQL queries to
    retrieve processed data from gold-level tables and creates various
    visualizations including tables, bar charts, and heatmaps to provide
    insights into parking violation patterns.
    
    The report includes metrics such as:
    - Recent parking tickets details
    - Ticket counts by county, violation type, issuing agency, and vehicle
    - Total fees collected and breakdown by precinct
    - Time-series analysis of tickets (monthly and weekly)
    - Fee metrics by issuing agency
    - Day-of-week pattern analysis using heatmaps
    
    Each metric is generated independently through dedicated methods and can be 
    combined into a comprehensive report using the create_report() method.
    
    The class uses matplotlib and seaborn for visualizations and depends on 
    a utility function 'duckdb_utils.run_sql_query_and_return_df' to fetch data from the
    database.
    """
    def __init__(self):
        self.metric_a_title = 'Metric A: 10 Latest Tickets'
        self.metric_a = 'SELECT * FROM gold_latest_tickets_90_days LIMIT 10'

        self.metric_b_title = 'Metric B: Top 10 Ticket Counts by County - Past 90 Days'
        self.metric_b = 'SELECT * FROM gold_tickets_by_county_90_days LIMIT 10'

        self.metric_c_title = 'Metric C: Top 10 Ticket Counts by Violation Type - Past 90 Days'
        self.metric_c = 'SELECT * FROM gold_tickets_by_violation_90_days LIMIT 10'

        self.metric_d_title = 'Metric D: Top 10 Ticket Counts by Issuing Agency - Past 90 Days'
        self.metric_d = 'SELECT * FROM gold_tickets_by_agency_90_days LIMIT 10'

        self.metric_e_title = 'Metric E: Top 10 Ticket Counts by Vehicle - Past 90 Days'
        self.metric_e = 'SELECT * FROM gold_tickets_by_vehicle_90_days LIMIT 10'

        self.metric_f_title = 'Metric F: Total Fees - Past 90 Days'
        self.metric_f = 'SELECT SUM(total_ticket_fees_usd) AS total_fees_90_days FROM gold_precinct_ticket_fee_sum_90_days'

        self.metric_g_title = 'Metric G: Top 10 Total Fees by Precinct - Past 90 Days'
        self.metric_g = 'SELECT * FROM gold_precinct_ticket_fee_sum_90_days LIMIT 10'

        self.metric_h_title = 'Metric H: 2023 Ticket Over Time (Monthly)'
        self.metric_h = 'SELECT * FROM gold_2023_ticket_counts_year_month'

        self.metric_i_title = 'Metric I: 2023 Ticket Over Time (Weekly)'
        self.metric_i = 'SELECT * FROM gold_2023_ticket_counts_year_week WHERE year_week NOT IN (\'2023-W52\', \'2023-W35\')'

        self.metric_j_title = 'Metric J: Fee Summaries by Agency - Past 90 Days'
        self.metric_j = 'SELECT * FROM gold_2023_agency_fee_metrics WHERE ticket_count >= 100'

        self.metric_k_title = 'Metric K: Weekly Violation Heatmap by Day of Week'
        self.metric_k = 'SELECT * FROM gold_2023_weekly_violations_day_of_week_heatmap WHERE year_week != \'2023-W52\''

        self.metric_l_title = 'Metric L: Precinct Violation Heatmap by Day of Week'
        self.metric_l = 'SELECT * FROM gold_2023_county_violations_day_of_week_heatmap'

        self.metric_m_title = 'Metric M: Violation Heatmap by Day of Week'
        self.metric_m = 'SELECT * FROM gold_2023_violations_day_of_week_heatmap'

    def create_metric_a(self):
        df = duckdb_utils.run_sql_query_and_return_df(self.metric_a)
        print('Metric A: Ten Latest Tickets')
        display(df)

    def create_metric_b(self):
        county_data = duckdb_utils.run_sql_query_and_return_df(self.metric_b)
        plt.figure(figsize=(12, 8))

        ax = sns.barplot(
            x='ticket_count', 
            y='violation_county',
            hue='violation_county',
            legend=False,
            data=county_data,
            palette='viridis'
        )
        plt.suptitle(self.metric_b_title, fontsize=16)
        plt.title('Counties', fontsize=14, pad=20)
        plt.xlabel('Number of Tickets', fontsize=14)
        plt.ylabel('County', fontsize=14)

        # Add the count values to the end of each bar
        for i, v in enumerate(county_data['ticket_count']):
            ax.text(v + 50, i, str(v), va='center', fontweight='bold')

        plt.grid(axis='x', alpha=0.3)
        plt.tight_layout(rect=[0, 0, 1, 0.96])

        plt.show()

    def create_metric_c(self):
        violation_data = duckdb_utils.run_sql_query_and_return_df(self.metric_c)

        plt.figure(figsize=(14, 10))
        ax = sns.barplot(
            x='ticket_count', 
            y='violation_definition',
            hue='violation_definition',
            legend=False,
            data=violation_data,
            palette='viridis'
        )

        plt.suptitle(self.metric_c_title, fontsize=16)
        plt.title('Violation', fontsize=14, pad=20)

        plt.xlabel('Number of Tickets', fontsize=14)
        plt.ylabel('Violation Type', fontsize=14)

        # Add the count values to the end of each bar
        for i, v in enumerate(violation_data['ticket_count']):
            ax.text(v + 100, i, str(v), va='center', fontweight='bold')

        # Add grid for better readability
        plt.grid(axis='x', alpha=0.3)

        # Ensure tight layout to accommodate the long text labels and titles
        plt.tight_layout(rect=[0, 0, 1, 0.96])

        # Show the plot
        plt.show()

    def create_metric_d(self):
        # Run the SQL query to get the data
        agency_data = duckdb_utils.run_sql_query_and_return_df(self.metric_d)

        # Set the figure size for better visualization
        plt.figure(figsize=(12, 8))

        # Create horizontal bar chart with Seaborn - using the updated approach with hue
        ax = sns.barplot(
            x='ticket_count', 
            y='issuing_agency',
            hue='issuing_agency',
            legend=False,
            data=agency_data,
            palette='viridis'
        )

        # Add two titles: the metric title at the top and a simpler title
        plt.suptitle(self.metric_d_title, fontsize=16)
        plt.title('Issuing Agencies', fontsize=14, pad=20)

        plt.xlabel('Number of Tickets', fontsize=14)
        plt.ylabel('Issuing Agency', fontsize=14)

        # Add the count values to the end of each bar
        for i, v in enumerate(agency_data['ticket_count']):
            ax.text(v + 200, i, str(v), va='center', fontweight='bold')

        # Add grid for better readability
        plt.grid(axis='x', alpha=0.3)

        # Ensure tight layout to accommodate the titles
        plt.tight_layout(rect=[0, 0, 1, 0.96])

        # Show the plot
        plt.show()

    def create_metric_e(self):
        # Run the SQL query to get the data
        vehicle_data = duckdb_utils.run_sql_query_and_return_df(self.metric_e)

        # Set the figure size for better visualization
        plt.figure(figsize=(14, 9))

        # Create a combined label for the y-axis that includes make, plate type, and state
        vehicle_data['vehicle_label'] = vehicle_data.apply(
            lambda row: f"{row['vehicle_make']} - {row['plate_type']} ({row['registration_state']})", 
            axis=1
        )

        # Create horizontal bar chart with Seaborn
        ax = sns.barplot(
            x='ticket_count', 
            y='vehicle_label',
            hue='vehicle_label',
            legend=False,
            data=vehicle_data,
            palette='viridis'
        )

        # Add titles
        plt.suptitle(self.metric_e_title, fontsize=16)
        plt.title('Vehicles by Make, Plate Type, and State', fontsize=14, pad=20)

        plt.xlabel('Number of Tickets', fontsize=14)
        plt.ylabel('Vehicle Information', fontsize=14)

        # Add the count values to the end of each bar
        for i, v in enumerate(vehicle_data['ticket_count']):
            ax.text(v + 30, i, str(v), va='center', fontweight='bold')

        # Add grid for better readability
        plt.grid(axis='x', alpha=0.3)

        # Ensure tight layout
        plt.tight_layout(rect=[0, 0, 1, 0.96])

        # Show the plot
        plt.show()

    def create_metric_f(self):
        # Run the SQL query to get the data
        fees_data = duckdb_utils.run_sql_query_and_return_df(self.metric_f)

        # Extract the total fee value
        total_fees = fees_data['total_fees_90_days'].iloc[0]

        # Format the number with commas and dollar sign
        formatted_fees = f"${total_fees:,.2f}"

        # Create a figure with a clean, minimal design
        fig, ax = plt.subplots(figsize=(10, 6))

        # Hide axes
        ax.axis('off')

        # Add the title at the top
        ax.text(0.5, 0.85, self.metric_f_title, 
                horizontalalignment='center',
                fontsize=16, 
                fontweight='bold')

        # Add the big number in the center
        ax.text(0.5, 0.5, formatted_fees, 
                horizontalalignment='center',
                fontsize=48, 
                fontweight='bold', 
                color='darkgreen')

        # Add a subtle label below
        ax.text(0.5, 0.35, "Total Ticket Revenue", 
                horizontalalignment='center',
                fontsize=14,
                color='gray')

        # Add a border around the figure
        plt.rcParams['axes.linewidth'] = 2
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color('lightgray')

        # Set figure background color
        fig.patch.set_facecolor('white')

        plt.tight_layout()
        plt.show()

    def create_metric_g(self):
        # Run the SQL query to get the data for Metric G
        precinct_fees_data = duckdb_utils.run_sql_query_and_return_df(self.metric_g)

        # Find the appropriate columns
        fee_column = None
        precinct_column = None

        # Look for fee column
        for col in precinct_fees_data.columns:
            if 'fee' in col.lower() or 'sum' in col.lower() or 'amount' in col.lower() or 'total' in col.lower():
                fee_column = col
                break

        # Look for precinct column
        for col in precinct_fees_data.columns:
            if 'precinct' in col.lower() or 'district' in col.lower():
                precinct_column = col
                break

        # Sort data by fee amount in descending order
        precinct_fees_data = precinct_fees_data.sort_values(by=fee_column, ascending=False)

        # Create a clean figure with a reasonable size
        plt.figure(figsize=(12, 8))

        # Create y positions for the bars
        y_pos = range(len(precinct_fees_data))

        # Use the viridis colormap to match the style of other charts
        chart_colors = plt.cm.viridis(np.linspace(0, 0.9, len(precinct_fees_data)))

        # Create a horizontal bar chart using the numeric positions
        bars = plt.barh(y_pos, precinct_fees_data[fee_column], color=chart_colors)

        # Set the y-tick labels to be the precinct names
        plt.yticks(y_pos, precinct_fees_data[precinct_column])

        # Add a main title and a subtitle
        plt.suptitle(self.metric_g_title, fontsize=16)
        plt.title('Precincts', fontsize=14, pad=20)

        # Add axis labels with a larger font size
        plt.xlabel('Total Fees ($)', fontsize=14)
        plt.ylabel('Precinct', fontsize=14)

        # Add grid lines for better readability
        plt.grid(axis='x', alpha=0.3)

        # Add the fee values at the end of each bar with bold text
        for i, fee in enumerate(precinct_fees_data[fee_column]):
            plt.text(
                fee + (precinct_fees_data[fee_column].max() * 0.02),
                i,
                f"${fee:,.0f}",
                va='center',
                fontweight='bold'
            )

        # Handle large numbers appropriately
        if precinct_fees_data[fee_column].max() > 500000:
            # Use FuncFormatter to avoid ScalarFormatter issues
            def currency_formatter(x, pos):
                """Format large numbers as compact currency with appropriate suffix"""
                if x >= 1e6:
                    return f'${x*1e-6:.1f}M'
                elif x >= 1e3:
                    return f'${x*1e-3:.0f}K'
                else:
                    return f'${x:.0f}'

            plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(currency_formatter))

        # Ensure tight layout with room for the suptitle
        plt.tight_layout(rect=[0, 0, 1, 0.96])

        # Show the plot
        plt.show()

    def create_metric_h(self):
        # Run the SQL query to get the data
        monthly_data = duckdb_utils.run_sql_query_and_return_df(self.metric_h)

        # Sort the data chronologically
        monthly_data = monthly_data.sort_values('year_month')

        # Create a figure with just the ticket count chart
        plt.figure(figsize=(14, 8))

        # Create the bar chart
        bars = plt.bar(monthly_data['year_month'], monthly_data['ticket_count'], 
                    color='royalblue', width=0.7)

        # Add title and labels
        plt.title(self.metric_h_title, fontsize=18)
        plt.xlabel('Month', fontsize=14)
        plt.ylabel('Number of Tickets', fontsize=14)

        # Rotate x-axis labels for better readability
        plt.xticks(monthly_data['year_month'], rotation=45)

        # Add grid for better readability
        plt.grid(axis='y', alpha=0.3)

        # Add the count values on top of each bar
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 200,
                    f'{int(height):,}', ha='center', fontsize=12, fontweight='bold')

        # Add a horizontal line for the average
        avg_tickets = monthly_data['ticket_count'].mean()
        plt.axhline(y=avg_tickets, color='red', linestyle='--', alpha=0.8, linewidth=2)

        # Add an annotation for the average
        # Position at the first month to avoid overcrowding
        plt.annotate(f'Average: {int(avg_tickets):,}', 
                    xy=(monthly_data['year_month'].iloc[0], avg_tickets),
                    xytext=(monthly_data['year_month'].iloc[0], avg_tickets + 500),
                    arrowprops=dict(arrowstyle='->', color='red', alpha=0.8),
                    color='red', fontweight='bold', fontsize=12)

        # Enhance the visualization with a border
        plt.gca().spines['top'].set_visible(True)
        plt.gca().spines['right'].set_visible(True)
        plt.gca().spines['left'].set_linewidth(1.5)
        plt.gca().spines['bottom'].set_linewidth(1.5)

        # Add a bit more space at the top of the chart
        y_max = monthly_data['ticket_count'].max()
        plt.ylim(0, y_max * 1.1)  # Add 10% space at the top

        # Tight layout
        plt.tight_layout()

        # Show the plot
        plt.show()

    def create_metric_i(self):
        # Run the SQL query to get the data - making sure to filter out 2023-W52
        weekly_data = duckdb_utils.run_sql_query_and_return_df(self.metric_i)

        # Sort the data chronologically by year_week
        weekly_data = weekly_data.sort_values('year_week')

        # Create a figure with 3 subplots stacked vertically
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(16, 18))

        # 1. First subplot - ticket_count
        bars1 = ax1.bar(weekly_data['year_week'], weekly_data['ticket_count'], 
                        color='royalblue', width=0.6)
        ax1.set_title('Weekly Ticket Count', fontsize=16)
        ax1.set_xlabel('Week', fontsize=14)
        ax1.set_ylabel('Number of Tickets', fontsize=14)
        ax1.grid(True, alpha=0.3, axis='y')
        # Rotate x-axis labels for better readability
        ax1.set_xticks(weekly_data['year_week'])
        ax1.set_xticklabels(weekly_data['year_week'], rotation=90)
        # Add data point values on top of bars
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 50,
                    f'{int(height)}', ha='center', fontsize=10, fontweight='bold')

        # 2. Second subplot - weekly_change
        # Filter out rows with NaN in weekly_change
        weekly_change_data = weekly_data.dropna(subset=['weekly_change'])

        # Important: Create a new x-axis that only includes weeks with valid weekly_change
        valid_weeks_change = weekly_change_data['year_week'].tolist()

        bars2 = ax2.bar(valid_weeks_change, weekly_change_data['weekly_change'], 
                        color=weekly_change_data['weekly_change'].apply(lambda x: 'forestgreen' if x >= 0 else 'crimson'),
                        width=0.6)
        ax2.set_title('Weekly Change in Tickets', fontsize=16)
        ax2.set_xlabel('Week', fontsize=14)
        ax2.set_ylabel('Change in Ticket Count', fontsize=14)
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.7)
        
        # Set x-axis to only show the valid weeks
        ax2.set_xticks(valid_weeks_change)
        ax2.set_xticklabels(valid_weeks_change, rotation=90)
       
        # Add data point values on top of bars
        for bar in bars2:
            height = bar.get_height()
            
            # Position above or below depending on whether it's positive or negative
            y_pos = height + 30 if height >= 0 else height - 50
            ax2.text(bar.get_x() + bar.get_width()/2., y_pos,
                    f'{int(height)}', ha='center', fontsize=10, fontweight='bold')

        # 3. Third subplot - percent_change
        # Filter out rows with NaN in percent_change
        percent_change_data = weekly_data.dropna(subset=['percent_change'])

        # Important: Create a new x-axis that only includes weeks with valid percent_change
        valid_weeks_percent = percent_change_data['year_week'].tolist()

        bars3 = ax3.bar(valid_weeks_percent, percent_change_data['percent_change'], 
                        color=percent_change_data['percent_change'].apply(lambda x: 'darkorange' if x >= 0 else 'purple'),
                        width=0.6)
        ax3.set_title('Weekly Percent Change', fontsize=16)
        ax3.set_xlabel('Week', fontsize=14)
        ax3.set_ylabel('Percent Change (%)', fontsize=14)
        ax3.grid(True, alpha=0.3, axis='y')
        ax3.axhline(y=0, color='black', linestyle='-', alpha=0.7)
        # Set x-axis to only show the valid weeks
        ax3.set_xticks(valid_weeks_percent)
        ax3.set_xticklabels(valid_weeks_percent, rotation=90)
        # Add data point values on top of bars
        for bar in bars3:
            height = bar.get_height()
            # Position above or below depending on whether it's positive or negative
            y_pos = height + 2 if height >= 0 else height - 4
            ax3.text(bar.get_x() + bar.get_width()/2., y_pos,
                    f'{height:.1f}%', ha='center', fontsize=10, fontweight='bold')

        # Add main title above all subplots
        fig.suptitle(self.metric_i_title, fontsize=18, y=0.98)

        # Adjust layout
        plt.tight_layout()
        plt.subplots_adjust(top=0.95)

        # Show the plot
        plt.show()

    def create_metric_j(self):
        # Run the filtered SQL query to get the data
        agency_fee_data = duckdb_utils.run_sql_query_and_return_df(self.metric_j)

        # Sort the data by total fees (descending)
        agency_fee_data = agency_fee_data.sort_values('total_ticket_fees_usd', ascending=False)

        # Create a figure with more height to accommodate the labels
        plt.figure(figsize=(14, 10))

        # Create horizontal bar chart
        bars = plt.barh(agency_fee_data['issuing_agency'], 
                    agency_fee_data['total_ticket_fees_usd'],
                    color='darkgreen',
                    height=0.6)

        # Add title and labels
        plt.title(self.metric_j_title, fontsize=16)
        plt.xlabel('Total Fees (USD)', fontsize=14)
        plt.ylabel('Agency', fontsize=14)

        # Format x-axis with dollar signs
        plt.gca().xaxis.set_major_formatter('${x:,.0f}')

        # Add grid for better readability
        plt.grid(axis='x', alpha=0.3)

        # Calculate the maximum total fee to set x-axis limit
        max_fee = agency_fee_data['total_ticket_fees_usd'].max()
        plt.xlim(0, max_fee * 1.4)

        # Add multi-line labels at the end of each bar
        for i, bar in enumerate(bars):
            width = bar.get_width()
            agency = agency_fee_data.iloc[i]

            # Create the multi-line label as requested
            label_text = f"Total: ${width:,.0f}\nAvg Fee: ${agency['average_fee_usd']:.2f}\nTicket Count: {int(agency['ticket_count']):,}"

            # Place text to the right of the bar
            plt.text(width + (max_fee * 0.01), bar.get_y() + bar.get_height()/2, 
                    label_text, va='center', ha='left', fontsize=9)

        # Ensure adequate spacing for the labels
        plt.tight_layout()
        plt.subplots_adjust(right=0.75)

        # Show the plot
        plt.show()

    def create_metric_k(self):
        # Run the SQL query to get the data
        weekly_violation_data = duckdb_utils.run_sql_query_and_return_df(self.metric_k)

        # Extract the day columns
        day_columns = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

        # Sort by year_week to maintain chronological ordering
        weekly_violation_data = weekly_violation_data.sort_values('year_week')

        # Prepare the data for the heatmap
        # We'll use year_week as rows and day of week as columns
        pivot_data = weekly_violation_data.set_index('year_week')[day_columns]

        # Create a figure with appropriate size
        plt.figure(figsize=(18, 14))

        # Set a custom colormap with white for 0 values
        cmap = sns.color_palette("YlGnBu", as_cmap=True)
        cmap.set_under('whitesmoke')  # Color for values below vmin

        # Create the heatmap
        ax = sns.heatmap(pivot_data, 
                        annot=True,
                        fmt=",d",
                        cmap=cmap,
                        linewidths=0.5,
                        cbar_kws={'label': 'Ticket Count'},
                        vmin=1)

        # Capitalize the day names on x-axis and put them on top
        ax.xaxis.set_ticks_position('top')
        ax.xaxis.set_label_position('top')
        plt.xticks(np.arange(len(day_columns)) + 0.5, [day.capitalize() for day in day_columns], rotation=0, fontsize=12)
        plt.yticks(fontsize=10)

        # Set the title - position it below the x-axis labels since they're now at the top
        plt.title(self.metric_k_title, fontsize=18, pad=20, y=1.08)

        # Adjust layout
        plt.tight_layout()

        # Show the plot
        plt.show()

    def create_metric_l(self):
        # Run the SQL query to get the data
        county_violation_data = duckdb_utils.run_sql_query_and_return_df(self.metric_l)

        # Extract the day columns
        day_columns = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

        # Sort by total_tickets in descending order
        county_violation_data = county_violation_data.sort_values('total_tickets', ascending=False)

        # Create a figure with appropriate size
        plt.figure(figsize=(20, 16))

        # Create the heatmap data - exclude total_tickets from the heatmap
        heatmap_data = county_violation_data.set_index('violation_county')[day_columns]

        # Set a custom colormap with white for 0 values
        cmap = sns.color_palette("YlGnBu", as_cmap=True)
        cmap.set_under('whitesmoke')  # Color for values below vmin

        # Create the heatmap
        ax = sns.heatmap(heatmap_data, 
                        annot=True,
                        fmt=",d",
                        cmap=cmap,
                        linewidths=0.5,
                        cbar_kws={'label': 'Ticket Count'},
                        vmin=1)

        # Capitalize the day names on x-axis and put them on top
        ax.xaxis.set_ticks_position('top')
        ax.xaxis.set_label_position('top')
        plt.xticks(np.arange(len(day_columns)) + 0.5, [day.capitalize() for day in day_columns], rotation=0, fontsize=12)
        plt.yticks(fontsize=10)

        # Set the title - position it below the x-axis labels since they're now at the top
        plt.title(self.metric_l_title, fontsize=18, pad=20, y=1.08)

        # Add total_tickets as an additional column label on the right
        for i, (idx, row) in enumerate(county_violation_data.iterrows()):
            # Format total with commas
            total_formatted = f"{row['total_tickets']:,}"
            # Position text to the right of the heatmap
            plt.text(len(day_columns) + 0.5, i + 0.5, total_formatted,
                    ha='left', va='center', fontweight='bold', fontsize=10)

        # Add "Total" header for the total_tickets column
        plt.text(len(day_columns) + 0.5, -0.3, 'Total Tickets',
                ha='left', va='center', fontweight='bold', fontsize=12)

        # Adjust figure size to make room for the total_tickets column
        plt.subplots_adjust(right=0.9)

        # Show the plot
        plt.tight_layout()
        plt.show()

    def create_metric_m(self):
        # Run the SQL query to get the data
        violation_day_data = duckdb_utils.run_sql_query_and_return_df(self.metric_m)

        # Extract the day columns
        day_columns = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

        # Sort by total_tickets in descending order
        violation_day_data = violation_day_data.sort_values('total_tickets', ascending=False)

        # Create a figure with appropriate size
        plt.figure(figsize=(20, 16))

        # Create a column to use as row labels (combining violation_code and definition)
        violation_day_data['violation_label'] = violation_day_data['violation_code'].astype(str) + ': ' + violation_day_data['violation_definition'].str[:50]

        # Create the heatmap data - exclude total_tickets and use combined label as index
        heatmap_data = violation_day_data.set_index('violation_label')[day_columns]

        # Create a logarithmic normalization for the colormap
        # Adding 1 to avoid log(0) issues
        log_norm = colors.LogNorm(vmin=1, vmax=heatmap_data.values.max())

        # Set a custom colormap with white for 0 values
        cmap = sns.color_palette("YlGnBu", as_cmap=True)
        cmap.set_under('whitesmoke')  # Color for values below vmin

        # Create the heatmap with logarithmic normalization
        ax = sns.heatmap(heatmap_data, 
                        annot=True,
                        fmt=",d",
                        cmap=cmap,
                        norm=log_norm,
                        linewidths=0.5,
                        cbar_kws={'label': 'Ticket Count (Log Scale)'},
                        vmin=1)

        # Capitalize the day names on x-axis and put them on top
        ax.xaxis.set_ticks_position('top')
        ax.xaxis.set_label_position('top')
        plt.xticks(np.arange(len(day_columns)) + 0.5, [day.capitalize() for day in day_columns], rotation=0, fontsize=12)
        plt.yticks(fontsize=10)

        # Set the title - position it below the x-axis labels since they're now at the top
        plt.title(self.metric_m_title, fontsize=18, pad=20, y=1.08)

        # Add total_tickets as an additional column label on the right
        for i, (idx, row) in enumerate(violation_day_data.iterrows()):
            # Format total with commas
            total_formatted = f"{row['total_tickets']:,}"
            # Position text to the right of the heatmap
            plt.text(len(day_columns) + 0.5, i + 0.5, total_formatted,
                    ha='left', va='center', fontweight='bold', fontsize=10)

        # Add "Total" header for the total_tickets column
        plt.text(len(day_columns) + 0.5, -0.3, 'Total Tickets',
                ha='left', va='center', fontweight='bold', fontsize=12)

        # Add a note about the logarithmic scale
        plt.figtext(0.5, 0.01, 'Note: Color intensity uses logarithmic scale to better show variation across all values.',
                ha='center', fontsize=12, style='italic')

        # Adjust figure size to make room for the total_tickets column
        plt.subplots_adjust(right=0.9, bottom=0.05)

        # Show the plot
        plt.tight_layout()
        plt.show()

    def create_report(self):
        self.create_metric_a()
        self.create_metric_b()
        self.create_metric_c()
        self.create_metric_d()
        self.create_metric_e()
        self.create_metric_f()
        self.create_metric_g()
        self.create_metric_h()
        self.create_metric_i()
        self.create_metric_j()
        self.create_metric_k()
        self.create_metric_l()
        self.create_metric_m()


if __name__ == "__main__":
    None
