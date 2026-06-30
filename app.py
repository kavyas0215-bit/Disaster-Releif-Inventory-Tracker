import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import inventory_manager as im

# Page Configuration
st.set_page_config(
    page_title="Disaster Relief Inventory Tracker",
    page_icon="🎒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Main container background */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(240, 245, 255, 0.5) 0%, rgba(255, 255, 255, 1) 90%);
    }
    
    /* Elegant Title Banner */
    .header-container {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2.5rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    }
    .header-container::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
        pointer-events: none;
    }
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .header-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    /* Card design */
    .metric-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02), 0 1px 3px rgba(0,0,0,0.02);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px rgba(0,0,0,0.05);
    }
    .metric-label {
        font-size: 0.9rem;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1a202c;
    }
    
    /* Alerts */
    .alert-banner {
        background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%);
        border-left: 5px solid #e53e3e;
        padding: 1.25rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        color: #9b2c2c;
        box-shadow: 0 2px 4px rgba(229, 62, 62, 0.05);
    }
    .alert-title {
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.25rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Section headers */
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d3748;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #2b6cb0;
        padding-left: 10px;
    }
    
    /* Badge styling */
    .badge-critical {
        background-color: #fed7d7;
        color: #c53030;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .badge-safe {
        background-color: #c6f6d5;
        color: #22543d;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to format timestamp
def format_datetime(iso_str):
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return iso_str

# Load Inventory
inventory = im.load_inventory()

# Main Header
st.markdown("""
    <div class="header-container">
        <div class="header-title">🎒 Disaster Relief Inventory Tracker</div>
        <div class="header-subtitle">Real-time supply coordination, stock status, and rapid response deployment logs.</div>
    </div>
""", unsafe_allow_html=True)

# Calculate statistics
report = im.get_inventory_report(inventory)
low_stock_alerts = im.get_low_stock_alerts(inventory)

# Display Alert Banner for Low Stock
if low_stock_alerts:
    alert_items = ", ".join([f"**{name}** ({details['quantity']} {details['unit']})" for name, details in low_stock_alerts.items()])
    st.markdown(f"""
        <div class="alert-banner">
            <div class="alert-title">⚠️ CRITICAL STOCK ALERT</div>
            <div>The following items have fallen below their safety threshold and require immediate replenishment: {alert_items}</div>
        </div>
    """, unsafe_allow_html=True)

# Tabs Navigation
tab_dashboard, tab_update, tab_register, tab_report = st.tabs([
    "📈 Live Dashboard",
    "🔄 Distribute & Replenish Stock",
    "➕ Register New Supply",
    "📝 Generate Report"
])

# ==============================================================================
# TAB 1: LIVE DASHBOARD
# ==============================================================================
with tab_dashboard:
    # Metric Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📦 Unique Items</div>
                <div class="metric-value">{report['total_items']}</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📊 Total Quantities</div>
                <div class="metric-value">{report['total_quantities']:,}</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid {'#e53e3e' if report['low_stock_count'] > 0 else '#48bb78'}">
                <div class="metric-label">🚨 Low Stock Items</div>
                <div class="metric-value" style="color: {'#e53e3e' if report['low_stock_count'] > 0 else '#48bb78'}">{report['low_stock_count']}</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🗂️ Categories</div>
                <div class="metric-value">{len(report['category_summary'])}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Inventory List & Search</div>", unsafe_allow_html=True)
    
    # Filter Controls
    f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
    with f_col1:
        search_query = st.text_input("Search Supplies by Name:", "", placeholder="Type supply name...")
    with f_col2:
        all_categories = sorted(list(set(item["category"] for item in inventory.values())))
        category_filter = st.selectbox("Filter Category:", ["All Categories"] + all_categories)
    with f_col3:
        stock_filter = st.selectbox("Filter Stock Status:", ["All Items", "Low Stock / Critical", "Normal Stock"])

    # Prepare DataFrame
    data_list = []
    for name, details in inventory.items():
        data_list.append({
            "Item Name": name,
            "Category": details["category"],
            "Quantity": details["quantity"],
            "Unit": details["unit"],
            "Safety Threshold": details["threshold"],
            "Status": "🚨 Low Stock" if details["quantity"] <= details["threshold"] else "✅ Safe",
            "Last Updated": format_datetime(details["last_updated"])
        })
    
    df = pd.DataFrame(data_list)
    
    # Apply Filters
    if search_query:
        df = df[df["Item Name"].str.contains(search_query, case=False)]
    if category_filter != "All Categories":
        df = df[df["Category"] == category_filter]
    if stock_filter == "Low Stock / Critical":
        df = df[df["Status"] == "🚨 Low Stock"]
    elif stock_filter == "Normal Stock":
        df = df[df["Status"] == "✅ Safe"]

    # Display Table
    if not df.empty:
        # Styled dataframe
        def highlight_status(val):
            if val == "🚨 Low Stock":
                return "background-color: #fed7d7; color: #9b2c2c; font-weight: bold;"
            return "background-color: #c6f6d5; color: #22543d;"

        # Reset index for clean viewing
        df_display = df.reset_index(drop=True)
        
        st.dataframe(
            df_display.style.map(highlight_status, subset=["Status"]),
            use_container_width=True,
            height=350
        )
    else:
        st.info("No items match the active filters.")

    # Visualization
    if not df.empty:
        st.markdown("<div class='section-title'>Visual Reports</div>", unsafe_allow_html=True)
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            fig_bar = px.bar(
                df, 
                x="Item Name", 
                y="Quantity", 
                color="Category",
                hover_data=["Safety Threshold", "Status"],
                title="Current Quantities by Item and Category",
                template="plotly_white",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_bar.update_layout(xaxis_title="Item", yaxis_title="Quantity")
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with chart_col2:
            cat_df = df.groupby("Category")["Quantity"].sum().reset_index()
            fig_pie = px.pie(
                cat_df, 
                values="Quantity", 
                names="Category",
                title="Category Share of Total Inventory Quantities",
                color_discrete_sequence=px.colors.qualitative.Safe,
                hole=0.4
            )
            st.plotly_chart(fig_pie, use_container_width=True)

# ==============================================================================
# TAB 2: DISTRIBUTE & REPLENISH STOCK (INTERMEDIATE)
# ==============================================================================
with tab_update:
    st.markdown("<div class='section-title'>Distribute or Replenish Stock</div>", unsafe_allow_html=True)
    st.write("Adjust stock levels for current items. Positive integers replenish items, negative integers indicate supply distributions.")
    
    if not inventory:
        st.warning("No items registered yet. Register items in the 'Register New Supply' tab first.")
    else:
        item_list = sorted(list(inventory.keys()))
        selected_item = st.selectbox("Select Supply Item:", item_list)
        
        # Display current status of selected item
        item_details = inventory[selected_item]
        col_item1, col_item2, col_item3 = st.columns(3)
        col_item1.metric("Current Stock", f"{item_details['quantity']} {item_details['unit']}")
        col_item2.metric("Safety Threshold", f"{item_details['threshold']} {item_details['unit']}")
        status_color = "🔴 Low Stock" if item_details['quantity'] <= item_details['threshold'] else "🟢 Safe"
        col_item3.metric("Status", status_color)
        
        with st.form("update_stock_form"):
            transaction_type = st.radio("Transaction Type:", ["Distribution (Subtract Stock)", "Replenishment (Add Stock)"])
            qty_change = st.number_input("Quantity Change Amount:", min_value=1, step=1)
            
            submit_update = st.form_submit_button("Submit Transaction", use_container_width=True)
            
            if submit_update:
                actual_change = -qty_change if transaction_type == "Distribution (Subtract Stock)" else qty_change
                
                try:
                    success = im.update_stock(inventory, selected_item, actual_change)
                    if success:
                        st.success(f"Successfully recorded transaction. Item '{selected_item}' updated.")
                        # Force refresh
                        st.rerun()
                    else:
                        st.error("Failed to save transaction to inventory file.")
                except ValueError as e:
                    st.error(f"Transaction Error: {e}")

# ==============================================================================
# TAB 3: REGISTER NEW SUPPLY (BASIC)
# ==============================================================================
with tab_register:
    st.markdown("<div class='section-title'>Register a New Item in Inventory</div>", unsafe_allow_html=True)
    st.write("Add completely new supplies to the tracking system with categories, initial stock, and safety alert thresholds.")
    
    # Pre-defined categories and option to add a custom one
    existing_categories = sorted(list(set(item["category"] for item in inventory.values()))) if inventory else []
    if "Water & Sanitation" not in existing_categories:
        existing_categories.append("Water & Sanitation")
    if "Medical Supplies" not in existing_categories:
        existing_categories.append("Medical Supplies")
    if "Food & Nutrition" not in existing_categories:
        existing_categories.append("Food & Nutrition")
    if "Shelter & Bedding" not in existing_categories:
        existing_categories.append("Shelter & Bedding")
    if "Operational Equipment" not in existing_categories:
        existing_categories.append("Operational Equipment")
    
    existing_categories = sorted(list(set(existing_categories)))
    
    with st.form("register_item_form"):
        r_name = st.text_input("Item Name (e.g., Solar Lanterns, Water Purification Tablets):", "")
        
        # Category selection
        cat_option = st.selectbox("Category Select:", existing_categories + ["-- Create Custom Category --"])
        custom_cat = ""
        if cat_option == "-- Create Custom Category --":
            custom_cat = st.text_input("Enter New Custom Category Name:", "")
            
        r_qty = st.number_input("Initial Quantity in Stock:", min_value=0, step=1, value=0)
        r_unit = st.text_input("Measurement Unit (e.g., liters, boxes, tents, units):", "units")
        r_threshold = st.number_input("Safety Warning Threshold (triggers alerts below/at this amount):", min_value=0, step=1, value=10)
        
        submit_register = st.form_submit_button("Register New Supply", use_container_width=True)
        
        if submit_register:
            r_name = r_name.strip()
            final_cat = custom_cat.strip() if cat_option == "-- Create Custom Category --" else cat_option
            
            if not r_name:
                st.error("Item Name is a required field.")
            elif not final_cat:
                st.error("Category is a required field.")
            else:
                try:
                    success = im.add_item(
                        inventory=inventory,
                        name=r_name,
                        category=final_cat,
                        quantity=r_qty,
                        unit=r_unit,
                        threshold=r_threshold
                    )
                    if success:
                        st.success(f"Successfully registered '{r_name}' under category '{final_cat}'.")
                        st.rerun()
                    else:
                        st.error("Failed to save registered item to inventory database.")
                except ValueError as e:
                    st.error(f"Error: {e}")

# ==============================================================================
# TAB 4: GENERATE REPORT & UTILITIES
# ==============================================================================
with tab_report:
    st.markdown("<div class='section-title'>Generate Inventory Stock Report</div>", unsafe_allow_html=True)
    st.write("Generate and download tabular spreadsheets and summaries of currently registered relief assets.")
    
    # Display full report summary
    st.markdown("### Executive Summary")
    
    st.write(f"**Report Generated On:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.write(f"- **Total Registered Supply Catalog Items:** {report['total_items']} items")
    st.write(f"- **Sum Total of Quantities (all categories combined):** {report['total_quantities']}")
    st.write(f"- **Total Items Flagged under Critical Stock Safety Alerts:** {report['low_stock_count']}")
    
    st.markdown("### Category Breakdown")
    cat_summary_data = []
    for cat, total in report["category_summary"].items():
        cat_summary_data.append({"Category": cat, "Total Stock": total})
    if cat_summary_data:
        cat_df = pd.DataFrame(cat_summary_data)
        st.table(cat_df)
    else:
        st.info("No stock data to summarize by category.")
        
    st.markdown("### Download Data")
    if inventory:
        # Convert dictionary to CSV format
        csv_df = pd.DataFrame(data_list)
        csv_data = csv_df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="Download Full Inventory CSV Report",
            data=csv_data,
            file_name=f"disaster_relief_inventory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.warning("No data available to download.")

    # Reset option (Utility)
    st.markdown("---")
    st.markdown("### ⚠️ Database Management")
    with st.expander("Delete an Item from Inventory"):
        if inventory:
            del_item = st.selectbox("Select item to DELETE:", sorted(list(inventory.keys())))
            confirm_del = st.checkbox("I confirm that I want to delete this item permanently.")
            btn_del = st.button("Delete Selected Item", type="primary")
            
            if btn_del:
                if confirm_del:
                    success = im.delete_item(inventory, del_item)
                    if success:
                        st.success(f"Permanently deleted '{del_item}'.")
                        st.rerun()
                    else:
                        st.error("Failed to update inventory database.")
                else:
                    st.warning("Please check the confirmation checkbox to proceed.")
        else:
            st.info("No items to delete.")
