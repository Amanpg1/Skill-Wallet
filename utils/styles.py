"""
Custom CSS styling and design system for Multimodal Construction Intelligence Platform.
Engineered for clean, modern aesthetics with dark/light mode resilience.
"""

def get_custom_css() -> str:
    return """
    <style>
    /* Google Fonts import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    code, pre, .mono-font {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
        max-width: 1300px;
    }

    /* Platform Hero Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #334155 100%);
        border-radius: 14px;
        padding: 1.6rem 2rem;
        margin-bottom: 1.8rem;
        border: 1px solid rgba(245, 158, 11, 0.3);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.25), 0 8px 10px -6px rgba(0, 0, 0, 0.2);
        color: white;
        position: relative;
        overflow: hidden;
    }

    .hero-banner::after {
        content: "";
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        width: 140px;
        background: repeating-linear-gradient(
            -45deg,
            rgba(245, 158, 11, 0.12),
            rgba(245, 158, 11, 0.12) 12px,
            transparent 12px,
            transparent 24px
        );
        pointer-events: none;
    }

    .hero-title {
        font-size: 1.75rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }

    .hero-subtitle {
        color: #94A3B8;
        font-size: 0.95rem;
        margin-top: 0.4rem;
        margin-bottom: 0;
        font-weight: 400;
    }

    .hero-badges {
        display: flex;
        gap: 0.5rem;
        margin-top: 0.9rem;
        flex-wrap: wrap;
    }

    .badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.22rem 0.65rem;
        border-radius: 9999px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        background: rgba(255, 255, 255, 0.08);
        color: #E2E8F0;
        border: 1px solid rgba(255, 255, 255, 0.12);
    }

    .badge-pill.amber {
        background: rgba(245, 158, 11, 0.15);
        color: #FCD34D;
        border-color: rgba(245, 158, 11, 0.35);
    }

    .badge-pill.green {
        background: rgba(16, 185, 129, 0.15);
        color: #6EE7B7;
        border-color: rgba(16, 185, 129, 0.35);
    }

    .badge-pill.blue {
        background: rgba(59, 130, 246, 0.15);
        color: #93C5FD;
        border-color: rgba(59, 130, 246, 0.35);
    }

    /* Metric & Insight Cards */
    .eng-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 12px;
        padding: 1.25rem 1.4rem;
        margin-bottom: 1.1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .eng-card:hover {
        border-color: rgba(245, 158, 11, 0.35);
        box-shadow: 0 8px 15px -3px rgba(0, 0, 0, 0.1);
    }

    .eng-card-title {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94A3B8;
        margin-bottom: 0.4rem;
    }

    .eng-card-value {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #0F172A;
    }

    @media (prefers-color-scheme: dark) {
        .eng-card-value {
            color: #F8FAFC;
        }
        .eng-card {
            background: #1E293B;
            border-color: #334155;
        }
    }

    /* Status Pills */
    .status-badge {
        padding: 0.35rem 0.8rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.82rem;
        display: inline-block;
        letter-spacing: 0.02em;
    }

    .status-compliant {
        background: #DCFCE7;
        color: #15803D;
        border: 1px solid #86EFAC;
    }

    .status-warning {
        background: #FEF3C7;
        color: #B45309;
        border: 1px solid #FCD34D;
    }

    .status-critical {
        background: #FEE2E2;
        color: #B91C1C;
        border: 1px solid #FCA5A5;
    }

    /* Severity badges */
    .severity-badge {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        padding: 0.2rem 0.55rem;
        border-radius: 4px;
        display: inline-block;
    }

    .sev-critical {
        background: #EF4444;
        color: white;
    }

    .sev-high {
        background: #F97316;
        color: white;
    }

    .sev-medium {
        background: #F59E0B;
        color: #1E293B;
    }

    .sev-low {
        background: #10B981;
        color: white;
    }

    /* Weather Warning Banners */
    .weather-banner {
        border-radius: 10px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 1.2rem;
        border-left: 5px solid;
    }

    .weather-wind {
        background: rgba(239, 68, 68, 0.08);
        border-left-color: #EF4444;
        border-top: 1px solid rgba(239, 68, 68, 0.2);
        border-right: 1px solid rgba(239, 68, 68, 0.2);
        border-bottom: 1px solid rgba(239, 68, 68, 0.2);
    }

    .weather-rain {
        background: rgba(59, 130, 246, 0.08);
        border-left-color: #3B82F6;
        border-top: 1px solid rgba(59, 130, 246, 0.2);
        border-right: 1px solid rgba(59, 130, 246, 0.2);
        border-bottom: 1px solid rgba(59, 130, 246, 0.2);
    }

    .weather-heat {
        background: rgba(245, 158, 11, 0.08);
        border-left-color: #F59E0B;
        border-top: 1px solid rgba(245, 158, 11, 0.2);
        border-right: 1px solid rgba(245, 158, 11, 0.2);
        border-bottom: 1px solid rgba(245, 158, 11, 0.2);
    }

    .weather-normal {
        background: rgba(16, 185, 129, 0.08);
        border-left-color: #10B981;
        border-top: 1px solid rgba(16, 185, 129, 0.2);
        border-right: 1px solid rgba(16, 185, 129, 0.2);
        border-bottom: 1px solid rgba(16, 185, 129, 0.2);
    }

    /* Checklist Item Styling */
    .checklist-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.6rem 0.8rem;
        background: rgba(255, 255, 255, 0.02);
        border-bottom: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 6px;
        margin-bottom: 0.35rem;
    }

    .checklist-name {
        font-weight: 500;
        font-size: 0.88rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Engineering Citation Box */
    .citation-box {
        font-size: 0.76rem;
        background: rgba(51, 65, 85, 0.06);
        border: 1px dashed rgba(100, 116, 139, 0.35);
        border-radius: 6px;
        padding: 0.6rem 0.9rem;
        margin-top: 0.6rem;
        color: #64748B;
    }

    /* Button Styling refinement */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.18s ease;
    }

    /* Sidebar Clean Styling */
    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(148, 163, 184, 0.15);
    }
    </style>
    """

def render_hero_banner():
    return """
    <div class="hero-banner">
        <h1 class="hero-title">
            <span>🏗️</span> Multimodal Construction Intelligence Platform
        </h1>
        <p class="hero-subtitle">
            Enterprise Site Safety, Structural Forensics, Real Estate Valuation & Weather-Aware Autonomous Advisory
        </p>
        <div class="hero-badges">
            <span class="badge-pill amber">Capstone Project 1</span>
            <span class="badge-pill green">OSHA 1926 & IS 456 Compliant</span>
            <span class="badge-pill blue">Gemini 2.5 Multi-Modal Vision</span>
            <span class="badge-pill">NBC 2016 Civil Standards</span>
        </div>
    </div>
    """
