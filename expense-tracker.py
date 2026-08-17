# expense-tracker.py
import json
import os
import uuid
import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(
    page_title="FluidFinance // Expense Tracker",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DATA_FILE = "data.json"

# FIXED: Removed the invalid parameter. unsafe_allow_html=True is the correct parameter.
st.markdown("""
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
""", unsafe_allow_html=True)

# 2. Local File Storage Management
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

st.title("FluidFinance // Expense Tracker")
st.markdown("---")

# 3. Layout Grid Split
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
    # Calculations Metrics Aggregation
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
    
    # 4. Embedded HTML Chart Component safely passing serialized dynamic lists
    chart_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://jsdelivr.net"></script>
        <style>
            body {{ background: transparent; margin: 0; padding: 0; }}
            .box {{ height: 180px; width: 100%; }}
        </style>
    </head>
    <body>
        <div class="box"><canvas id="strChart"></canvas></div>
        <script>
            const ctx = document.getElementById('strChart').getContext('2d');
            new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: {list(categories_agg.keys())},
                    datasets: [{{
                        data: {list(categories_agg.values())},
                        backgroundColor: ['#6366f1', '#ec4899', '#14b8a6', '#f59e0b', '#94a3b8'],
                        borderRadius: 6
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }},
                        x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }}
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    """
    components.html(chart_html, height=190)

# 5. Ledger Interactive Data List Table 
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