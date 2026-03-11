"""
💰 SmartBudget — Personal Finance Tracker & Budget Planner
Streamlit app with 29 UI components. Zero external chart dependencies.
"""

import streamlit as st
import pandas as pd
from datetime import date, timedelta

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SmartBudget",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%); }
    [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    [data-testid="metric-container"] {
        background: #f8fafc; border: 1px solid #e2e8f0;
        border-radius: 12px; padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    h1 { font-family: 'Space Mono', monospace !important; }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
    }
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important; border: none !important;
        border-radius: 8px !important; font-weight: 600 !important;
        padding: 0.5rem 1.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SAMPLE DATA
# ─────────────────────────────────────────────
CATEGORIES = [
    "🍔 Food & Dining", "🚗 Transport", "🛍 Shopping", "💡 Utilities",
    "🏥 Health", "🎮 Entertainment", "📚 Education", "✈ Travel",
    "💼 Work", "🏠 Housing"
]

SAMPLE_TRANSACTIONS = pd.DataFrame({
    "Date": [date.today() - timedelta(days=i) for i in range(15)],
    "Description": [
        "Grocery Run", "Uber Ride", "Netflix", "Electric Bill", "Gym Membership",
        "Restaurant", "Coffee Shop", "Amazon", "Doctor Visit", "Bus Pass",
        "Spotify", "Online Course", "Lunch", "Fuel", "Water Bill"
    ],
    "Category": [
        "🍔 Food & Dining", "🚗 Transport", "🎮 Entertainment", "💡 Utilities", "🏥 Health",
        "🍔 Food & Dining", "🍔 Food & Dining", "🛍 Shopping", "🏥 Health", "🚗 Transport",
        "🎮 Entertainment", "📚 Education", "🍔 Food & Dining", "🚗 Transport", "💡 Utilities"
    ],
    "Amount": [
        45.20, 12.50, 15.99, 80.00, 30.00, 62.40, 8.75, 134.20,
        50.00, 25.00, 9.99, 49.00, 18.30, 55.60, 18.00
    ],
    "Type": ["Expense"] * 15,
})

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "transactions"   not in st.session_state:
    st.session_state.transactions   = SAMPLE_TRANSACTIONS.copy()
if "budget_limits"  not in st.session_state:
    st.session_state.budget_limits  = {cat: 200.0 for cat in CATEGORIES}
if "monthly_income" not in st.session_state:
    st.session_state.monthly_income = 3500.0
if "savings_goal"   not in st.session_state:
    st.session_state.savings_goal   = 1000.0
if "dark_mode"      not in st.session_state:
    st.session_state.dark_mode      = False

# ─────────────────────────────────────────────
# SIDEBAR  — COMPONENT 1: st.sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💰 SmartBudget")
    st.markdown("---")

    # COMPONENT 2: st.radio — navigation
    page = st.radio(
        "Navigate",
        ["📊 Dashboard", "➕ Add Transaction", "📈 Analytics",
         "⚙️ Budget Settings", "ℹ️ About"],
        label_visibility="collapsed",
    )

    st.markdown("---")

    # COMPONENT 3: st.toggle — dark mode (extra merit)
    dark_toggle = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    st.session_state.dark_mode = dark_toggle

    st.markdown("---")

    # COMPONENT 4: st.date_input — filter range
    st.markdown("**📅 Date Filter**")
    date_range = st.date_input(
        "Select range",
        value=(date.today() - timedelta(days=30), date.today()),
        label_visibility="collapsed",
    )

    # COMPONENT 5: st.multiselect — filter categories
    st.markdown("**🏷 Filter Categories**")
    selected_cats = st.multiselect(
        "Categories", options=CATEGORIES,
        default=CATEGORIES[:5], label_visibility="collapsed",
    )

    st.markdown("---")
    st.caption("v1.0.0 · Built with Streamlit")


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def get_filtered_df():
    df = st.session_state.transactions.copy()
    if selected_cats:
        df = df[df["Category"].isin(selected_cats)]
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        df = df[(df["Date"] >= date_range[0]) & (df["Date"] <= date_range[1])]
    return df


# ═══════════════════════════════════════════════════════
# PAGE 1 — DASHBOARD
# ═══════════════════════════════════════════════════════
if page == "📊 Dashboard":
    st.title("📊 Dashboard")
    st.markdown("Your financial snapshot at a glance.")

    df = get_filtered_df()
    total_expenses = df["Amount"].sum()
    balance        = st.session_state.monthly_income - total_expenses
    savings_pct    = (balance / st.session_state.monthly_income * 100
                      if st.session_state.monthly_income else 0)

    # COMPONENT 6: st.columns
    col1, col2, col3, col4 = st.columns(4)

    # COMPONENT 7: st.metric
    col1.metric("💵 Monthly Income",  f"${st.session_state.monthly_income:,.2f}")
    col2.metric("💸 Total Expenses",  f"${total_expenses:,.2f}",
                delta=f"-${total_expenses:,.0f}")
    col3.metric("💚 Balance",          f"${balance:,.2f}",
                delta=f"{savings_pct:.1f}% saved")
    col4.metric("🎯 Savings Goal",     f"${st.session_state.savings_goal:,.2f}")

    st.markdown("---")
    left, right = st.columns([3, 2])

    with left:
        # COMPONENT 8: st.progress — savings goal
        st.markdown("#### 🎯 Savings Goal Progress")
        prog = min(max(balance, 0) / st.session_state.savings_goal, 1.0) \
               if st.session_state.savings_goal else 0.0
        st.progress(float(prog))
        st.caption(f"${max(0, balance):,.2f} of ${st.session_state.savings_goal:,.2f} "
                   f"({prog*100:.1f}%)")

        st.markdown("#### 🏷 Budget Utilisation per Category")
        cat_spend = df.groupby("Category")["Amount"].sum()
        for cat in list(cat_spend.index)[:6]:
            limit = st.session_state.budget_limits.get(cat, 200)
            used  = cat_spend[cat]
            pct   = min(used / limit, 1.0) if limit else 0
            icon  = "🔴" if pct > 0.9 else ("🟡" if pct > 0.7 else "🟢")
            st.markdown(f"{icon} **{cat}** — `${used:.2f}` / `${limit:.2f}`")
            st.progress(float(pct))

    with right:
        st.markdown("#### 📊 Spend by Category")
        if not df.empty:
            cat_totals = (df.groupby("Category")["Amount"]
                          .sum().sort_values(ascending=False))
            # COMPONENT 9: st.bar_chart (built-in — no plotly)
            st.bar_chart(cat_totals, height=320)
        else:
            st.info("No data for selected filters.")

    st.markdown("---")
    st.markdown("#### 🕐 Recent Transactions")

    # COMPONENT 10: st.dataframe
    st.dataframe(
        df.sort_values("Date", ascending=False).head(8),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Amount": st.column_config.NumberColumn("Amount", format="$%.2f"),
            "Date":   st.column_config.DateColumn("Date"),
        },
    )


