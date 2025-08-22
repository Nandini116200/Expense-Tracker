import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# App configuration
st.set_page_config(page_title="Expense Tracker", layout="wide")
st.title("💰 Expense Tracker")

# Initialize session state for transactions
if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame(
        columns=["Date", "Type", "Amount", "Category", "Description"]
    )

# Sidebar: Category-wise Summary
st.sidebar.header("📜 Category Summary")
if not st.session_state.transactions.empty:
    category_summary = st.session_state.transactions.groupby("Category")["Amount"].sum().reset_index()
    st.sidebar.dataframe(
        category_summary,
        use_container_width=True,
        hide_index=True
    )
else:
    st.sidebar.info("No transactions yet.")
# ---
st.markdown("---")
st.sidebar.markdown("<p style='text-align:corner; font-size:13px; color:gray;'>Made by Nandini</p>", unsafe_allow_html=True)
# ---

# Main content area
st.subheader("➕ Add Transaction")
t_type = st.selectbox("Type", ["Income", "Expense"])

with st.form("add_transaction_form"):
    t_date = st.date_input("Date", value=date.today())
    t_amount = st.number_input("Amount", min_value=1, step=1)
    
    income_categories = ["Salary", "Bonus", "Other Income"]
    expense_categories = ["Food", "Transport", "Housing", "Entertainment", "Shopping", "Utilities", "Health", "Other Expense"]
    
    if t_type == "Income":
        t_category = st.selectbox(
            "Category",
            income_categories
        )
    else:
        t_category = st.selectbox(
            "Category",
            expense_categories
        )
    
    t_description = st.text_area("Description (optional)")

    submitted = st.form_submit_button("Add")

if submitted:
    new_entry = {
        "Date": str(t_date),
        "Type": t_type,
        "Amount": t_amount,
        "Category": t_category,
        "Description": t_description
    }
    st.session_state.transactions = pd.concat(
        [st.session_state.transactions, pd.DataFrame([new_entry])],
        ignore_index=True
    )
    st.success("Transaction Added ✅")
    st.rerun()



# Transactions Table
st.subheader("📋 All Transactions")
if not st.session_state.transactions.empty:
    st.table(st.session_state.transactions)
else:
    st.info("No transactions yet. Add some from above!")

if not st.session_state.transactions.empty:
    # Metrics with full data
    income = st.session_state.transactions.query("Type == 'Income'")["Amount"].sum()
    expense = st.session_state.transactions.query("Type == 'Expense'")["Amount"].sum()
    balance = income - expense

    st.subheader("📊 Summary")

    summary_df = pd.DataFrame({
        "Metric": ["Total Income", "Total Expense", "Balance"],
        "Amount": [f"₹{income}", f"₹{expense}", f"₹{balance}"]
    })

    st.table(summary_df)


    # Charts with full data
    col1, col2 = st.columns(2)

    # Pie chart: category-wise expenses
    with col1:
        st.markdown("#### Category-wise Expenses")
        with st.container():
            expenses = st.session_state.transactions.query("Type == 'Expense'")
            if not expenses.empty:
                fig, ax = plt.subplots(figsize=(5, 8))
                expenses.groupby("Category")["Amount"].sum().plot.pie(
                    autopct="%1.1f%%", ax=ax, ylabel=""
                )
                st.pyplot(fig)
            else:
                st.info("No expenses to show.")

    # Bar chart: Income vs Expense
    with col2:
        st.markdown("#### Income vs Expense")
        with st.container():
            if not st.session_state.transactions.empty:
                fig, ax = plt.subplots(figsize=(2, 1.5))
                grouped = st.session_state.transactions.groupby("Type")["Amount"].sum()
                colors = ["green" if t == "Income" else "red" for t in grouped.index]
                grouped.plot.bar(ax=ax, color=colors)
                ax.set_ylabel("Amount")
                st.pyplot(fig)

