"""
Tab 1: Site Safety & PPE Audit (Epic 2)
Multimodal Vision Inspection for OSHA 1926 & IS 456 Personal Protective Equipment (PPE) Compliance.
"""

import streamlit as st
import json
from PIL import Image
from utils.gemini_client import GeminiConstructionEngine
from utils.sample_images import (
    generate_safety_sample_violation,
    generate_safety_sample_compliant
)

def render_tab1_safety_ppe(engine: GeminiConstructionEngine):
    st.markdown("### 🦺 Site Safety & Worker PPE Compliance Audit (Epic 2)")
    st.markdown(
        "Autonomous multi-modal forensic inspection verifying personal protective equipment "
        "and physical site hazard protocols under **OSHA 1926**, **IS 456:2000**, and **IS 3696** standards."
    )

    # Top Control Bar: Upload vs Sample Scenarios
    col_input_mode, col_options = st.columns([2, 1])

    with col_input_mode:
        source_mode = st.radio(
            "Select Inspection Image Source:",
            ["📁 Upload Custom Site Photo", "⚡ Preloaded Test Scenarios (Instant 1-Click)"],
            horizontal=True,
            key="tab1_source_radio"
        )

    target_image: Image.Image = None
    image_name = "inspection_specimen.png"

    if source_mode == "📁 Upload Custom Site Photo":
        uploaded_file = st.file_uploader(
            "Upload Construction Site Photo (JPG, PNG, JPEG, WEBP)",
            type=["jpg", "jpeg", "png", "webp"],
            key="tab1_uploader",
            help="Upload clear high-resolution job site photography depicting active trades or scaffolding."
        )
        if uploaded_file is not None:
            try:
                target_image = Image.open(uploaded_file)
                image_name = uploaded_file.name
            except Exception as e:
                st.error(f"Failed to read image file: {e}")
        else:
            st.info("👆 Please upload a site image, or toggle 'Preloaded Test Scenarios' above for instant verification.")
    else:
        sample_choice = st.selectbox(
            "Choose Synthetic Test Scenario:",
            [
                "Scenario A: Elevated Scaffolding & Fall Arrest Hazard (High Risk)",
                "Scenario B: Deep Trench Excavation Crew (Fully Compliant)"
            ],
            key="tab1_sample_select"
        )
        if "Scenario A" in sample_choice:
            target_image = generate_safety_sample_violation()
            image_name = "scaffold_violation_specimen.png"
        else:
            target_image = generate_safety_sample_compliant()
            image_name = "trench_compliant_specimen.png"

    # Display image preview & run button
    if target_image is not None:
        col_img, col_act = st.columns([1.2, 1])

        with col_img:
            st.image(
                target_image,
                caption=f"Selected Audit Specimen: {image_name}",
                use_container_width=True
            )

        with col_act:
            st.markdown("#### 🔍 Inspection Configuration")
            site_zone = st.text_input(
                "Site Sector / Zone ID",
                value="Sector 4 - Tower B Structural Superstructure",
                key="tab1_zone_id"
            )
            audit_shift = st.selectbox(
                "Audit Shift & Conditions",
                ["Morning Shift (Active Concrete Pour)", "Afternoon Shift (Facade Erection)", "Night Shift (Tower Crane Lift)"],
                key="tab1_shift"
            )
            regulatory_code = st.multiselect(
                "Compliance Standards Active",
                ["OSHA 1926 (Safety & Health)", "IS 456:2000 (RCC Construction)", "IS 3696 (Scaffolding & Ladders)", "NBC 2016 Part 7"],
                default=["OSHA 1926 (Safety & Health)", "IS 456:2000 (RCC Construction)"],
                key="tab1_regs"
            )

            st.write("")
            run_audit_btn = st.button(
                "🚀 Execute AI Safety & PPE Audit",
                type="primary",
                use_container_width=True,
                key="tab1_run_btn"
            )

            if engine.is_demo_mode:
                st.caption("ℹ️ *Running in Intelligent Demonstration Mode (API key optional).*")
            else:
                st.caption(f"🟢 *Live Multi-Modal Gemini Connected ({engine.model_name})*")

        # Execute Audit Logic
        if run_audit_btn or f"tab1_audit_result_{image_name}" in st.session_state:
            result_key = f"tab1_audit_result_{image_name}"

            if run_audit_btn or result_key not in st.session_state:
                with st.spinner("Analyzing worker PPE items and structural hazard contours..."):
                    context_str = f"Site Zone: {site_zone}, Shift: {audit_shift}, Standards: {', '.join(regulatory_code)}"
                    audit_data, was_live = engine.audit_site_safety_ppe(target_image, custom_context=context_str)
                    st.session_state[result_key] = (audit_data, was_live)

            audit_data, was_live = st.session_state[result_key]

            st.markdown("---")
            st.markdown("### 📋 Executive Safety Audit Report")

            # Top Metric Highlights
            score = audit_data.get("safety_score", 70)
            status = audit_data.get("overall_status", "Needs Attention")
            workers_count = audit_data.get("workers_observed_count", 2)

            col_m1, col_m2, col_m3, col_m4 = st.columns(4)

            with col_m1:
                st.metric("Safety Index Score", f"{score} / 100")
                if score >= 80:
                    st.markdown("<span class='status-badge status-compliant'>PASS: Highly Compliant</span>", unsafe_allow_html=True)
                elif score >= 50:
                    st.markdown("<span class='status-badge status-warning'>WARN: Needs Attention</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span class='status-badge status-critical'>FAIL: Critical Non-Compliance</span>", unsafe_allow_html=True)

            with col_m2:
                st.metric("Overall Site Status", status)
                mode_label = "Gemini Live Vision" if was_live else "Resident Demo Engine"
                st.caption(f"Inspection Engine: `{mode_label}`")

            with col_m3:
                st.metric("Workers In Frame", workers_count)
                st.caption("Auto-detected personnel count")

            with col_m4:
                hazards_list = audit_data.get("site_hazards", [])
                critical_count = sum(1 for h in hazards_list if h.get("severity") in ["Critical", "High"])
                st.metric("High/Critical Hazards", critical_count)
                if critical_count > 0:
                    st.markdown("<span class='status-badge status-critical'>Immediate Action Required</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span class='status-badge status-compliant'>Zero Severe Hazards</span>", unsafe_allow_html=True)

            # Executive Summary Callout
            st.info(f"**Safety Summary:** {audit_data.get('summary', 'Audit completed successfully.')}")

            # Two Column Breakdown: PPE Detection Checklist vs Site Hazards
            col_ppe, col_hazards = st.columns([1.1, 1.4])

            with col_ppe:
                st.markdown("#### 🛡️ Worker PPE Detection Matrix")
                ppe_items = audit_data.get("ppe_detection", [])
                for item in ppe_items:
                    name = item.get("item", "Item")
                    st_val = item.get("status", "Detected")
                    rate = item.get("compliance_rate", "N/A")
                    notes = item.get("notes", "")
                    std = item.get("standard", "")

                    if "Compliant" in st_val and "Non" not in st_val and "Partially" not in st_val:
                        icon = "✅"
                        badge_cls = "status-compliant"
                    elif "Partially" in st_val:
                        icon = "⚠️"
                        badge_cls = "status-warning"
                    elif "Not Applicable" in st_val:
                        icon = "➖"
                        badge_cls = "status-badge"
                    else:
                        icon = "❌"
                        badge_cls = "status-critical"

                    st.markdown(
                        f"""
                        <div class="checklist-row">
                            <div>
                                <span class="checklist-name">{icon} <strong>{name}</strong></span>
                                <div style="font-size: 0.75rem; color: #64748B;">{std}</div>
                                <div style="font-size: 0.8rem; margin-top: 0.2rem;">{notes}</div>
                            </div>
                            <div style="text-align: right;">
                                <span class="status-badge {badge_cls}">{rate}</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            with col_hazards:
                st.markdown("#### ⚠️ Identified Site Hazards & Corrective Remedies")
                for h in hazards_list:
                    sev = h.get("severity", "Medium")
                    if sev == "Critical":
                        sev_cls = "sev-critical"
                    elif sev == "High":
                        sev_cls = "sev-high"
                    elif sev == "Medium":
                        sev_cls = "sev-medium"
                    else:
                        sev_cls = "sev-low"

                    st.markdown(
                        f"""
                        <div class="eng-card">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                                <span class="severity-badge {sev_cls}">{sev} SEVERITY</span>
                                <span style="font-size: 0.75rem; font-weight: 600; color: #EF4444;">⏱️ {h.get('resolution_timeframe', 'Within 2 Hours')}</span>
                            </div>
                            <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 0.2rem;">
                                {h.get('hazard', 'Unspecified Hazard')}
                            </div>
                            <div style="font-size: 0.8rem; color: #94A3B8; margin-bottom: 0.4rem;">
                                📍 <em>Location: {h.get('location_element', 'Job Site')}</em> | <strong>{h.get('standard_code', 'OSHA 1926')}</strong>
                            </div>
                            <div style="font-size: 0.84rem; background: rgba(245, 158, 11, 0.08); padding: 0.5rem 0.7rem; border-radius: 6px; border-left: 3px solid #F59E0B;">
                                <strong>Corrective Remedy:</strong> {h.get('corrective_remedy', 'Mitigate immediately.')}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            # Recommended Actions Checklist
            actions = audit_data.get("recommended_safety_actions", [])
            if actions:
                st.markdown("#### 🎯 Mandated Corrective Protocols")
                for idx, act in enumerate(actions, 1):
                    st.checkbox(f"**Step {idx}:** {act}", key=f"action_chk_{idx}")

            # Downloadable Reports
            st.markdown("---")
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                json_str = json.dumps(audit_data, indent=2)
                st.download_button(
                    label="📥 Download Structured JSON Safety Report",
                    data=json_str,
                    file_name=f"site_safety_audit_{image_name.split('.')[0]}.json",
                    mime="application/json",
                    use_container_width=True
                )
            with col_d2:
                markdown_report = f"""# Construction Site Safety & PPE Audit Report
**Target Image:** {image_name}
**Safety Score:** {score} / 100 ({status})
**Workers Observed:** {workers_count}
**Standards:** OSHA 1926 / IS 456:2000 / IS 3696

## Executive Summary
{audit_data.get('summary', '')}

## PPE Checklist
{json.dumps(audit_data.get('ppe_detection', []), indent=2)}

## Site Hazards & Corrective Actions
{json.dumps(audit_data.get('site_hazards', []), indent=2)}
"""
                st.download_button(
                    label="📄 Download Markdown Audit Dossier",
                    data=markdown_report,
                    file_name=f"site_safety_audit_{image_name.split('.')[0]}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
