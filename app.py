import streamlit as st
import sqlite3
import re
import random

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="SOC Hacker Terminal",
    page_icon="🛡",
    layout="centered"
)

# ===================== DATABASE =====================
conn = sqlite3.connect("passwords.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS password_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password TEXT,
    score INTEGER,
    risk_level TEXT
)
""")
conn.commit()

# ===================== BREACHED PASSWORDS =====================
breached_passwords = ["123456", "password", "admin", "qwerty", "letmein"]

# ===================== ANALYSIS ENGINE =====================
def analyze_password(password):
    score = 5
    issues = []

    if len(password) < 8:
        score -= 1
        issues.append("Too short")

    if not re.search(r"[A-Z]", password):
        score -= 1
        issues.append("No uppercase")

    if not re.search(r"[a-z]", password):
        score -= 1
        issues.append("No lowercase")

    if not re.search(r"[0-9]", password):
        score -= 1
        issues.append("No numbers")

    if not re.search(r"[!@#$%^&*()]", password):
        score -= 1
        issues.append("No special characters")

    if password.lower() in breached_passwords:
        score = 0
        issues.append("BREACHED PASSWORD")

    if score >= 4:
        level = "LOW RISK"
    elif score >= 2:
        level = "MEDIUM RISK"
    else:
        level = "HIGH RISK"

    return score, level, issues

# ===================== SAVE =====================
def save_to_db(password, score, level):
    cursor.execute(
        "INSERT INTO password_logs VALUES (NULL, ?, ?, ?)",
        (password, score, level)
    )
    conn.commit()

# ===================== GENERATOR =====================
def generate_password():
    words = ["neo", "matrix", "cyber", "dark", "ghost", "zero", "root", "hack"]
    return random.choice(words) + str(random.randint(10, 99))

# ===================== HACKER HEADER =====================
st.markdown("""
    <h1 style='text-align: center; color: #00ff9f;'>
    🛡 SOC HACKER TERMINAL
    </h1>
    <h4 style='text-align: center; color: #39ff14;'>
    Password Security & Threat Analyzer
    </h4>
    <hr style='border: 1px solid #00ff9f;'>
""", unsafe_allow_html=True)

# ===================== INPUT =====================
password = st.text_input("💀 Enter Target Password", type="password")

col1, col2 = st.columns(2)

# ===================== GENERATE =====================
with col1:
    if st.button("🎲 Generate Password"):
        st.session_state["gen"] = generate_password()

if "gen" in st.session_state:
    st.success(f"🔐 Generated: {st.session_state['gen']}")

# ===================== ANALYZE =====================
with col2:
    if st.button("🔍 Run SOC Scan"):
        if not password:
            st.error("No input detected")
        else:
            score, level, issues = analyze_password(password)
            save_to_db(password, score, level)

            # COLORS
            if level == "LOW RISK":
                color = "🟢"
            elif level == "MEDIUM RISK":
                color = "🟡"
            else:
                color = "🔴"

            st.markdown(f"""
            ## 📡 SCAN RESULTS
            - Password: `{password}`
            - Score: **{score}/5**
            - Risk Level: {color} **{level}**
            """)

            if issues:
                st.markdown("### ⚠ Issues Detected")
                for i in issues:
                    st.write("•", i)

            if password.lower() in breached_passwords:
                st.error("🚨 COMPROMISED PASSWORD DETECTED (SIMULATED BREACH DB)")

# ===================== ANALYTICS =====================
st.markdown("---")
st.markdown("## 📊 SOC Intelligence Dashboard")

cursor.execute("SELECT risk_level FROM password_logs")
data = cursor.fetchall()

low = sum(1 for d in data if d[0] == "LOW RISK")
medium = sum(1 for d in data if d[0] == "MEDIUM RISK")
high = sum(1 for d in data if d[0] == "HIGH RISK")

st.markdown(f"""
🟢 Low Risk: **{low}**  
🟡 Medium Risk: **{medium}**  
🔴 High Risk: **{high}**
""")

# ===================== FOOTER =====================
st.markdown("""
<hr style='border:1px solid #00ff9f'>
<p style='text-align:center; color:#00ff9f'>
SOC Security Terminal | Developed by SM NTIBO
</p>
""", unsafe_allow_html=True)
