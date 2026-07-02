import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# --- LOGO CONFIGURATION ---
# Change this to match your exact file name if it isn't "logo.png"
logo_filename = "logo.png" 

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Holcim Water Protect - Value Analyzer",
    page_icon="🏗️",
    layout="wide"
)

# --- CUSTOM BRANDING & LOGIN STYLES ---
st.markdown("""
    <style>
    .main-header { font-size:32px !important; font-weight: 800; color: #DC2626; margin-bottom: 5px; }
    .sub-header { font-size:16px !important; color: #4B5563; margin-bottom: 30px; }
    .card-std { background-color: #FEF2F2; padding: 20px; border-radius: 8px; border: 1px solid #FEE2E2; border-left: 6px solid #EF4444; }
    .card-hwp { background-color: #EFF6FF; padding: 20px; border-radius: 8px; border: 1px solid #DBEAFE; border-left: 6px solid #2563EB; }
    .card-savings { background-color: #ECFDF5; padding: 20px; border-radius: 8px; border: 1px solid #D1FAE5; border-left: 6px solid #10B981; }
    .signature-box { font-size: 13px; color: #6B7280; line-height: 1.4; border-top: 1px solid #E5E7EB; padding-top: 10px; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN SCRIPT VALIDATION ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_login, col_r = st.columns([1, 1.2, 1])
    
    with col_login:
        # 📸 Show PNG at the top of Login Portal
        if os.path.exists(logo_filename):
            st.image(logo_filename, use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
        st.header("🔑 Port Login")
        st.subheader("FrontDesk Bangladesh Ltd TCO Analyzer Portal")
        
        user_id = st.text_input("User ID (TSE01 to TSE10)").strip().upper()
        password = st.text_input("Password", type="password")
        
        # Valid credentials array logic
        valid_users = [f"TSE{str(i).zfill(2)}" for i in range(1, 11)]
        
        if st.button("Access Dashboard", use_container_width=True):
            if user_id in valid_users and password == "12121":
                st.session_state['authenticated'] = True
                st.session_state['user_id'] = user_id
                st.rerun()
            else:
                st.error("Invalid User ID or Password. Please try again.")
        
        # Admin Support Signature on Login Screen
        st.markdown("""
            <div class="signature-box">
                <b>🔑 Admin Support & Maintenance:</b><br>
                MD Abdullah Al Naim<br>
                Assistant Engineer, FrontDesk Bangladesh Ltd.
            </div>
        """, unsafe_allow_html=True)
    st.stop()

# --- MAIN APPLICATION LAYER ---
# 📸 Show PNG at the top of the Main Dashboard Portal
if os.path.exists(logo_filename):
    st.image(logo_filename, width=250) # You can adjust the width here to make it fit your logo design perfectly

# Header Area
st.markdown('<p class="main-header">Holcim Water Protect — Value Optimization Dashboard</p>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-header">Data-driven structural ROI analysis mapping initial material premiums against long-term asset failure costs. | <b>Session: {st.session_state["user_id"]}</b></p>', unsafe_allow_html=True)

# --- DEVELOPER SIGNATURE ON MAIN SCREEN ---
st.sidebar.markdown("""
    <div style="background-color: #F3F4F6; padding: 15px; border-radius: 6px; border-left: 4px solid #10B981; margin-bottom: 25px;">
        <span style="font-size: 11px; color: #6B7280; font-weight: bold; letter-spacing: 0.5px;">SYSTEM DEVELOPER</span><br>
        <span style="font-size: 15px; font-weight: 700; color: #111827;">MD Abdullah Al Naim</span><br>
        <span style="font-size: 12px; color: #4B5563;">Assistant Engineer</span><br>
        <span style="font-size: 12px; color: #4B5563; font-style: italic;">FrontDesk Bangladesh Ltd.</span>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR INPUTS ---
st.sidebar.header("🏢 1. Structural Scope")
floor_area = st.sidebar.number_input("Floor Area per Story (Sq. Ft.)", min_value=500, value=2000, step=100)
stories = st.sidebar.slider("Number of Stories", min_value=1, max_value=20, value=5)

st.sidebar.header("💰 2. Market Pricing (BDT)")
std_cement_price = st.sidebar.number_input("Standard Cement Price (per Bag)", min_value=400, value=560, step=10)
water_protect_price = st.sidebar.number_input("Holcim Water Protect Price (per Bag)", min_value=500, value=680, step=10)
sand_price_cft = st.sidebar.number_input("Sand Price (per CFT)", min_value=10, value=45, step=5)
paint_price_sqft = st.sidebar.number_input("Paint & Putty Cost (per Sq. Ft.)", min_value=5, value=35, step=5)

st.sidebar.header("⏱️ 3. Risk Horizon & Repairs")
failure_years = st.sidebar.slider("Projected Year of Plaster Failure", min_value=3, max_value=10, value=5)
repair_labor_sqft = st.sidebar.number_input("Repair Labor Cost (per Sq. Ft.)", min_value=10, value=65, step=5)

if st.sidebar.button("🚪 Log Out"):
    st.session_state['authenticated'] = False
    st.rerun()

# --- CALCULATIONS ---
external_plaster_area = floor_area * stories * 0.7
internal_plaster_area = floor_area * stories * 2.8
roof_screed_area = floor_area
total_surface_area = external_plaster_area + internal_plaster_area + roof_screed_area

def calculate_bags(area_sqft, thickness_inches):
    wet_volume = area_sqft * (thickness_inches / 12.0)
    dry_volume = wet_volume * 1.33
    cement_volume = dry_volume * (1 / 5)
    return cement_volume / 1.25

total_cement_bags = round(
    calculate_bags(internal_plaster_area, 0.5) + 
    calculate_bags(external_plaster_area, 0.75) + 
    calculate_bags(roof_screed_area, 0.75)
)
total_sand_cft = total_cement_bags * 4

# Financial Tally
total_std_cost = total_cement_bags * std_cement_price
total_hwp_cost = total_cement_bags * water_protect_price
upfront_premium = total_hwp_cost - total_std_cost

# Future Damage Costs
future_cement_damage = total_cement_bags * std_cement_price
future_sand_damage = total_sand_cft * sand_price_cft
future_paint_damage = total_surface_area * paint_price_sqft
future_labor_damage = total_surface_area * repair_labor_sqft
total_damage_bill = future_cement_damage + future_sand_damage + future_paint_damage + future_labor_damage

net_loss_prevented = total_damage_bill - upfront_premium

# --- FINANCIAL OVERVIEW CARDS ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="card-std">
        <span style="font-size: 13px; color: #7F1D1D; font-weight:700;">STANDARD CEMENT BUDGET</span><br>
        <span style="font-size: 28px; font-weight: 800; color: #B91C1C;">BDT {total_std_cost:,.0f}</span><br>
        <span style="font-size: 13px; color: #4B5563;">For {total_cement_bags:,} bags @ BDT {std_cement_price}/bag</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card-hwp">
        <span style="font-size: 13px; color: #1E3A8A; font-weight:700;">HOLCIM WATER PROTECT BUDGET</span><br>
        <span style="font-size: 28px; font-weight: 800; color: #1D4ED8;">BDT {total_hwp_cost:,.0f}</span><br>
        <span style="font-size: 13px; color: #4B5563;">Upfront Net Premium: <b>BDT {upfront_premium:,.0f}</b></span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card-savings">
        <span style="font-size: 13px; color: #065F46; font-weight:700;">NET VALUE SAVED (YEAR {failure_years})</span><br>
        <span style="font-size: 28px; font-weight: 800; color: #047857;">BDT {net_loss_prevented:,.0f}</span><br>
        <span style="font-size: 13px; color: #4B5563;">Avoided total breakdown and re-work costs</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- CHART INTERACTION ---
st.subheader("📊 Comparative Financial Lifecycle Analysis")

fig = go.Figure()
fig.add_trace(go.Bar(
    y=['Traditional Plan', 'Water Protect Plan'],
    x=[total_std_cost, total_hwp_cost],
    name='Initial Cement Cost',
    orientation='h',
    marker=dict(color='#3B82F6')
))
fig.add_trace(go.Bar(
    y=['Traditional Plan', 'Water Protect Plan'],
    x=[total_damage_bill, 0],
    name=f'Plaster Repair & Repainting Damage (Year {failure_years})',
    orientation='h',
    marker=dict(color='#EF4444'),
    hovertemplate='BDT %{x:,.0f}'
))

fig.update_layout(
    barmode='stack',
    height=250,
    margin=dict(l=20, r=20, t=10, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="center", x=0.5),
    xaxis=dict(title="Total Outflow (BDT)", tickformat=",.0f")
)
st.plotly_chart(fig, use_container_width=True)

# --- DETAIL SPAN ---
col_table, col_pitch = st.columns([4, 3])

with col_table:
    st.subheader(f"📋 Damage Breakdown Itemization (Year {failure_years})")
    
    breakdown_df = pd.DataFrame({
        "Expense Item": ["Chipping & Repair Labor", "Wall/Roof Repainting & Putty", "New Sand Procurement", "Replacement Cement Bags"],
        "Calculation Basis": [f"{total_surface_area:,.0f} Sq. Ft. @ BDT {repair_labor_sqft}", f"{total_surface_area:,.0f} Sq. Ft. @ BDT {paint_price_sqft}", f"{total_sand_cft:,} CFT @ BDT {sand_price_cft}", f"{total_cement_bags:,} Bags @ BDT {std_cement_price}"],
        "Cost Impact": [future_labor_damage, future_paint_damage, future_sand_damage, future_cement_damage]
    })
    breakdown_df["Cost Impact"] = breakdown_df["Cost Impact"].map("BDT {:,.0f}".format)
    st.table(breakdown_df)

with col_pitch:
    st.subheader("🎯 High-Ticket Sales Pitch Strategy")
    st.markdown(f"""
    When presenting this to a client, point directly to the red bar on the chart above and say:
    
    * **The Core Premise:** *"If you look at the chart, selecting a regular option isn't saving you money; it is simply delaying a massive **BDT {total_damage_bill:,.0f}** structural maintenance crisis."*
    * **The Premium Margin Value:** *"For a minor premium difference of **BDT {upfront_premium:,.0f}** at Day One, you eliminate the cost of completely stripping, re-plastering, and re-painting **{total_surface_area:,.0f} Sq. Ft.** of your building's core skin."*
    """)
    st.button("📄 Download Structural Executive Pitch Summary (PDF)", use_container_width=True)