import json
import os
import uuid
import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="Shri Finance // Expense Tracker",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DATA_FILE = "data.json"

# 2. Custom Styling (Using a separate variable name so we don't overwrite 'st')
css_styles = """
    <style>
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%) !important;
            color: #f8fafc !important;
        }
        
        /* Styled container for metrics */
        .metric-card {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.08);
            margin-bottom: 1rem;
        }
        .metric-val {
            font-size: 1.8rem;
            font-weight: 700;
            color: #6366f1;
            margin-top: 0.5rem;
        }
        
        /* Custom Button Styling */
        .stButton>button {
            width: 100%;
            background: #6366f1 !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.6rem 1rem !important;
            font-weight: 600 !important;
        }
    </style>
"""
st.markdown(css_styles, unsafe_allow_html=True)

# 3. Local File Storage Management
def init_storage():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

def read_data():
    init_storage()
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def write_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Load existing state data array
expenses = read_data()

st.title("Shri Finance // Expense Tracker")
st.markdown("---")

# 4. Layout Grid Split
col_form, col_dash = st.columns([1.1, 1.9], gap="large")

with col_form:
    st.subheader("Log Transaction")
    
    with st.form("expense_input_form", clear_on_submit=True):
        title = st.text_input("Description", placeholder="e.g., Grocery Shopping")
        amount = st.number_input("Amount ($)", min_value=0.0, step=0.01, format="%.2f")
        category = st.selectbox("Category", [
            "Food", "Rent", "Utilities", "Entertainment", "Other"
        ])
        
        submit_btn = st.form_submit_button("Add to Ledger")
        
        if submit_btn:
            if title and amount > 0:
                new_item = {
                    "id": str(uuid.uuid4()),
                    "title": title,
                    "amount": float(amount),
                    "category": category
                }
                expenses.append(new_item)
                write_data(expenses)
                st.rerun()
            else:
                st.error("Please provide a valid description and amount.")

with col_dash:
    # 5. Calculations Metrics Aggregation
    total_spend = sum(item["amount"] for item in expenses)
    total_items = len(expenses)
    
    # Process chart distribution properties
    categories_agg = { "Food": 0, "Rent": 0, "Utilities": 0, "Entertainment": 0, "Other": 0 }
    for item in expenses:
        cat = item["category"]
        if cat in categories_agg:
            categories_agg[cat] += item["amount"]
        else:
            categories_agg["Other"] += item["amount"]

    # Metrics Display Columns
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="metric-card"><p style="color:#94a3b8;margin:0;">Total Burn Rate</p><div class="metric-val">${total_spend:,.2f}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><p style="color:#94a3b8;margin:0;">Active Line Items</p><div class="metric-val">{total_items}</div></div>', unsafe_allow_html=True)
        
    st.subheader("Allocation Breakdown")
    
    # 6. Bar Chart Data Preparation
    # Filter out categories with 0 amount so the chart looks clean
    chart_data = {k: v for k, v in categories_agg.items() if v > 0}
    
    if chart_data:
        # Convert to Pandas DataFrame
        df = pd.DataFrame(list(chart_data.items()), columns=['Category', 'Amount'])
        # Set Category as index for st.bar_chart
        df = df.set_index('Category')
        
        # Render the native Streamlit bar chart (no HTML needed)
        st.bar_chart(df, color="#6366f1", height=250)
    else:
        st.info("Add transactions to see the breakdown chart.")

# 7. Ledger Interactive Data List Table 
st.markdown("### Transaction Ledger")
if not expenses:
    st.info("No transaction logs recorded yet.")
else:
    for item in expenses:
        r_col1, r_col2, r_col3, r_col4 = st.columns([2, 1, 1, 0.5])
        r_col1.write(item["title"])
        r_col2.write(f"`{item['category']}`")
        r_col3.write(f"**${item['amount']:.2f}**")
        
        if r_col4.button("🗑️", key=f"del_{item['id']}"):
            updated = [x for x in expenses if x["id"] != item["id"]]
            write_data(updated)
            st.rerun()