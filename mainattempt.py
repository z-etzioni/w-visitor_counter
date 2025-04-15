import streamlit as st
import math
import requests
from supabase import create_client, Client

# ---------- Streamlit Config ----------
st.set_page_config(page_title="Econ Salary", page_icon="📈", layout="centered")

# ---------- Supabase Setup ----------
SUPABASE_URL = "https://auqqsiljywsnqghtechh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF1cXFzaWxqeXdzbnFnaHRlY2hoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ3MjEwMzAsImV4cCI6MjA2MDI5NzAzMH0.jaDhkMMokUoBIOep1x2gUvdo5kVNzLcd6P_LZbQm8f4"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------- Visitor Counter (Once Per Session) ----------
if "already_logged" not in st.session_state:
    try:
        supabase.table("visits").insert({}).execute()
    except Exception as e:
        st.warning("Visitor logging failed.")
    st.session_state["already_logged"] = True

# ---------- Get Visitor Count ----------
res = supabase.table("visits").select("id", count="exact").execute()
visits = res.count

# ---------- Title + Visitor Count ----------
st.title("Predicting Salaries of Economics Professors in the United States")
st.markdown(f"#### 👥 Total Visitors: `{visits}`")

# ---------- Salary Prediction Function ----------
def compute_y(TPhD, THired, N_pub, N_top5, Tenure, Full, USNews):
    log_y = 11.8194 + 0.019676 * TPhD - 0.00023849 * TPhD**2 - 0.01095 * THired \
        + 0.0015629 * (N_pub - N_top5) + 0.024239 * N_top5 \
        + 0.10954 * Tenure + 0.15688 * Full + 0.041223 * USNews + 0.06979 * (max(USNews - 3, 0))**2
    return int(round(1.029 * math.exp(log_y)))

# ---------- Custom Styles ----------
st.markdown("""
    <style>
    @media (prefers-color-scheme: dark) {
        .highlight-text {
            font-size: 20px;
            font-weight: bold;
            color: #FFFFFF !important;
            padding: 5px;
        }
        .list-text {
            font-size: 18px;
            color: #DDDDDD !important;
            padding-left: 15px;
        }
    }
    @media (prefers-color-scheme: light) {
        .highlight-text {
            font-size: 20px;
            font-weight: bold;
            color: #000000 !important;
            padding: 5px;
        }
        .list-text {
            font-size: 18px;
            color: #333333 !important;
            padding-left: 15px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Attribution ----------
st.markdown('<p class="highlight-text">Developed by:</p>', unsafe_allow_html=True)
st.markdown('<p class="list-text">- <a href="https://alexisakira.github.io/">Alexis Akira Toda</a>, Professor, Emory University (data analysis)</p>', unsafe_allow_html=True)
st.markdown('<p class="list-text">- <a href="https://www.linkedin.com/in/zachary-etzioni-5904aa296/">Zachary Etzioni</a>, Class of 2027, Emory University (web tool)</p>', unsafe_allow_html=True)

st.markdown('<p class="highlight-text">The prediction is based on the following parameters (R-squared 79%):</p>', unsafe_allow_html=True)
st.markdown('<p class="list-text">- Education</p>', unsafe_allow_html=True)
st.markdown('<p class="list-text">- Employment</p>', unsafe_allow_html=True)
st.markdown('<p class="list-text">- Publications</p>', unsafe_allow_html=True)

st.markdown('<p class="highlight-text">The predictive model is an extension of <a href="https://econjwatch.org/articles/publications-citations-position-and-compensation-of-economics-professors">Lyu and Toda (2019)</a></p>', unsafe_allow_html=True)
st.markdown('<p class="list-text">Disclaimer: the model is still experimental</p>', unsafe_allow_html=True)

# ---------- Input Form ----------
st.markdown('<p class="main-title">Enter your values below and click Compute Salary.</p>', unsafe_allow_html=True)

with st.container():
    TPhD = st.number_input("How many years ago did you finish PhD?", min_value=0, step=1, format="%d")
    THired = st.number_input("How many years have you been working at your current institution?", min_value=0, step=1, format="%d")
    N_pub = st.number_input("How many papers have you published? Please include only peer-reviewed research or review articles that you are comfortable listing in your CV under 'research'. Exclude books, book chapters, comments, conference proceedings (no AEA P&P, please!), corrigenda, handbook chapters, etc.", min_value=0, step=1, format="%d")
    N_top5 = st.number_input("How many papers have you published in so-called 'Top 5' economics journals?", min_value=0, step=1, format="%d")
    Tenure = st.radio("Do you have tenure? Choose Yes (1) or No (0).", [0, 1])
    Full = st.radio("Are you a full professor? Choose Yes (1) or No (0).", [0, 1])
    USNews = st.number_input("What is the [US News Peer Assessment Score](https://www.usnews.com/best-graduate-schools/top-humanities-schools/economics-rankings) of your department? Enter 1.0 if your school is not listed.", min_value=1.0, max_value=5.0, value="min", step=0.1, format="%0.1f")

if st.button("🔍 Compute Salary"):
    salary = compute_y(TPhD, THired, N_pub, N_top5, Tenure, Full, USNews)
    st.success(f"💰 Your expected salary in 2024 is **${salary:,}**")
