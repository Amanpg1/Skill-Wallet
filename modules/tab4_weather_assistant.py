"""
Tab 4: Daily Site Assistant & Weather-Aware Advisory (Epic 5)
Dynamic Environmental Hazard Mitigation and Multi-Turn Civil Engineering AI Assistant.
"""

import streamlit as st
from utils.gemini_client import GeminiConstructionEngine

WEATHER_ADVISORIES = {
    "High Wind (>40 km/h)": {
        "class": "weather-wind",
        "icon": "💨",
        "title": "HIGH WIND SEVERE ALERT — CRANE SUSPENSION & AERODYNAMIC HAZARDS",
        "alerts": [
            "**OSHA 1926.1431 / IS 13367 Mandatory Directive:** Immediately suspend all tower crane and mobile crane lifting operations. Slew brakes MUST be released into free 'weathervane' rotation.",
            "**Scaffolding & Work at Height:** Evacuate external suspended working platforms (cradles) and perimeter facade brackets.",
            "**Material Securing:** Fasten and lash all loose GI sheets, plywood shuttering panels, insulation bundles, and lightweight materials on top decks."
        ],
        "badge_color": "#EF4444"
    },
    "Heavy Rain / Monsoon": {
        "class": "weather-rain",
        "icon": "🌧️",
        "title": "MONSOON ADVISORY — ELECTRICAL ISOLATION & DEWATERING PROTOCOL",
        "alerts": [
            "**Concrete Concreting Ban:** Postpone exposed slab pours to avoid water-cement (w/c) matrix dilution and surface paste washout.",
            "**Electrical Mitigation:** De-energize temporary distribution boards in low-lying zones; enforce IP65 weather-proof enclosures and 30mA RCD tripping tests.",
            "**Deep Excavations & Slopes:** Deploy heavy submersible sump pumps; inspect sheet pile shoring and trench perimeters for hydrostatic tension cracks (IS 3764)."
        ],
        "badge_color": "#3B82F6"
    },
    "Extreme Heat (>42°C)": {
        "class": "weather-heat",
        "icon": "☀️",
        "title": "HEAT STRESS PROTOCOL — CONCRETE CURING & SHIFT ROTATION",
        "alerts": [
            "**Hot Weather Concreting (IS 456 / ACI 305R):** Concrete placement temperature must not exceed 32°C. Utilize chilled batching water or shaved ice; add polycarboxylate ether (PCE) set retarders.",
            "**Intense Curing Protocol:** Apply liquid membrane-forming curing compounds immediately followed by saturated double-layer hessian fabric ponding.",
            "**Worker Thermal Safety:** Enforce mandatory 15-minute shaded hydration breaks every 45 minutes; reschedule rebar fixing to early morning (05:30 - 10:30) and post 16:00."
        ],
        "badge_color": "#F59E0B"
    },
    "Normal / Clear Weather": {
        "class": "weather-normal",
        "icon": "☀️",
        "title": "NORMAL WEATHER — OPTIMAL PRODUCTION STATUS",
        "alerts": [
            "**Full Site Clearance:** All heavy structural lifts, mass concreting, external glazing, and survey total station alignments authorized.",
            "**Standard Quality Gates:** Maintain 7-day ponding curing for OPC slabs (IS 456 Cl. 13.5).",
            "**Daily Routine:** Conduct routine daily morning Toolbox Talk (TBT) before shift kick-off."
        ],
        "badge_color": "#10B981"
    }
}

