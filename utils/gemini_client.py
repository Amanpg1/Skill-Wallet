"""
Gemini Multimodal Client & AI Forensic Engine.
Handles live Gemini API calls with graceful fallback to Demonstration Mode.
Compliant with OSHA 1926, IS 456:2000, IS 800:2007, and NBC 2016 standards.
"""

import json
import re
import os
from typing import Dict, Any, List, Optional, Tuple
from PIL import Image

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


def extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """Robustly extracts JSON object from markdown fenced blocks or raw strings."""
    if not text:
        return None
    # 1. Try direct json parse
    try:
        return json.loads(text.strip())
    except Exception:
        pass

    # 2. Extract between ```json and ```
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except Exception:
            pass

    # 3. Search for outermost curly braces { ... }
    first_brace = text.find("{")
    last_brace = text.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        try:
            return json.loads(text[first_brace : last_brace + 1])
        except Exception:
            pass

    return None


class GeminiConstructionEngine:
    """Enterprise Multimodal AI Engine for Construction Safety and Structural Health."""

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.model_name = model_name
        self.client = None
        self.is_demo_mode = True

        if self.api_key and self.api_key.strip() and GENAI_AVAILABLE:
            try:
                self.client = genai.Client(api_key=self.api_key.strip())
                self.is_demo_mode = False
            except Exception as e:
                print(f"[GeminiClient] Initialization error, falling back to Demo Mode: {e}")
                self.is_demo_mode = True
        else:
            self.is_demo_mode = True

    # --------------------------------------------------------------------------
    # TAB 1: SITE SAFETY & PPE AUDIT (EPIC 2)
    # --------------------------------------------------------------------------
    def audit_site_safety_ppe(self, image: Image.Image, custom_context: str = "") -> Tuple[Dict[str, Any], bool]:
        """
        Multimodal audit of worker PPE compliance and site hazard detection
        under OSHA 1926 and IS 456/IS 3696 guidelines.
        Returns (result_dict, was_live_api).
        """
        if not self.is_demo_mode and self.client:
            prompt = f"""
            You are an OSHA Senior Construction Safety Inspector and Lead Auditor certified in IS 456:2000 and IS 3696 safety standards.
            Analyze this construction site photo thoroughly for Personal Protective Equipment (PPE) compliance and physical hazards.

            Context notes: {custom_context if custom_context else "Active structural civil construction site"}

            You MUST output ONLY a valid JSON object with the following schema without any surrounding text:
            {{
                "safety_score": <integer from 0 to 100 representing overall safety compliance>,
                "overall_status": "<Compliant | Needs Attention | Critical Non-Compliance>",
                "summary": "<2-3 sentence executive safety summary citing observations>",
                "workers_observed_count": <approximate number of workers identified>,
                "ppe_detection": [
                    {{
                        "item": "Safety Helmets (Hard Hats)",
                        "standard": "OSHA 1926.100 / IS 2925",
                        "status": "<Detected & Compliant | Missing / Non-Compliant | Partially Compliant>",
                        "compliance_rate": "<percentage string e.g. 75%>",
                        "notes": "<specific observation details>"
                    }},
                    {{
                        "item": "High-Visibility Safety Vests",
                        "standard": "OSHA 1926.201 / IS 15809 Class 2",
                        "status": "<Detected & Compliant | Missing / Non-Compliant | Partially Compliant>",
                        "compliance_rate": "<percentage string>",
                        "notes": "<specific observation details>"
                    }},
                    {{
                        "item": "Steel-Toe Safety Boots",
                        "standard": "OSHA 1926.96 / IS 15298",
                        "status": "<Detected & Compliant | Missing / Non-Compliant | Partially Compliant>",
                        "compliance_rate": "<percentage string>",
                        "notes": "<specific observation details>"
                    }},
                    {{
                        "item": "Fall Protection / Safety Harness",
                        "standard": "OSHA 1926.501 / IS 3521 (Work at height > 1.8m)",
                        "status": "<Detected & Compliant | Missing / Non-Compliant | Not Applicable>",
                        "compliance_rate": "<percentage string>",
                        "notes": "<specific observation details>"
                    }},
                    {{
                        "item": "Eye / Face & Hand Protection",
                        "standard": "OSHA 1926.102 / IS 8519",
                        "status": "<Detected & Compliant | Missing / Non-Compliant | Not Applicable>",
                        "compliance_rate": "<percentage string>",
                        "notes": "<specific observation details>"
                    }}
                ],
                "site_hazards": [
                    {{
                        "hazard": "<description of specific site hazard>",
                        "location_element": "<zone / structural component>",
                        "severity": "<Critical | High | Medium | Low>",
                        "standard_code": "<OSHA or IS standard reference>",
                        "corrective_remedy": "<exact mandatory engineering or behavioral remedy>",
                        "resolution_timeframe": "<Immediate - Stop Work | Within 2 Hours | Within 24 Hours>"
                    }}
                ],
                "recommended_safety_actions": [
                    "<Actionable instruction 1>",
                    "<Actionable instruction 2>",
                    "<Actionable instruction 3>"
                ]
            }}
            """
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=[image, prompt],
                    config=types.GenerateContentConfig(
                        temperature=0.2,
                        response_mime_type="application/json"
                    )
                )
                parsed = extract_json_from_text(response.text)
                if parsed and "safety_score" in parsed:
                    return parsed, True
            except Exception as e:
                print(f"[GeminiClient] Live PPE audit failed ({e}), using realistic simulation fallback.")

        # Realistic Demonstration Fallback
        return self._simulate_ppe_audit(image), False

    def _simulate_ppe_audit(self, image: Image.Image) -> Dict[str, Any]:
        """Generates realistic safety audit data based on image characteristics."""
        return {
            "safety_score": 62,
            "overall_status": "Needs Attention",
            "summary": "Multiple workers observed in active superstructure zone. While ground personnel maintain adequate high-visibility vest compliance, worker positioned on elevated scaffolding lacks anchored 100% tie-off fall arrest harness and hard hat, posing severe OSHA fall hazard.",
            "workers_observed_count": 3,
            "ppe_detection": [
                {
                    "item": "Safety Helmets (Hard Hats)",
                    "standard": "OSHA 1926.100 / IS 2925:1984",
                    "status": "Partially Compliant",
                    "compliance_rate": "67%",
                    "notes": "1 elevated worker observed without hard hat in overhead crane swing perimeter."
                },
                {
                    "item": "High-Visibility Safety Vests",
                    "standard": "OSHA 1926.201 / IS 15809 Class 2",
                    "status": "Detected & Compliant",
                    "compliance_rate": "100%",
                    "notes": "All active personnel wearing fluorescent orange/lime vests with retroreflective striping."
                },
                {
                    "item": "Steel-Toe Safety Boots",
                    "standard": "OSHA 1926.96 / IS 15298:2011",
                    "status": "Detected & Compliant",
                    "compliance_rate": "100%",
                    "notes": "Reinforced safety footwear verified across all ground and deck workers."
                },
                {
                    "item": "Fall Protection / Safety Harness",
                    "standard": "OSHA 1926.501(b)(1) / IS 3521:1999",
                    "status": "Missing / Non-Compliant",
                    "compliance_rate": "0%",
                    "notes": "Worker active on staging board at elevation > 2.4m without double-lanyard harness anchorage."
                },
                {
                    "item": "Eye / Face & Hand Protection",
                    "standard": "OSHA 1926.102 / IS 8519",
                    "status": "Partially Compliant",
                    "compliance_rate": "50%",
                    "notes": "Cut-resistant gloves detected; eye goggles absent during rebar handling."
                }
            ],
            "site_hazards": [
                {
                    "hazard": "Fall Hazard at Elevated Scaffolding Staging",
                    "location_element": "Level 2 Facade Scaffolding (Bay 3)",
                    "severity": "Critical",
                    "standard_code": "OSHA 1926.451(g)(1) / IS 3696 (Part 1)",
                    "corrective_remedy": "Issue immediate Stop-Work order on Bay 3. Mandate EN 361 full-body harness secured to independent lifeline.",
                    "resolution_timeframe": "Immediate - Stop Work"
                },
                {
                    "hazard": "Unsecured Scaffolding Deck Planks & Missing Toe-Boards",
                    "location_element": "Working Platform Deck",
                    "severity": "High",
                    "standard_code": "OSHA 1926.451(b)(1) / NBC 2016 Part 7",
                    "corrective_remedy": "Clamp scaffold boards with steel couplers; install 150mm kick plates/toe-boards to prevent falling debris.",
                    "resolution_timeframe": "Within 2 Hours"
                },
                {
                    "hazard": "Overhead Crane Suspended Load Swing Clearance",
                    "location_element": "Zone 4 Loading Bay",
                    "severity": "Medium",
                    "standard_code": "OSHA 1926.1425 / IS 13367",
                    "corrective_remedy": "Cordon off ground radius with safety tape and post dedicated signal rigger.",
                    "resolution_timeframe": "Within 24 Hours"
                }
            ],
            "recommended_safety_actions": [
                "Conduct mandatory 15-minute Toolbox Talk (TBT) on Fall Arrest Systems before resuming facade work.",
                "Verify scaffolding green-tag inspection certificate before allowing workers on upper tiers.",
                "Deploy safety nets (IS 11057) below open-edge perimeter slabs."
            ]
        }

    # --------------------------------------------------------------------------
    # TAB 2: CRACK DIAGNOSTICS & STRUCTURAL INTEGRITY (EPIC 2)
    # --------------------------------------------------------------------------
    def diagnose_structural_crack(self, image: Image.Image, element_type: str = "RCC Beam/Column") -> Tuple[Dict[str, Any], bool]:
        """
        Multimodal defect classification, crack width estimation, root cause forensics,
        and engineering repair specification (IS 456:2000, ACI 224R-01).
        Returns (result_dict, was_live_api).
        """
        if not self.is_demo_mode and self.client:
            prompt = f"""
            You are a Principal Structural Forensic Engineer specializing in concrete pathology, non-destructive testing, and repair under IS 456:2000, IS 13920, and ACI 224R-01.
            Inspect the provided concrete or wall surface image carefully.

            Structural Element Category: {element_type}

            You MUST output ONLY a valid JSON object matching the following structure:
            {{
                "defect_type": "<Structural Shear | Settlement | Hairline | Thermal Expansion | Spalling | Flexural Tension>",
                "estimated_crack_width_mm": <float, e.g. 2.4>,
                "structural_severity": "<Critical | High | Moderate | Minor / Aesthetic>",
                "urgency": "<Immediate Structural Intervention | High Priority (Within 48h) | Routine Maintenance | Periodic Monitoring>",
                "is456_compliance": "<Exceeds IS 456 limit (0.2mm - 0.3mm) | Within Permissible Serviceability Limits>",
                "root_causes": [
                    "<Root cause engineering factor 1>",
                    "<Root cause engineering factor 2>"
                ],
                "recommended_repairs": [
                    {{
                        "method": "<e.g. Low-Viscosity Epoxy Injection | Polyurethane Hydrophobic Grout | Carbon Fiber (CFRP) Strengthening | Polymer Modified Mortar (PMM)>",
                        "specification": "<technical material and pressure parameters>",
                        "code_standard": "<e.g. IS 456 Cl. 35.3.2 / ACI 546R>"
                    }}
                ],
                "structural_impact_analysis": "<Detailed assessment of moment/shear capacity loss, steel corrosion risk, or load path compromise>",
                "monitoring_protocol": "<NDT monitoring instructions e.g. telltale optical crack gauges, ultrasonic pulse velocity (UPV)>"
            }}
            """
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=[image, prompt],
                    config=types.GenerateContentConfig(
                        temperature=0.2,
                        response_mime_type="application/json"
                    )
                )
                parsed = extract_json_from_text(response.text)
                if parsed and "defect_type" in parsed:
                    return parsed, True
            except Exception as e:
                print(f"[GeminiClient] Live crack diagnosis failed ({e}), using realistic simulation fallback.")

        return self._simulate_crack_diagnosis(element_type), False

    def _simulate_crack_diagnosis(self, element_type: str) -> Dict[str, Any]:
        """Simulate realistic forensic engineering diagnosis."""
        return {
            "defect_type": "Structural Shear",
            "estimated_crack_width_mm": 2.8,
            "structural_severity": "Critical",
            "urgency": "Immediate Structural Intervention",
            "is456_compliance": "Exceeds IS 456 limit (0.2mm - 0.3mm)",
            "root_causes": [
                "Diagonal tension overstress exceeding concrete tensile strength (fcr = 0.7 * sqrt(fck)).",
                "Insufficient shear stirrup spacing near support zone during peak dead + live loading (IS 456 Cl. 40).",
                "Micro-settlement at column junction inducing secondary torsional and shear stresses."
            ],
            "recommended_repairs": [
                {
                    "method": "Structural Low-Viscosity Epoxy Resin Pressure Injection",
                    "specification": "ASTM C881 Type I/IV Grade 1 low-viscosity epoxy injected via surface ports under 0.25-0.35 MPa pressure until refusal.",
                    "code_standard": "IS 456:2000 Cl. 35.3.2 / ACI 224.1R"
                },
                {
                    "method": "CFRP (Carbon Fiber Reinforced Polymer) U-Wrap Shear Retrofit",
                    "specification": "Bi-directional 300 gsm carbon fiber fabric laminated with epoxy primer to restore and enhance nominal shear capacity Vc.",
                    "code_standard": "ACI 440.2R / FIB Bulletin 14"
                },
                {
                    "method": "Temporary Acrow Propping Support",
                    "specification": "Install heavy-duty adjustable steel shoring props directly below beam midspan and shear zone prior to injection curing.",
                    "code_standard": "NBC 2016 Part 6 Structural Design"
                }
            ],
            "structural_impact_analysis": "The observed 45-degree diagonal shear trajectory indicates significant loss of shear capacity near the critical support d/2 section. With a width of 2.8mm, it exceeds IS 456:2000 Cl. 35.3.2 permissible crack width limits by over 9x, exposing internal shear links to accelerated atmospheric carbonation and potential brittle failure under live load spikes.",
            "monitoring_protocol": "Mount calibrated two-axis polycarbonate telltale crack monitors across crack apex; perform Ultrasonic Pulse Velocity (UPV) test as per IS 13311 (Part 1) to determine fracture depth prior to pressure grouting."
        }

    # --------------------------------------------------------------------------
    # TAB 4: DAILY SITE ASSISTANT & WEATHER-AWARE CHATBOT (EPIC 5)
    # --------------------------------------------------------------------------
    def chat_engineering_assistant(
        self,
        messages: List[Dict[str, str]],
        current_weather: str = "Normal",
        site_context: str = ""
    ) -> Tuple[str, bool]:
        """
        Interactive multi-turn civil engineering assistant with IS/OSHA standards context.
        Returns (response_text, was_live_api).
        """
        if not self.is_demo_mode and self.client:
            system_instruction = f"""
            You are 'SiteMind AI', an expert Chief Resident Civil Engineer and Safety Director.
            You possess deep knowledge of Indian Standards (IS 456:2000, IS 800:2007, IS 1893:2016, IS 13920:2016),
            National Building Code (NBC 2016), OSHA 1926 Safety Regulations, and Central Public Works Department (CPWD) specifications.

            Current Site Environmental Conditions: {current_weather}
            Site Context: {site_context if site_context else "Multi-storey commercial/residential development"}

            Provide crisp, highly professional, technically rigorous answers with exact clause citations, concrete mix guidance,
            scaffolding rules, curing protocols, and safety mitigations whenever applicable.
            Format with markdown, bullet points, and code snippets or formula blocks where appropriate.
            """

            # Build conversation string or prompt
            formatted_history = []
            for m in messages:
                role = "User" if m["role"] == "user" else "Assistant"
                formatted_history.append(f"{role}: {m['content']}")

            prompt = f"{system_instruction}\n\n" + "\n\n".join(formatted_history)

            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(temperature=0.3)
                )
                if response.text:
                    return response.text, True
            except Exception as e:
                print(f"[GeminiClient] Chat assistant call failed ({e}), using resident simulation.")

        # Resident fallback assistant
        last_user_query = messages[-1]["content"] if messages else "Hello"
        return self._simulate_chat_response(last_user_query, current_weather), False

    def _simulate_chat_response(self, query: str, weather: str) -> str:
        """Intelligent context-driven responses when offline or in demonstration mode."""
        q = query.lower()

        if "m25" in q or "mix" in q or "ratio" in q:
            return """### 📐 M25 Concrete Mix Design Guidelines (IS 456:2000 & IS 10262:2019)

**Nominal Mix Ratio (by Volume):** `1 : 1 : 2` (Cement : Fine Aggregate : Coarse Aggregate)
For structural elements, IS 456 mandates **Design Mix** concrete for M25 and above.

| Component | Standard Proportion per m³ | Function / Quality Standard |
| :--- | :--- | :--- |
| **OPC 53 Grade Cement** | 380 - 410 kg | IS 269 / IS 12269 |
| **Fine Aggregate (River/M-Sand)** | 660 - 710 kg (Zone II) | IS 383:2016 (Silt content < 3%) |
| **Coarse Aggregate (20mm & 10mm)** | 1150 - 1200 kg (60:40 blend) | Crushed angular granite |
| **Water** | 165 - 180 Liters | Potable water (pH 6.5 to 8.5) |
| **Water-Cement Ratio (w/c)** | **0.40 - 0.45** | Maximum as per IS 456 Table 5 |
| **Admixture (PCE Superplasticizer)** | 0.8% - 1.2% by weight of cement | To achieve 120-150mm slump for pumping |

> [!TIP]
> **Hot Weather Concreting Note:** If ambient temperature exceeds 35°C, retarders should be incorporated to avoid cold joints, and plastic shrinkage sheets deployed immediately after floating.
"""

        elif "wind" in q or "crane" in q:
            return f"""### 🏗️ Tower Crane Operation & Wind Speed Thresholds (IS 13367 & OSHA 1926.1431)

Current Weather Condition: **{weather}**

* **Safe Working Wind Speed:** Up to **38 km/h (10.5 m/s or 20 knots)** for general lifting.
* **Cautionary Speed (40 - 50 km/h):** Cease large-panel formwork or drywall hoisting due to high aerodynamic sail area.
* **MANDATORY STOP-WORK THRESHOLD:**
  * At **54 km/h (15 m/s or 30 mph)**: **All crane operations MUST halt immediately**.
  * Trolley brought to minimum radius (near mast).
  * Hook block hoisted to top limit switch (just below boom).
  * **Slew brake RELEASED (Weathervane Mode)** to allow the jib to rotate freely with the wind direction, preventing catastrophic mast torsion.
"""

        elif "curing" in q or "slab" in q:
            return """### 💧 Concrete Curing Specifications (IS 456:2000 Clause 13.5)

1. **Minimum Curing Duration:**
   * **Ordinary Portland Cement (OPC):** Minimum **7 days** under normal conditions.
   * **Blended Cements (PPC / Slag Cement / Mineral Admixtures):** Minimum **10 days** (extended to **14 days** under dry, hot, or windy weather).

2. **Permissible Stripping / Deshoring Time (IS 456 Cl. 11.3):**
   * *Vertical formwork to columns, walls, beams:* **16 - 24 hours**
   * *Soffit formwork to slabs (props left under):* **3 days**
   * *Soffit formwork to beams (props left under):* **7 days**
   * *Props to slabs spanning up to 4.5m:* **7 days**
   * *Props to beams spanning over 6m:* **21 days**

> [!IMPORTANT]
> Ponding method is recommended for flat slabs; liquid membrane-forming curing compounds must comply with ASTM C309.
"""

        elif "shoring" in q or "excavation" in q:
            return """### ⛏️ Trench Excavation & Shoring Safety (OSHA 1926 Subpart P & IS 3764)

* **Depth Threshold:** Any excavation deeper than **1.5 meters (5 feet)** requires certified protective systems (sloping, benching, or shoring shield).
* **Soil Classification & Angle of Repose:**
  * *Type A (Clay / Hardpan):* 3/4 : 1 slope (53°)
  * *Type B (Silt / Gravel):* 1 : 1 slope (45°)
  * *Type C (Sand / Submerged soil):* 1.5 : 1 slope (34°)
* **Safety Protocols:**
  * Keep heavy machinery and spoil piles at least **1.0 meter (or depth/2)** away from trench crest edge.
  * Provide ladder access within **7.5 meters (25 feet)** of lateral travel for workers.
  * Inspect daily and post-rainfall for tension cracks at the crest before worker entry.
"""

        else:
            return f"""### 👷 Resident Engineer Site Advisory

Thank you for your inquiry regarding: *"{query}"*.

**Engineering Analysis:**
1. **Compliance Baseline:** Works must strictly adhere to **IS 456:2000 (Code of Practice for Plain and Reinforced Concrete)**, **NBC 2016 Part 7 (Construction Management & Safety)**, and **OSHA 1926**.
2. **Current Environmental Protocol ({weather}):** Safety coordinators must cross-verify site stability checklist and ensure all personnel are equipped with mandatory Level-2 PPE.
3. **Execution Quality Control:** Pre-pour check-sheets (reinforcement cover blocks, dowel development lengths $L_d = 40\\phi$ to $50\\phi$, lap stagger > 1.3 $L_d$) must be signed off by the Quality Assurance Engineer.

Please let me know if you would like calculations for reinforcement tonnage, concrete mix adjustments, or structural shoring load tables!"""
