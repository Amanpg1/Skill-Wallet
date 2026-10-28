"""
Verification test script for Multimodal Construction Intelligence Platform.
"""
import sys
import os

# Ensure UTF-8 output on Windows terminal
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

from utils.gemini_client import GeminiConstructionEngine
from utils.sample_images import (
    generate_safety_sample_violation,
    generate_safety_sample_compliant,
    generate_crack_structural_shear,
    generate_crack_spalling_rebar,
    generate_crack_hairline_plaster
)
from utils.valuation_calculator import ConstructionValuationEngine

def test_all():
    print("[1/4] Testing Sample Images Generation...")
    img_viol = generate_safety_sample_violation()
    img_comp = generate_safety_sample_compliant()
    img_crack = generate_crack_structural_shear()
    img_spall = generate_crack_spalling_rebar()
    img_hair = generate_crack_hairline_plaster()
    assert img_viol.size == (800, 600)
    assert img_crack.size == (750, 500)
    print(" -> All 5 sample images generated successfully!")

    print("[2/4] Testing Gemini Client Simulation Engine...")
    engine = GeminiConstructionEngine(api_key="", model_name="gemini-2.5-flash")
    assert engine.is_demo_mode is True

    audit, was_live = engine.audit_site_safety_ppe(img_viol)
    assert "safety_score" in audit
    assert "ppe_detection" in audit
    assert len(audit["site_hazards"]) > 0
    print(f" -> Safety Audit: Score = {audit['safety_score']}, Status = {audit['overall_status']}")

    diag, was_live = engine.diagnose_structural_crack(img_crack)
    assert "defect_type" in diag
    assert "estimated_crack_width_mm" in diag
    assert len(diag["recommended_repairs"]) > 0
    print(f" -> Crack Diagnostics: Defect = {diag['defect_type']}, Width = {diag['estimated_crack_width_mm']}mm")

    chat_reply, was_live = engine.chat_engineering_assistant(
        [{"role": "user", "content": "Calculate M25 concrete mix ratio"}],
        current_weather="High Wind (>40 km/h)"
    )
    assert len(chat_reply) > 50
    print(" -> Chat Engine: Responded successfully!")

    print("[3/4] Testing Valuation & BoQ Engine...")
    val = ConstructionValuationEngine.calculate_project_metrics(
        structure_type="Residential High-Rise (G+24)",
        built_up_sqft=100000,
        location_tier="Tier 1 (Mumbai, Bengaluru, Delhi NCR)",
        completion_pct=50
    )
    assert val["total_budget_inr"] == 320000000
    assert val["capex_incurred_inr"] == 160000000
    assert val["total_steel_mt"] == 480.0
    assert val["consumed_steel_mt"] == 240.0
    print(f" -> Valuation: Budget = {val['total_budget_formatted']}, CapEx = {val['capex_incurred_formatted']}, Steel = {val['total_steel_mt']} MT")

    prompt_text, url = ConstructionValuationEngine.generate_pollinations_rendering_prompt(
        "Residential High-Rise (G+24)",
        "Tier 1 (Mumbai, Bengaluru, Delhi NCR)",
        50
    )
    assert "pollinations.ai" in url
    print(" -> Pollinations AI URL generated successfully!")

    print("\n[4/4] ALL VERIFICATION TESTS PASSED 100%!")

if __name__ == "__main__":
    test_all()