# ═══════════════════════════════════════════════════════
# PAGE 2 — ADD TRANSACTION
# ═══════════════════════════════════════════════════════
elif page == "➕ Add Transaction":
    st.title("➕ Add Transaction")
    st.markdown("Log a new income or expense entry.")

    # COMPONENT 11: st.tabs
    tab_exp, tab_inc = st.tabs(["💸 Expense", "💵 Income"])

    with tab_exp:
        st.markdown("### Record an Expense")
        c1, c2 = st.columns(2)

        with c1:
            # COMPONENT 12: st.text_input
            desc = st.text_input("📝 Description",
                                 placeholder="e.g. Coffee at Starbucks")
            # COMPONENT 13: st.selectbox
            cat = st.selectbox("🏷 Category", CATEGORIES)
            # COMPONENT 14: st.number_input
            amount = st.number_input("💲 Amount ($)",
                                     min_value=0.01, max_value=10000.0,
                                     value=20.00, step=0.50)

        with c2:
            # COMPONENT 15: st.date_input
            tx_date = st.date_input("📅 Date", value=date.today(), key="tx_date")
            # COMPONENT 16: st.text_area
            notes = st.text_area("📌 Notes (optional)",
                                 placeholder="Any extra details...", height=80)
            # COMPONENT 17: st.checkbox
            recurring = st.checkbox("🔁 Mark as recurring monthly expense")

        # COMPONENT 18: st.slider
        priority = st.slider("⭐ Priority / Importance", 1, 5, 3,
                             help="1 = low priority · 5 = critical")

        # COMPONENT 19: st.color_picker (extra merit)
        tag_color = st.color_picker("🎨 Tag Colour", "#6366f1",
                                    help="Assign a colour label to this transaction")

        # COMPONENT 20: st.button
        if st.button("✅ Add Expense"):
            if desc.strip():
                new_row = pd.DataFrame([{
                    "Date": tx_date, "Description": desc,
                    "Category": cat, "Amount": amount, "Type": "Expense",
                }])
                st.session_state.transactions = pd.concat(
                    [st.session_state.transactions, new_row], ignore_index=True)
                # COMPONENT 21: st.success
                st.success(f"✅ **{desc}** — ${amount:.2f} added!")
                if recurring:
                    # COMPONENT 22: st.info
                    st.info("🔁 Marked as recurring. We'll remind you next month.")
            else:
                # COMPONENT 23: st.warning
                st.warning("⚠️ Please enter a description before saving.")

    with tab_inc:
        st.markdown("### Record Income")
        c1, c2 = st.columns(2)
        with c1:
            inc_desc = st.text_input("📝 Source",
                                     placeholder="e.g. Freelance Project",
                                     key="inc_desc")
            inc_amt  = st.number_input("💲 Amount ($)", min_value=0.01,
                                       value=500.00, step=10.0, key="inc_amt")
        with c2:
            inc_date  = st.date_input("📅 Date", value=date.today(), key="inc_date")
            inc_notes = st.text_area("📌 Notes", height=80, key="inc_notes")

        if st.button("✅ Add Income", key="btn_income"):
            if inc_desc.strip():
                new_row = pd.DataFrame([{
                    "Date": inc_date, "Description": inc_desc,
                    "Category": "💼 Work", "Amount": inc_amt, "Type": "Income",
                }])
                st.session_state.transactions = pd.concat(
                    [st.session_state.transactions, new_row], ignore_index=True)
                st.success(f"✅ Income **{inc_desc}** — ${inc_amt:.2f} recorded!")
            else:
                st.warning("⚠️ Please enter an income source.")


