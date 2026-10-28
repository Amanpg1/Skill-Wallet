"""
Tab 3: Planning & Real Estate Valuation (Epic 3)
Interactive Project Budgeting, Capital Expenditure (CapEx) Tracking, BoQ Materials,
Asset Valuation in INR (Lakhs/Crores), and Pollinations AI 3D Architectural Rendering.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.valuation_calculator import ConstructionValuationEngine

def render_tab3_planning_valuation():
    st.markdown("### 📊 Planning, CapEx & Real Estate Valuation (Epic 3)")
    st.markdown(
        "Interactive civil project economics engine: computes total construction budgets, "
        "CapEx incurred, real-time Indian market asset valuation (₹ Lakhs/Crores), Bill of Quantities (BoQ) "
        "for Steel & Cement, and conceptual 3D architectural visualization."
    )

    # Top Control Cards: Interactive Inputs
    with st.container():
        st.markdown("#### 🏗️ Project Parameters & Site Geometry")
        col1, col2, col3 = st.columns(3)

        with col1:
            structure_type = st.selectbox(
                "Structure Type",
                list(ConstructionValuationEngine.STRUCTURE_BENCHMARKS.keys()),
                index=0,
                key="tab3_structure_type"
            )

        with col2:
            built_up_sqft = st.number_input(
                "Total Built-up Area (Sq. Ft.)",
                min_value=5_000,
                max_value=2_000_000,
                value=125_000,
                step=5_000,
                key="tab3_built_up_sqft",
                help="Total gross constructed slab area across all floors."
            )

        with col3:
            location_tier = st.selectbox(
                "Urban Location Tier (Indian Cities)",
                [
                    "Tier 1 (Mumbai, Bengaluru, Delhi NCR)",
                    "Tier 2 (Pune, Hyderabad, Ahmedabad, Chennai)",
                    "Tier 3 (Emerging Hubs, Jaipur, Indore, Kochi)"
                ],
                index=0,
                key="tab3_location_tier"
            )

        # Milestone Completion Slider
        st.write("")
        completion_pct = st.slider(
            "Overall Project Construction Completion (%)",
            min_value=0,
            max_value=100,
            value=45,
            step=1,
            key="tab3_completion_slider",
            help="Drag to dynamically recompute CapEx, steel/cement consumption, and current asset market valuation."
        )

    # Compute Valuation & BoQ Metrics
    metrics = ConstructionValuationEngine.calculate_project_metrics(
        structure_type=structure_type,
        built_up_sqft=built_up_sqft,
        location_tier=location_tier,
        completion_pct=completion_pct
    )

    # Milestone Progress Bar & Stage Indicator
    st.markdown("---")
    st.markdown(f"#### 🚩 Construction Milestone Progress: **{completion_pct}%**")
    st.progress(completion_pct / 100.0)
    st.markdown(
        f"""
        <div style="background: rgba(255, 255, 255, 0.04); border-left: 4px solid {metrics['stage_color']}; padding: 0.6rem 1rem; border-radius: 6px; margin-bottom: 1.2rem;">
            <strong>Current Active Milestone Stage:</strong> <span style="color: {metrics['stage_color']}; font-weight: 700;">{metrics['current_stage']}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Primary Financial Metric Cards (INR Lakhs / Crores)
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)

    with col_f1:
        st.metric(
            "Total Construction Budget",
            metrics["total_budget_formatted"],
            help=f"Based on ₹{metrics['base_rate_per_sqft']:,} / sq.ft. base civil construction benchmark."
        )
        st.caption(f"Base Rate: ₹{metrics['base_rate_per_sqft']:,}/sqft")

    with col_f2:
        st.metric(
            "CapEx Incurred to Date",
            metrics["capex_incurred_formatted"],
            delta=f"{completion_pct}% Deployed",
            delta_color="normal"
        )
        remaining_budget = metrics["total_budget_inr"] - metrics["capex_incurred_inr"]
        from utils.valuation_calculator import format_inr
        st.caption(f"Remaining: {format_inr(remaining_budget)}")

    with col_f3:
        st.metric(
            "Current Asset Valuation",
            metrics["current_market_valuation_formatted"],
            help="Current market asset value considering land equity share and completed structural work."
        )
        st.caption(f"Completed GDV: {metrics['full_completed_gdvalue_formatted']}")

    with col_f4:
        st.metric(
            "Market Saleable Rate",
            f"₹{metrics['market_rate_per_sqft']:,} / sqft",
            help="Prevailing Tier market capital value."
        )
        st.caption(f"Project Category: {structure_type.split('(')[0].strip()}")

    # BoQ Steel and Cement Metrics Section
    st.markdown("---")
    st.markdown("#### 🔩 Bill of Quantities (BoQ) Material Utilization Metrics")

    col_mat1, col_mat2, col_mat3, col_mat4 = st.columns(4)

    with col_mat1:
        st.metric("Total Steel Rebar", f"{metrics['total_steel_mt']:,} MT")
        st.caption("Fe500D / Fe550 TMT Rebar (IS 1786)")

    with col_mat2:
        st.metric("Steel Consumed to Date", f"{metrics['consumed_steel_mt']:,} MT")
        pct_steel = int((metrics['consumed_steel_mt'] / max(1, metrics['total_steel_mt'])) * 100)
        st.caption(f"Consumption: {pct_steel}% of Total")

    with col_mat3:
        st.metric("Total Cement Required", f"{metrics['total_cement_bags']:,} Bags")
        st.caption(f"≈ {metrics['total_cement_mt']:,} Metric Tonnes (OPC 53)")

    with col_mat4:
        st.metric("Cement Consumed to Date", f"{metrics['consumed_cement_bags']:,} Bags")
        st.caption(f"≈ {metrics['consumed_cement_mt']:,} Metric Tonnes")

    # Interactive Visualizations: Budget Breakdown Donut & CapEx S-Curve
    col_chart1, col_chart2 = st.columns([1.1, 1])

    with col_chart1:
        st.markdown("##### 🍩 Discipline Budget Distribution")
        breakdown = metrics["discipline_breakdown"]
        labels = list(breakdown.keys())
        values = list(breakdown.values())

        fig_donut = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.48,
            textinfo='label+percent',
            marker=dict(colors=['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899']),
            showlegend=False
        )])
        fig_donut.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            height=280,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#94A3B8")
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_chart2:
        st.markdown("##### 📈 CapEx Deployed vs Remaining Contingency")
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            name='CapEx Incurred',
            x=['Financial Status'],
            y=[metrics['capex_incurred_inr'] / 10_000_000],
            marker_color='#F59E0B',
            text=[f"{metrics['capex_incurred_formatted']}"],
            textposition='auto',
        ))
        fig_bar.add_trace(go.Bar(
            name='Remaining Budget',
            x=['Financial Status'],
            y=[remaining_budget / 10_000_000],
            marker_color='#334155',
            text=[f"{format_inr(remaining_budget)}"],
            textposition='auto',
        ))
        fig_bar.update_layout(
            barmode='stack',
            height=280,
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#94A3B8"),
            yaxis=dict(title="₹ Crores", gridcolor="rgba(148, 163, 184, 0.1)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # --------------------------------------------------------------------------
    # Conceptual 3D Architectural Rendering Integration (Pollinations AI)
    # --------------------------------------------------------------------------
    st.markdown("---")
    st.markdown("### 🎨 Conceptual 3D Architectural Rendering Integration")
    st.markdown(
        "Automated generative AI rendering powered by **Pollinations AI** prompt engineering. "
        "Dynamically transforms structural geometry, milestone completion, and regional architectural style into a conceptual render."
    )

    col_render_cfg, col_render_view = st.columns([1, 1.4])

    with col_render_cfg:
        arch_style = st.selectbox(
            "Architectural Philosophy / Aesthetic",
            [
                "Modern Sustainable Biomimetic & Glass",
                "Brutalist Exposed Concrete & Tropical Greenery",
                "High-Tech Neo-Futuristic Parametric",
                "Classical Indo-Contemporary Luxury",
                "Minimalist Scandinavian Industrial"
            ],
            key="tab3_arch_style"
        )

        prompt_text, render_url = ConstructionValuationEngine.generate_pollinations_rendering_prompt(
            structure_type=structure_type,
            location_tier=location_tier,
            completion_pct=completion_pct,
            architectural_style=arch_style
        )

        st.markdown("**Engineered Generative Prompt:**")
        st.text_area("Prompt Inspector", value=prompt_text, height=120, key="tab3_prompt_box", disabled=True)

        refresh_render = st.button("🔄 Regenerate 3D Visual Concept", key="tab3_refresh_render")

    with col_render_view:
        st.markdown("##### 🏛️ Conceptual Architectural Preview")
        try:
            st.image(
                render_url,
                caption=f"Conceptual 3D Visualization: {structure_type} ({completion_pct}% Stage)",
                use_container_width=True
            )
            st.markdown(f"[🔗 Open Full-Resolution 1024x640 Render]({render_url})", unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Unable to preview image directly: {e}. You can access the render URL: {render_url}")
