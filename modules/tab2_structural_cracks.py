"""
Tab 2: Crack Diagnostics & Structural Integrity (Epic 2)
AI Forensic Vision for Concrete Defect Classification, Crack Width Forensics & Structural Remediation.
"""

import streamlit as st
import json
from PIL import Image
from utils.gemini_client import GeminiConstructionEngine
from utils.sample_images import (
    generate_crack_structural_shear,
    generate_crack_spalling_rebar,
    generate_crack_hairline_plaster
)

def render_tab2_structural_cracks(engine: GeminiConstructionEngine):
    st.markdown("### 🧱 Concrete Defect Pathology & Structural Integrity Diagnostics (Epic 2)")
    st.markdown(
        "Automated multimodal defect classification, fracture width estimation, root cause forensics, "
        "and engineering repair protocols adhering to **IS 456:2000 (Clause 35.3.2)**, **IS 13920**, and **ACI 224R-01**."
    )

    # Input Mode Selection
    col_mode, col_info = st.columns([2, 1])
    with col_mode:
        source_mode = st.radio(
            "Select Concrete Surface Specimen Source:",
            ["📁 Upload Surface Photo", "⚡ Preloaded Forensic Specimens (Instant 1-Click)"],
            horizontal=True,
            key="tab2_source_radio"
        )

    target_image: Image.Image = None
    specimen_name = "crack_specimen.png"

    if source_mode == "📁 Upload Surface Photo":
        uploaded_file = st.file_uploader(
            "Upload Concrete or Masonry Surface Image (JPG, PNG, JPEG)",
            type=["jpg", "jpeg", "png", "webp"],
            key="tab2_uploader",
            help="Upload clear close-up photography of concrete cracks, beams, columns, or retaining walls."
        )
        if uploaded_file is not None:
            try:
                target_image = Image.open(uploaded_file)
                specimen_name = uploaded_file.name
            except Exception as e:
                st.error(f"Failed to read image file: {e}")
        else:
            st.info("👆 Upload an image or select a preloaded forensic specimen to begin structural analysis.")
    else:
        sample_choice = st.selectbox(
            "Select Forensic Specimen:",
            [
                "Specimen 1: 45° Diagonal Structural Shear Crack (Critical Failure Risk)",
                "Specimen 2: Severe Concrete Spalling with Exposed Corroding Rebar",
                "Specimen 3: Superficial Plaster Hairline Crazing (Drying Shrinkage)"
            ],
            key="tab2_sample_select"
        )
        if "Specimen 1" in sample_choice:
            target_image = generate_crack_structural_shear()
            specimen_name = "shear_crack_45deg.png"
        elif "Specimen 2" in sample_choice:
            target_image = generate_crack_spalling_rebar()
            specimen_name = "spalling_rebar_corrosion.png"
        else:
            target_image = generate_crack_hairline_plaster()
            specimen_name = "hairline_plaster_crazing.png"

    if target_image is not None:
        col_img, col_cfg = st.columns([1.2, 1])

        with col_img:
            st.image(
                target_image,
                caption=f"Specimen: {specimen_name}",
                use_container_width=True
            )

        with col_cfg:
            st.markdown("#### ⚙️ Structural Element Context")
            elem_type = st.selectbox(
                "Structural Member Inspected",
                [
                    "RCC Deep Beam (Shear Zone near Support)",
                    "Main Structural Column / Shear Wall",
                    "Suspended Floor Slab / Cantilever Balcony",
                    "Foundation Retaining Wall / Footing",
                    "External AAC Block Masonry Wall"
                ],
                key="tab2_elem_select"
            )
            concrete_grade = st.selectbox(
                "Design Concrete Grade",
                ["M25 (Standard)", "M30 (RCC Slabs/Beams)", "M40/M50 (Columns/High-Rise)", "M15 (Lean Masonry)"],
                index=1,
                key="tab2_conc_grade"
            )
            exposure_cond = st.selectbox(
                "Environmental Exposure (IS 456 Table 3)",
                ["Moderate (Sheltered from severe rain)", "Severe (Direct coastal spray / wetting)", "Extreme (Aggressive chemicals/groundwater)"],
                key="tab2_exposure"
            )

            st.write("")
            run_diag_btn = st.button(
                "🔬 Execute Structural Integrity Diagnosis",
                type="primary",
                use_container_width=True,
                key="tab2_run_btn"
            )

            if engine.is_demo_mode:
                st.caption("ℹ️ *Running in Intelligent Demonstration Mode (API key optional).*")
            else:
                st.caption(f"🟢 *Live Multi-Modal Gemini Connected ({engine.model_name})*")

        # Diagnosis Processing
        diag_key = f"tab2_diag_{specimen_name}"
        if run_diag_btn or diag_key in st.session_state:
            if run_diag_btn or diag_key not in st.session_state:
                with st.spinner("Analyzing concrete fracture path, width, and shear mechanics..."):
                    diag_data, was_live = engine.diagnose_structural_crack(target_image, element_type=elem_type)
                    st.session_state[diag_key] = (diag_data, was_live)

            diag_data, was_live = st.session_state[diag_key]

            st.markdown("---")
            st.markdown("### 📊 Forensic Structural Assessment Report")

            # High Level Metrics
            defect_type = diag_data.get("defect_type", "Structural Shear")
            crack_width = diag_data.get("estimated_crack_width_mm", 2.5)
            severity = diag_data.get("structural_severity", "Critical")
            urgency = diag_data.get("urgency", "Immediate Structural Intervention")

            col_m1, col_m2, col_m3, col_m4 = st.columns(4)

            with col_m1:
                st.metric("Classified Defect Type", defect_type)
                st.markdown(f"<span class='status-badge status-critical'>{defect_type}</span>", unsafe_allow_html=True)

            with col_m2:
                st.metric("Estimated Crack Width", f"{crack_width} mm")
                # IS 456 limit is 0.2mm for moderate, 0.3mm for mild
                if crack_width <= 0.2:
                    st.markdown("<span class='status-badge status-compliant'>≤ 0.2mm (IS 456 Permissible)</span>", unsafe_allow_html=True)
                elif crack_width <= 0.4:
                    st.markdown("<span class='status-badge status-warning'>0.2 - 0.4mm (Moderate Serviceability Breach)</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span class='status-badge status-critical'>> 0.4mm (Severe Structural Violation)</span>", unsafe_allow_html=True)

            with col_m3:
                st.metric("Structural Severity", severity)
                if severity == "Critical":
                    st.markdown("<span class='severity-badge sev-critical'>CRITICAL</span>", unsafe_allow_html=True)
                elif severity == "High":
                    st.markdown("<span class='severity-badge sev-high'>HIGH</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span class='severity-badge sev-medium'>MODERATE</span>", unsafe_allow_html=True)

            with col_m4:
                st.metric("Remediation Urgency", urgency)
                st.caption(f"Engine: `{'Gemini 2.5 Live' if was_live else 'Resident Forensic Engine'}`")

            # Impact Analysis Card
            st.markdown(
                f"""
                <div class="eng-card" style="border-left: 5px solid #EF4444;">
                    <div class="eng-card-title">⚠️ Structural Forensic Pathology & Capacity Impact</div>
                    <p style="font-size: 0.92rem; line-height: 1.5; margin-bottom: 0.5rem;">
                        {diag_data.get('structural_impact_analysis', '')}
                    </p>
                    <div class="citation-box">
                        <strong>Standard Citation:</strong> IS 456:2000 Clause 35.3.2 specifies that the surface width of cracks shall not exceed <strong>0.3 mm</strong> in members where cracking is not harmful to durability and <strong>0.2 mm</strong> where members are directly exposed to moisture or aggressive chemical atmospheres.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Two Column: Root Causes vs Engineering Repairs
            col_rc, col_repairs = st.columns([1, 1.3])

            with col_rc:
                st.markdown("#### 🔬 Root Cause Forensic Breakdown")
                causes = diag_data.get("root_causes", [])
                for idx, c in enumerate(causes, 1):
                    st.markdown(
                        f"""
                        <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(148, 163, 184, 0.15); border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 0.6rem;">
                            <div style="font-weight: 700; color: #F59E0B; font-size: 0.85rem; margin-bottom: 0.2rem;">Hypothesis #{idx}</div>
                            <div style="font-size: 0.88rem;">{c}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.markdown("#### 📡 Non-Destructive Testing (NDT) Protocol")
                st.info(diag_data.get("monitoring_protocol", "Install crack gauges."))

            with col_repairs:
                st.markdown("#### 🛠️ Recommended Engineering Repair Specification")
                repairs = diag_data.get("recommended_repairs", [])
                for r in repairs:
                    st.markdown(
                        f"""
                        <div class="eng-card" style="border-left: 4px solid #10B981;">
                            <div style="font-size: 0.95rem; font-weight: 700; color: #10B981; margin-bottom: 0.3rem;">
                                🔧 {r.get('method', 'Repair Method')}
                            </div>
                            <div style="font-size: 0.86rem; margin-bottom: 0.4rem; color: #E2E8F0;">
                                {r.get('specification', '')}
                            </div>
                            <div style="font-size: 0.76rem; color: #94A3B8;">
                                📋 Code Baseline: <strong>{r.get('code_standard', 'IS 456 / ACI 546R')}</strong>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            # Export Forensic Dossier
            st.markdown("---")
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.download_button(
                    "📥 Download JSON Forensic Dossier",
                    data=json.dumps(diag_data, indent=2),
                    file_name=f"structural_crack_forensics_{specimen_name.split('.')[0]}.json",
                    mime="application/json",
                    use_container_width=True
                )
            with col_d2:
                report_md = f"""# Structural Forensic & Concrete Defect Diagnosis Dossier
**Element:** {elem_type} | **Grade:** {concrete_grade}
**Defect:** {defect_type} | **Width:** {crack_width} mm | **Severity:** {severity}
**Urgency:** {urgency}

## Engineering Impact
{diag_data.get('structural_impact_analysis', '')}

## Recommended Structural Repairs
{json.dumps(diag_data.get('recommended_repairs', []), indent=2)}
"""
                st.download_button(
                    "📄 Download Structural Diagnostic Report (.md)",
                    data=report_md,
                    file_name=f"structural_crack_forensics_{specimen_name.split('.')[0]}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