def render_tab4_weather_assistant(engine: GeminiConstructionEngine):
    st.markdown("### 🌦️ Daily Site Assistant & Weather-Aware Advisory (Epic 5)")
    st.markdown(
        "Dynamic environmental hazard monitoring aligned with real-time site conditions, coupled with "
        "an interactive multi-turn Construction Engineering Assistant chatbot versed in **IS 456**, **IS 800**, **IS 1893**, and **OSHA**."
    )

    # --------------------------------------------------------------------------
    # Weather Selector & Dynamic Safety Alerts
    # --------------------------------------------------------------------------
    st.markdown("#### 🌡️ Live Meteorological Site Condition Selector")
    col_w_select, col_w_summary = st.columns([1.2, 2])

    with col_w_select:
        current_weather = st.selectbox(
            "Select Current On-Site Weather Condition:",
            list(WEATHER_ADVISORIES.keys()),
            index=0,
            key="tab4_weather_dropdown"
        )
        adv_info = WEATHER_ADVISORIES[current_weather]

    with col_w_summary:
        st.markdown(
            f"""
            <div class="weather-banner {adv_info['class']}">
                <div style="font-size: 0.95rem; font-weight: 800; color: {adv_info['badge_color']}; margin-bottom: 0.4rem; display: flex; align-items: center; gap: 0.5rem;">
                    <span>{adv_info['icon']}</span> {adv_info['title']}
                </div>
                <div style="font-size: 0.86rem; line-height: 1.45;">
                    Current Active Protocols: <strong>{len(adv_info['alerts'])} Directives Enforced</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Display Alert Directives as Expandable Cards or List
    with st.expander(f"⚠️ View Detailed Safety Directives for '{current_weather}'", expanded=True):
        for alert_text in adv_info["alerts"]:
            st.markdown(f"- {alert_text}")

    # --------------------------------------------------------------------------
    # Interactive Multi-Turn Chatbot
    # --------------------------------------------------------------------------
    st.markdown("---")
    st.markdown("#### 💬 SiteMind: Interactive Construction Engineering Assistant")
    st.markdown(
        "*Ask technical questions on IS codes, structural mix designs, shoring calculations, "
        "formwork removal schedules, or OSHA compliance protocols.*"
    )

    # Initialize Chat History in Session State
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": f"Hello Engineer! I am **SiteMind AI**, your Chief Resident Civil & Safety Assistant. Current environmental conditions are set to **{current_weather}**. How can I assist your site operations today?"
            }
        ]

    # Quick Suggestion Chips
    st.markdown("**Quick Technical Queries:**")
    col_chip1, col_chip2, col_chip3, col_chip4 = st.columns(4)

    prompt_to_send = None

    with col_chip1:
        if st.button("📐 M25 Concrete Mix Design", use_container_width=True, key="chip_m25"):
            prompt_to_send = "Provide detailed M25 concrete mix design proportions per m³ as per IS 456 and IS 10262, including water-cement ratio and slump guidelines."
    with col_chip2:
        if st.button("🏗️ Tower Crane Wind Limits", use_container_width=True, key="chip_crane"):
            prompt_to_send = "What are the exact wind speed thresholds for suspending tower crane operations under IS 13367 and OSHA 1926? What is weathervane mode?"
    with col_chip3:
        if st.button("💧 Slab Curing & Deshoring", use_container_width=True, key="chip_curing"):
            prompt_to_send = "What are the mandatory curing duration and formwork stripping/deshoring intervals for slabs and beams under IS 456:2000 Clause 11.3?"
    with col_chip4:
        if st.button("⛏️ 4m Excavation Shoring", use_container_width=True, key="chip_shoring"):
            prompt_to_send = "What are the OSHA and IS 3764 safety requirements for trench excavation deeper than 3 meters in Type B soil?"

    # Render Chat History
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                with st.chat_message("user", avatar="👷"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("assistant", avatar="🏗️"):
                    st.markdown(msg["content"])

    # Chat Input Box
    user_input = st.chat_input("Type your civil engineering or site safety question here...")
    active_prompt = prompt_to_send if prompt_to_send else user_input

    if active_prompt:
        # Add user message to state
        st.session_state.chat_messages.append({"role": "user", "content": active_prompt})

        with st.chat_message("user", avatar="👷"):
            st.markdown(active_prompt)

        # Call engine for response
        with st.chat_message("assistant", avatar="🏗️"):
            with st.spinner("Consulting IS codes & OSHA standards..."):
                response_text, was_live = engine.chat_engineering_assistant(
                    messages=st.session_state.chat_messages,
                    current_weather=current_weather,
                    site_context="Active commercial high-rise construction"
                )
                st.markdown(response_text)
                if was_live:
                    st.caption("🟢 *Gemini 2.5 Live Response*")
                else:
                    st.caption("ℹ️ *Resident Engineering Knowledge Base*")

        # Save assistant message to state
        st.session_state.chat_messages.append({"role": "assistant", "content": response_text})

    # Clear Chat History Button
    col_clear, _ = st.columns([1, 4])
    with col_clear:
        if st.button("🗑️ Reset Chat History", key="tab4_clear_chat"):
            st.session_state.chat_messages = [
                {
                    "role": "assistant",
                    "content": f"Chat reset. Site condition is **{current_weather}**. Ready for new engineering inquiries."
                }
            ]
            st.rerun()
