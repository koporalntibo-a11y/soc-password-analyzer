import streamlit as st
import sqlite3
import re
import random

# ===================== PAGE CONFIG =====================
st.set_page_config(page_title="SOC Password Analyzer", layout="centered")

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
        issues.append("BREACHED PASSWORD DETECTED")

    if score >= 4:
        level = "LOW RISK"
    elif score >= 2:
        level = "MEDIUM RISK"
    else:
        level = "HIGH RISK"

    return score, level, issues

# ===================== SAVE TO DB =====================
def save_to_db(password, score, level):
    cursor.execute(
        "INSERT INTO password_logs (password, score, risk_level) VALUES (?, ?, ?)",
        (password, score, level)
    )
    conn.commit()

# ===================== PASSWORD GENERATOR =====================
def generate_password():
    words = ["sun", "blue", "river", "code", "lion", "cloud", "star", "tech"]
    return random.choice(words) + str(random.randint(10, 99))

# ===================== UI =====================

st.title("🛡 SOC Password Security Analyzer")
st.write("Cybersecurity tool for password strength and breach detection")

password = st.text_input("Enter Password", type="password")

col1, col2 = st.columns(2)

# Generate password
with col1:
    if st.button("Generate Password"):
        st.session_state["generated"] = generate_password()

if "generated" in st.session_state:
    st.success(f"Generated Password: {st.session_state['generated']}")

# Analyze password
with col2:
    if st.button("Analyze Password"):
        if not password:
            st.error("Please enter a password")
        else:
            score, level, issues = analyze_password(password)

            save_to_db(password, score, level)

            st.subheader("Analysis Result")
            st.write("Score:", score, "/ 5")
            st.write("Risk Level:", level)

            if issues:
                st.warning("Issues Found:")
                for i in issues:
                    st.write("•", i)

            if password.lower() in breached_passwords:
                st.error("🚨 Password found in breached database!")

# ===================== ANALYTICS =====================
st.divider()
st.subheader("📊 SOC Analytics Dashboard")

cursor.execute("SELECT risk_level FROM password_logs")
data = cursor.fetchall()

low = sum(1 for d in data if d[0] == "LOW RISK")
medium = sum(1 for d in data if d[0] == "MEDIUM RISK")
high = sum(1 for d in data if d[0] == "HIGH RISK")

st.write("Low Risk:", low)
st.write("Medium Risk:", medium)
st.write("High Risk:", high)

# ===================== FOOTER =====================
st.divider()
st.caption("SOC Password Analyzer | Developed by SM NTIBO")
