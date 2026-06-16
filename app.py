import streamlit as st
import sqlite3
import re
import random

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="SOC Terminal",
    layout="centered"
)

# ===================== HACKER DARK THEME =====================
st.markdown("""
<style>
/* Background */
.stApp {
    background-color: #050a0f;
    color: #00ff9f;
    font-family: "Courier New", monospace;
}

/* Input box */
input {
    background-color: #0b141a !important;
    color: #00ff9f !important;
    border: 1px solid #00ff9f !important;
}

/* Buttons */
.stButton button {
    background-color: #0b141a;
    color: #00ff9f;
    border: 1px solid #00ff9f;
    font-weight: bold;
}

.stButton button:hover {
    background-color: #00ff9f;
    color: #000000;
}

/* Titles */
h1, h2, h3, h4 {
    color: #00ff9f !important;
    font-family: "Courier New", monospace;
}

/* Divider */
hr {
    border: 1px solid #00ff9f;
}
</style>
""", unsafe_allow_html=True)

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
        issues.append("weak length")

    if not re.search(r"[A-Z]", password):
        score -= 1
        issues.append("missing uppercase")

    if not re.search(r"[a-z]", password):
        score -= 1
        issues.append("missing lowercase")

    if not re.search(r"[0-9]", password):
        score -= 1
        issues.append("missing numbers")

    if not re.search(r"[!@#$%^&*()]", password):
        score -= 1
        issues.append("missing symbols")

    if password.lower() in breached_passwords:
        score = 0
        issues.append("breached database match")

    if score >= 4:
        level = "LOW RISK"
    elif score >= 2:
        level = "MEDIUM RISK"
    else:
        level = "HIGH RISK"

    return score, level, issues

# ===================== SAVE DATA =====================
def save_to_db(password, score, level):
    cursor.execute(
        "INSERT INTO password_logs VALUES (NULL, ?, ?, ?)",
        (password, score, level)
    )
    conn.commit()

# ===================== PASSWORD GENERATOR =====================
def generate_password():
    words = ["neo", "matrix", "cyber", "dark", "root", "zero", "ghost", "signal"]
    return random.choice(words) + str(random.randint(10, 99))

# ===================== HEADER =====================
st.markdown("<h1>SOC TERMINAL INTERFACE</h1>", unsafe_allow_html=True)

st.markdown("System: Password Security Analyzer")
st.markdown("---")

# ===================== INPUT =====================
password = st.text_input("ENTER TARGET PASSWORD", type="password")

col1, col2 = st.columns(2)

# ===================== GENERATE =====================
with col1:
    if st.button("GENERATE PASSWORD"):
        st.session_state["gen"] = generate_password()

if "gen" in st.session_state:
    st.success(st.session_state["gen"])

# ===================== ANALYZE =====================
with col2:
    if st.button("RUN ANALYSIS"):
        if not password:
            st.error("NO INPUT DETECTED")
        else:
            score, level, issues = analyze_password(password)
            save_to_db(password, score, level)

            st.markdown("ANALYSIS RESULT")
            st.write("SCORE:", score, "/5")
            st.write("RISK LEVEL:", level)

            if issues:
                st.markdown("VULNERABILITIES DETECTED")
                for i in issues:
                    st.write("-", i)

            if password.lower() in breached_passwords:
                st.error("BREACH DATABASE MATCH FOUND")

# ===================== DASHBOARD =====================
st.markdown("---")
st.markdown("SECURITY DASHBOARD")

cursor.execute("SELECT risk_level FROM password_logs")
data = cursor.fetchall()

low = sum(1 for d in data if d[0] == "LOW RISK")
medium = sum(1 for d in data if d[0] == "MEDIUM RISK")
high = sum(1 for d in data if d[0] == "HIGH RISK")

st.write("LOW RISK:", low)
st.write("MEDIUM RISK:", medium)
st.write("HIGH RISK:", high)

st.markdown("---")
st.markdown("SOC TERMINAL | DEVELOPED BY SM NTIBO")