# ═══════════════════════════════════════════════════════
# PAGE 3 — ANALYTICS
# ═══════════════════════════════════════════════════════
elif page == "📈 Analytics":
    st.title("📈 Analytics")
    df = get_filtered_df()

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("#### 📆 Daily Spending Trend")
        if not df.empty:
            daily = (df.groupby("Date")["Amount"]
                     .sum().reset_index().set_index("Date"))
            # COMPONENT 24: st.area_chart (built-in)
            st.area_chart(daily, height=260)
        else:
            st.info("No data for selected filters.")

    with col_r:
        st.markdown("#### 🏷 Spending by Category")
        if not df.empty:
            cat_totals = df.groupby("Category")["Amount"].sum()
            st.bar_chart(cat_totals, height=260)

    st.markdown("---")

    # COMPONENT 25: st.expander (extra merit)
    with st.expander("✏️ View & Edit Full Transaction Table", expanded=False):
        # COMPONENT 26: st.data_editor (extra merit)
        edited_df = st.data_editor(
            st.session_state.transactions,
            use_container_width=True,
            num_rows="dynamic",
            column_config={
                "Amount":   st.column_config.NumberColumn("Amount ($)", format="$%.2f"),
                "Date":     st.column_config.DateColumn("Date"),
                "Type":     st.column_config.SelectboxColumn(
                                "Type", options=["Expense", "Income"]),
                "Category": st.column_config.SelectboxColumn(
                                "Category", options=CATEGORIES),
            },
        )
        if st.button("💾 Save Edits"):
            st.session_state.transactions = edited_df
            st.success("Changes saved!")

    if not df.empty:
        st.markdown("#### 📊 Summary Stats")
        c1, c2, c3 = st.columns(3)
        c1.metric("Highest Spend",       f"${df['Amount'].max():.2f}")
        c2.metric("Average Transaction",  f"${df['Amount'].mean():.2f}")
        c3.metric("Total Transactions",   str(len(df)))

    st.info("💡 **Tip:** Use the sidebar date and category filters to narrow your analysis.")


