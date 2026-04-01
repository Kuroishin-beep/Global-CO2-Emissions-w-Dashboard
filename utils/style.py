import streamlit as st

def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        * { font-family: 'Inter', sans-serif; }

        .main .block-container {
            padding: 1.5rem 2rem 2rem 2rem;
            max-width: 1400px;
        }

        /* Header */
        .dashboard-header {
            background: linear-gradient(135deg, #6C63FF 0%, #3B82F6 50%, #06B6D4 100%);
            padding: 2rem 2.5rem;
            border-radius: 16px;
            margin-bottom: 1.5rem;
            position: relative;
            overflow: hidden;
        }
        .dashboard-header::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -20%;
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
            border-radius: 50%;
        }
        .dashboard-header h1 {
            color: #fff;
            font-size: 2rem;
            font-weight: 800;
            margin: 0;
            letter-spacing: -0.5px;
        }
        .dashboard-header p {
            color: rgba(255,255,255,0.85);
            font-size: 1rem;
            margin: 0.4rem 0 0 0;
            font-weight: 400;
        }

        /* Metric cards */
        .metric-card {
            background: linear-gradient(145deg, #1E2235 0%, #171B2D 100%);
            border: 1px solid rgba(108,99,255,0.15);
            border-radius: 14px;
            padding: 1.25rem 1.5rem;
            text-align: center;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .metric-card:hover {
            transform: translateY(-2px);
            border-color: rgba(108,99,255,0.4);
        }
        .metric-value {
            font-size: 1.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, #6C63FF, #06B6D4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .metric-label {
            color: #8B8FA3;
            font-size: 0.8rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 0.3rem;
        }
        .metric-delta-up { color: #EF4444; font-size: 0.85rem; font-weight: 600; }
        .metric-delta-down { color: #10B981; font-size: 0.85rem; font-weight: 600; }

        /* Section titles */
        .section-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: #FAFAFA;
            margin: 1.5rem 0 0.75rem 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .section-title .icon { font-size: 1.3rem; }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #12152A 0%, #0E1117 100%);
        }
        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] .stMultiSelect label,
        section[data-testid="stSidebar"] .stSlider label {
            color: #A5A8BD !important;
            font-weight: 500;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.5px;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            background: transparent;
        }
        .stTabs [data-baseweb="tab"] {
            background: rgba(108,99,255,0.08);
            border-radius: 10px;
            padding: 0.5rem 1.2rem;
            color: #A5A8BD;
            font-weight: 500;
            border: 1px solid transparent;
        }
        .stTabs [aria-selected="true"] {
            background: rgba(108,99,255,0.2) !important;
            color: #fff !important;
            border-color: rgba(108,99,255,0.4) !important;
        }

        /* Expanders */
        .streamlit-expanderHeader {
            background: rgba(108,99,255,0.06);
            border-radius: 10px;
            font-weight: 600;
        }

        /* Hide Streamlit branding */
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header { visibility: hidden; }

        /* Download button */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #6C63FF, #3B82F6);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
        }
        .stDownloadButton > button:hover {
            background: linear-gradient(135deg, #5B54E6, #2563EB);
        }
    </style>
    """, unsafe_allow_html=True)
