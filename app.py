"""
Multimodal Construction Intelligence Platform (Skill Wallet Capstone Project 1)
Production-Ready Streamlit Application for Enterprise Site Safety, Structural Integrity Forensics,
Real Estate Valuation Economics, and Autonomous Weather-Aware Advisory.
"""

import streamlit as st
import os
from utils.styles import get_custom_css, render_hero_banner
from utils.gemini_client import GeminiConstructionEngine
from modules.tab1_safety_ppe import render_tab1_safety_ppe
from modules.tab2_structural_cracks import render_tab2_structural_cracks
from modules.tab3_planning_valuation import render_tab3_planning_valuation
from modules.tab4_weather_assistant import render_tab4_weather_assistant

# Page Configuration
st.set_page_config(
    page_title="Multimodal Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom High-Precision CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# SIDEBAR: API KEY CONFIGURATION, DEMO FALLBACK & ARCHITECTURE OVERVIEW
# ------------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Engine Configuration")

    # API Key Input with Secure Masking
    env_key = os.getenv("GEMINI_API_KEY", "")
    api_key_input = st.text_input(
        "Google Gemini API Key",
        value=env_key,
        type="password",
        placeholder="AIzaSy...",
        help="Enter your Google Gemini API Key. If left empty, the platform automatically runs in Demonstration Mode with full forensic simulation.",
        key="global_api_key_input"
    )

    # Force Demonstration Mode Toggle
    force_demo = st.checkbox(
        "Run in Offline Demonstration Mode",
        value=False if (api_key_input and api_key_input.strip()) else True,
        help="Enable to test the entire platform without consuming Google Gemini API quotas.",
        key="toggle_force_demo"
    )

    # Model Selector
    model_choice = st.selectbox(
        "Multimodal AI Model",
        ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-1.5-flash"],
        index=0,
        help="Select Google Gemini foundation vision model.",
        key="model_selector"
    )

    # Determine Active Mode & Status Indicator
    effective_api_key = "" if force_demo else api_key_input.strip()
    engine = GeminiConstructionEngine(api_key=effective_api_key, model_name=model_choice)

    if engine.is_demo_mode:
        st.markdown(
            """
            <div style="background: rgba(245, 158, 11, 0.12); border: 1px solid rgba(245, 158, 11, 0.35); border-radius: 8px; padding: 0.65rem 0.85rem; margin-top: 0.5rem; margin-bottom: 1rem;">
                <div style="font-weight: 700; color: #F59E0B; font-size: 0.82rem; display: flex; align-items: center; gap: 0.4rem;">
                    <span>🟡</span> DEMO / MOCK MODE ACTIVE
                </div>
                <div style="font-size: 0.74rem; color: #94A3B8; margin-top: 0.25rem;">
                    Operating with resident civil forensic models. All modules & test scenarios are 100% interactive.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 8px; padding: 0.65rem 0.85rem; margin-top: 0.5rem; margin-bottom: 1rem;">
                <div style="font-weight: 700; color: #10B981; font-size: 0.82rem; display: flex; align-items: center; gap: 0.4rem;">
                    <span>🟢</span> GEMINI LIVE CONNECTED
                </div>
                <div style="font-size: 0.74rem; color: #94A3B8; margin-top: 0.25rem;">
                    Multimodal Vision active via <code>{model_choice}</code>.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")
    # Architecture Overview Section
    with st.expander("🏛️ Architecture & Epics Overview", expanded=True):
        st.markdown(
            """
            **Skill Wallet Capstone Project 1**
            * **Epic 2 (Site Safety & PPE Audit):** Multimodal detection of helmets, vests, safety harnesses & steel-toe boots under OSHA 1926 & IS 456.
            * **Epic 2 (Crack Diagnostics):** NDT concrete crack classification, fracture width (mm), shear overstress root causes & epoxy repair protocols.
            * **Epic 3 (Planning & Valuation):** Dynamic CapEx tracker, BoQ steel/cement estimator, Indian Tier 1/2/3 real estate valuation, & Pollinations AI 3D renders.
            * **Epic 5 (Daily Site Assistant):** Weather-triggered environmental alerts (crane limits, dewatering) & multi-turn civil engineering chatbot.
            """
        )

    # Civil Engineering Standards Quick Reference
    st.markdown("##### 📚 Regulatory Code Compliance")
    st.markdown(
        """
        - **IS 456:2000:** Code for Plain and Reinforced Concrete
        - **OSHA 1926:** Safety & Health Regulations for Construction
        - **IS 13920:2016:** Ductile Detailing of Reinforced Concrete
        - **IS 13367:** Safe Use of Cranes & Wind Limits
        - **NBC 2016:** National Building Code of India
        """
    )

    st.markdown("---")
    if st.button("🧹 Clear Session & Cache", use_container_width=True, key="btn_clear_cache"):
        st.session_state.clear()
        st.rerun()

    st.caption("v2.4.0-Production • Zero DB Dependencies • 1-Click Cloud Ready")

# ------------------------------------------------------------------------------
# MAIN APPLICATION INTERFACE
# ------------------------------------------------------------------------------
# Render Hero Banner
st.markdown(render_hero_banner(), unsafe_allow_html=True)

# 4 Core Tab Modules
tab1, tab2, tab3, tab4 = st.tabs([
    "🦺 1. Site Safety & PPE Audit (Epic 2)",
    "🧱 2. Crack Diagnostics & Structural Integrity (Epic 2)",
    "📊 3. Planning & Real Estate Valuation (Epic 3)",
    "🌦️ 4. Daily Site Assistant & Weather Advisory (Epic 5)"
])

with tab1:
    render_tab1_safety_ppe(engine)

with tab2:
    render_tab2_structural_cracks(engine)

with tab3:
    render_tab3_planning_valuation()

with tab4:
    render_tab4_weather_assistant(engine)

# ------------------------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #64748B; font-size: 0.8rem; padding: 1rem 0;">
        Multimodal Construction Intelligence Platform • Developed for Skill Wallet Capstone Project 1 • Engineered for Streamlit Community Cloud
    </div>
    """,
    unsafe_allow_html=True
)
