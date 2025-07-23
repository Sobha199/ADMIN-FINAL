import streamlit as st
import pandas as pd
import time

# Load login credentials CSV
df = pd.read_csv("Login tracking (1).csv")
df.columns = df.columns.str.strip()

st.set_page_config(page_title="Admin Login", layout="centered")

# Styling
st.markdown("""
    <style>
    .stTextInput>div>div>input {
        background-color: black;
        color: white;
        border: 2px solid white;
        border-radius: 5px;
    }
    .stButton>button {
        background-color: skyblue;
        color: black;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.image("s2m-logo.png", width=200)
st.title("🔐 Admin Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")
login_button = st.button("Login")
if login_button:
        with st.spinner("Signing in..."):
            time.sleep(2)
            df = pd.read_csv("Login tracking (1).csv")
            if any((df["Username"] == username) & (df["Password"] == password)):
                st.success("Login successful!")
                st.session_state.logged_in = True
            else:
                st.error("Invalid credentials")
                
def admin_dashboard():
    st.title("Admin Dashboard")
    df = pd.read_csv("Login tracking (1).csv")

    st.subheader("Total HC")
    st.metric("Total HC", len(df))

    st.subheader("Tenurity Wise Deviation")
    st.write("Available columns:", df.columns.tolist())
    df['DOJ'] = pd.to_datetime(df['DOJ'], errors='coerce')
    df['TenureMonths'] = ((pd.to_datetime('today') - df['DOJ'])/pd.Timedelta(days=30)).fillna(0).astype(int)

    t1 = len(df[df['TenureMonths'] <= 6])
    t2 = len(df[(df['TenureMonths'] > 6) & (df['TenureMonths'] <= 12)])
    t3 = len(df[df['TenureMonths'] > 12])

    st.write(f"0-6 Months: {t1}")
    st.write(f"6-12 Months: {t2}")
    st.write(f">1 Year: {t3}")

    st.subheader("Internal Role-wise HC")
    st.dataframe(df["Internal Role"].value_counts())

    st.subheader("Login Count")
    st.metric("Login Count", df["Username"].nunique())

    st.subheader("Certified Count")
    st.metric("Certified", df[df["Certified"] == "Yes"].shape[0])

    st.subheader("Inactive Logins")
    st.metric("Inactive", df[df["Login Status"] == "Inactive"].shape[0])

    st.download_button("Download Raw Data", df.to_csv(index=False), "admin_data.csv", "text/csv")

def production_portal():
    st.title("Production Portal")
    df = pd.read_csv("data_dummy.csv")

    st.metric("Charts Completed", df[df["Chart Status"] == "Completed"].shape[0])
    st.metric("Pages Completed", df["Page No"].sum())
    st.metric("ICD Completed", df["No of Codes"].sum())
    st.metric("Working Days", df["Date"].nunique())

    st.download_button("Download Production Data", df.to_csv(index=False), "production_data.csv", "text/csv")

# Main App Flow
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    tab = st.sidebar.radio("Go to", ["Dashboard", "Production Portal"])
    if tab == "Dashboard":
        admin_dashboard()
    else:
        production_portal()