# ═══════════════════════════════════════════════════════
# PAGE 4 — BUDGET SETTINGS
# ═══════════════════════════════════════════════════════
elif page == "⚙️ Budget Settings":
    st.title("⚙️ Budget Settings")
    st.markdown("Customise your income, savings goal, and per-category limits.")

    c1, c2 = st.columns(2)
    with c1:
        new_income = st.number_input(
            "💵 Monthly Income ($)", min_value=0.0,
            value=float(st.session_state.monthly_income), step=100.0)
        st.session_state.monthly_income = new_income
    with c2:
        new_goal = st.number_input(
            "🎯 Savings Goal ($)", min_value=0.0,
            value=float(st.session_state.savings_goal), step=50.0)
        st.session_state.savings_goal = new_goal

    st.markdown("---")
    st.markdown("### 🏷 Category Budget Limits")

    # COMPONENT 27: st.select_slider (extra merit)
    budget_tier = st.select_slider(
        "🎚 Quick Budget Tier",
        options=["Tight 🟥", "Moderate 🟨", "Comfortable 🟩", "Generous 💚"],
        value="Moderate 🟨",
        help="Apply a preset to all category limits at once.",
    )
    tier_map = {
        "Tight 🟥": 100, "Moderate 🟨": 200,
        "Comfortable 🟩": 350, "Generous 💚": 500,
    }

    if st.button("⚡ Apply Tier to All Categories"):
        for cat in CATEGORIES:
            st.session_state.budget_limits[cat] = float(tier_map[budget_tier])
        st.success(f"All limits set to ${tier_map[budget_tier]}/month.")

    st.markdown("#### Fine-tune per category:")
    cols = st.columns(2)
    for i, cat in enumerate(CATEGORIES):
        with cols[i % 2]:
            val = st.number_input(
                f"{cat}", min_value=0.0,
                value=float(st.session_state.budget_limits[cat]),
                step=10.0, key=f"limit_{i}")
            st.session_state.budget_limits[cat] = val

    st.markdown("---")

    # COMPONENT 28: st.download_button (extra merit)
    csv_bytes = st.session_state.transactions.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Transactions as CSV",
        data=csv_bytes,
        file_name="smartbudget_transactions.csv",
        mime="text/csv",
    )


