import streamlit as st

def inject_custom_css():
    """Inject premium CSS for a modern, glassmorphism look."""
    st.markdown("""
        <style>
            /* Global Styles */
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
            
            html, body, [data-testid="stSidebar"] {
                font-family: 'Outfit', sans-serif;
            }
            
            /* Background and Gradient */
            .main {
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                color: #f8fafc;
            }
            
            /* Sidebar Styling */
            [data-testid="stSidebar"] {
                background-color: rgba(15, 23, 42, 0.95);
                border-right: 1px solid rgba(255, 255, 255, 0.05);
            }
            
            /* Cards / Containers */
            div[data-testid="stVerticalBlockBorderWrapper"] {
                background: rgba(255, 255, 255, 0.03);
                backdrop-filter: blur(10px);
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.08);
                padding: 1.5rem;
                transition: all 0.3s ease;
            }
            
            div[data-testid="stVerticalBlockBorderWrapper"]:hover {
                background: rgba(255, 255, 255, 0.05);
                transform: translateY(-2px);
                border-color: rgba(255, 255, 255, 0.15);
            }
            
            /* Buttons */
            .stButton>button {
                border-radius: 12px;
                background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
                color: white;
                border: none;
                font-weight: 600;
                padding: 0.5rem 1rem;
                transition: all 0.2s ease;
            }
            
            .stButton>button:hover {
                opacity: 0.9;
                transform: scale(1.02);
                box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
            }
            
            /* Secondary Buttons (Delete/Neutral) */
            .stButton>button[kind="secondary"] {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            /* Form inputs */
            .stTextInput>div>div>input, .stTextArea>div>div>textarea {
                background-color: rgba(255, 255, 255, 0.03) !important;
                border-radius: 10px !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                color: white !important;
            }

            /* Metrics */
            [data-testid="stMetric"] {
                background: rgba(59, 130, 246, 0.1);
                border-radius: 12px;
                padding: 10px;
                border: 1px solid rgba(59, 130, 246, 0.2);
            }
            
            /* Custom Scrollbar */
            ::-webkit-scrollbar {
                width: 8px;
            }
            ::-webkit-scrollbar-track {
                background: rgba(255, 255, 255, 0.02);
            }
            ::-webkit-scrollbar-thumb {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 4px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: rgba(255, 255, 255, 0.2);
            }

            /* Dashboard Headers */
            h1, h2, h3 {
                background: linear-gradient(90deg, #ffffff 0%, #cbd5e1 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: 700;
            }
            
            .stDivider {
                border-color: rgba(255, 255, 255, 0.05);
            }
        </style>
    """, unsafe_allow_html=True)