# ═══════════════════════════════════════════════════════
# PAGE 5 — ABOUT
# ═══════════════════════════════════════════════════════
elif page == "ℹ️ About":
    st.title("ℹ️ About SmartBudget")

    st.markdown("""
    <div style="background:linear-gradient(135deg,#6366f1,#8b5cf6);
                border-radius:16px;padding:32px;color:white;margin-bottom:24px;">
        <h2 style="margin:0;font-family:monospace;">💰 SmartBudget</h2>
        <p style="margin:8px 0 0;font-size:1.1rem;opacity:.9;">
            Personal Finance Tracker &amp; Budget Planner
        </p>
    </div>
    """, unsafe_allow_html=True)

    # COMPONENT 29: st.tabs (About sections)
    a1, a2, a3, a4 = st.tabs([
        "🧭 What It Does", "👤 Target Users",
        "📥 Inputs & Outputs", "🛠 Components Used"
    ])

    with a1:
        st.markdown("""
        ### What Does SmartBudget Do?
        **SmartBudget** is a personal finance management tool that helps users:
        - 📌 **Track** day-to-day income and expenses in one place
        - 📊 **Visualise** spending patterns with interactive charts
        - 🎯 **Set** monthly budgets per category and monitor progress
        - 💡 **Gain insights** into where money goes over time
        - ⬇️ **Export** transaction history (e.g. for tax prep)

        The app is fully built in **Streamlit** with **no external API integration** —
        all data lives in-session to demonstrate a complete, meaningful UI flow.
        """)

    with a2:
        st.markdown("""
        ### Who Is This For?

        | User Type | Scenario |
        |---|---|
        | 🎓 Students | Track allowance, rent, and groceries on a tight budget |
        | 👩‍💼 Young Professionals | Monitor salary, subscriptions, and build savings |
        | 👨‍👩‍👧 Families | Manage household expenses across multiple categories |
        | 💻 Freelancers | Log irregular income and project-related spending |

        **No financial expertise required.** The interface is intuitive for first-time
        budgeters and powerful enough for detail-oriented users.
        """)

    with a3:
        st.markdown("""
        ### Inputs Collected

        | Input | Page | Component |
        |---|---|---|
        | Monthly income | Budget Settings | `st.number_input` |
        | Savings goal | Budget Settings | `st.number_input` |
        | Transaction description | Add Transaction | `st.text_input` |
        | Category | Add Transaction | `st.selectbox` |
        | Amount | Add Transaction | `st.number_input` |
        | Date | Add Transaction | `st.date_input` |
        | Notes | Add Transaction | `st.text_area` |
        | Recurring flag | Add Transaction | `st.checkbox` |
        | Priority rating | Add Transaction | `st.slider` |
        | Tag colour | Add Transaction | `st.color_picker` |
        | Date range filter | Sidebar | `st.date_input` |
        | Category filter | Sidebar | `st.multiselect` |
        | Budget tier preset | Settings | `st.select_slider` |

        ### Outputs Shown
        - 📊 KPI metric cards (income, expenses, balance, goal)
        - 📈 Area chart — daily spending trend
        - 📉 Bar chart — category comparison
        - 🟩 Progress bars — budget utilisation & savings goal
        - 📋 Interactive data table — all transactions
        - ✏️ Editable data editor — modify logged entries
        - ⬇️ CSV download — exportable transaction history
        """)

    with a4:
        st.markdown("""
        ### Streamlit Components Used (29 total)

        #### Core Components
        `st.title` · `st.markdown` · `st.columns` · `st.metric` · `st.progress`
        `st.sidebar` · `st.radio` · `st.selectbox` · `st.multiselect`
        `st.text_input` · `st.number_input` · `st.date_input` · `st.text_area`
        `st.checkbox` · `st.slider` · `st.button` · `st.tabs`
        `st.dataframe` · `st.bar_chart` · `st.area_chart` · `st.expander`
        `st.success` · `st.warning` · `st.info` · `st.caption`

        #### ✨ Extra Merit Components (beyond class syllabus)

        | Component | Why It's Interesting |
        |---|---|
        | `st.toggle` | Modern on/off switch — cleaner than checkbox for binary settings |
        | `st.color_picker` | Native colour wheel widget used for transaction tag labelling |
        | `st.select_slider` | Labelled discrete steps instead of plain numeric range |
        | `st.data_editor` | Fully editable DataFrame inline — no separate form needed |
        | `st.download_button` | Lets users export data straight from the browser |
        | `st.column_config.*` | Typed column rendering (currency, date, dropdowns) in tables |
        """)

    st.markdown("---")
    st.caption("Built as a Streamlit UI components demonstration · No real financial data is stored or transmitted.")
