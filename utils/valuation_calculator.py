"""
Construction Economics, BoQ Material Forensics, and Real Estate Valuation Engine.
Calculates Capital Expenditure (CapEx), Bill of Quantities (BoQ) for Steel & Cement,
and Real Estate Market Valuations for Tier 1/2/3 Indian urban zones.
"""

from typing import Dict, Any, Tuple

def format_inr(amount_in_rupees: float) -> str:
    """Format currency in Indian Lakhs and Crores."""
    if amount_in_rupees >= 10_000_000:
        crores = amount_in_rupees / 10_000_000
        return f"₹{crores:,.2f} Cr"
    elif amount_in_rupees >= 100_000:
        lakhs = amount_in_rupees / 100_000
        return f"₹{lakhs:,.2f} Lakhs"
    else:
        return f"₹{amount_in_rupees:,.0f}"

class ConstructionValuationEngine:
    """Calculates project budgets, CapEx, BoQ materials, and market valuations."""

    STRUCTURE_BENCHMARKS = {
        "Residential High-Rise (G+24)": {
            "steel_kg_per_sqft": 4.8,      # IS 456 ductile detailing
            "cement_bags_per_sqft": 0.43,   # 50kg bags
            "tier_costs": {
                "Tier 1 (Mumbai, Bengaluru, Delhi NCR)": {"base_const_rate": 3200, "market_sale_rate": 14500},
                "Tier 2 (Pune, Hyderabad, Ahmedabad, Chennai)": {"base_const_rate": 2450, "market_sale_rate": 7800},
                "Tier 3 (Emerging Hubs, Jaipur, Indore, Kochi)": {"base_const_rate": 1850, "market_sale_rate": 4500}
            },
            "category": "High-Density Residential"
        },
        "Commercial IT Park & Office Tower": {
            "steel_kg_per_sqft": 5.6,
            "cement_bags_per_sqft": 0.46,
            "tier_costs": {
                "Tier 1 (Mumbai, Bengaluru, Delhi NCR)": {"base_const_rate": 3750, "market_sale_rate": 18500},
                "Tier 2 (Pune, Hyderabad, Ahmedabad, Chennai)": {"base_const_rate": 2850, "market_sale_rate": 9800},
                "Tier 3 (Emerging Hubs, Jaipur, Indore, Kochi)": {"base_const_rate": 2100, "market_sale_rate": 5500}
            },
            "category": "Grade-A Commercial"
        },
        "Industrial Logistics & PEB Warehouse": {
            "steel_kg_per_sqft": 6.8,      # High structural steel portals
            "cement_bags_per_sqft": 0.32,   # Heavy duty flooring
            "tier_costs": {
                "Tier 1 (Mumbai, Bengaluru, Delhi NCR)": {"base_const_rate": 2100, "market_sale_rate": 6500},
                "Tier 2 (Pune, Hyderabad, Ahmedabad, Chennai)": {"base_const_rate": 1650, "market_sale_rate": 4200},
                "Tier 3 (Emerging Hubs, Jaipur, Indore, Kochi)": {"base_const_rate": 1300, "market_sale_rate": 2900}
            },
            "category": "Industrial / Logistics"
        },
        "Gated Luxury Villa Community": {
            "steel_kg_per_sqft": 3.9,
            "cement_bags_per_sqft": 0.39,
            "tier_costs": {
                "Tier 1 (Mumbai, Bengaluru, Delhi NCR)": {"base_const_rate": 3900, "market_sale_rate": 16000},
                "Tier 2 (Pune, Hyderabad, Ahmedabad, Chennai)": {"base_const_rate": 2950, "market_sale_rate": 8900},
                "Tier 3 (Emerging Hubs, Jaipur, Indore, Kochi)": {"base_const_rate": 2200, "market_sale_rate": 5200}
            },
            "category": "Low-Rise Luxury"
        },
        "Infrastructure / Flyover & Bridge Section": {
            "steel_kg_per_sqft": 8.2,      # High tensile prestressing + HYSD
            "cement_bags_per_sqft": 0.58,   # High performance M45/M50
            "tier_costs": {
                "Tier 1 (Mumbai, Bengaluru, Delhi NCR)": {"base_const_rate": 4800, "market_sale_rate": 9500},
                "Tier 2 (Pune, Hyderabad, Ahmedabad, Chennai)": {"base_const_rate": 4100, "market_sale_rate": 7800},
                "Tier 3 (Emerging Hubs, Jaipur, Indore, Kochi)": {"base_const_rate": 3500, "market_sale_rate": 6200}
            },
            "category": "Civil Infrastructure"
        }
    }

    @classmethod
    def calculate_project_metrics(
        cls,
        structure_type: str,
        built_up_sqft: float,
        location_tier: str,
        completion_pct: float
    ) -> Dict[str, Any]:
        """Compute full BoQ materials, budgets, CapEx, and asset valuations."""
        benchmark = cls.STRUCTURE_BENCHMARKS.get(
            structure_type,
            cls.STRUCTURE_BENCHMARKS["Residential High-Rise (G+24)"]
        )
        tier_data = benchmark["tier_costs"].get(
            location_tier,
            benchmark["tier_costs"]["Tier 1 (Mumbai, Bengaluru, Delhi NCR)"]
        )

        base_rate = tier_data["base_const_rate"]
        market_rate = tier_data["market_sale_rate"]

        # Budget & Financials
        total_construction_budget = built_up_sqft * base_rate
        capex_incurred = total_construction_budget * (completion_pct / 100.0)

        # Asset market valuation considers land equity value (estimated at 35-45% of completed gross development value)
        # plus the value of physical construction work completed to date
        completed_gdvalue = built_up_sqft * market_rate
        base_land_value = completed_gdvalue * 0.40
        current_work_value = (completed_gdvalue * 0.60) * (completion_pct / 100.0)
        current_market_asset_valuation = base_land_value + current_work_value

        # BoQ Materials
        # Steel
        total_steel_kg = built_up_sqft * benchmark["steel_kg_per_sqft"]
        total_steel_metric_tonnes = total_steel_kg / 1000.0
        consumed_steel_mt = total_steel_metric_tonnes * (completion_pct / 100.0)

        # Cement
        total_cement_bags = int(built_up_sqft * benchmark["cement_bags_per_sqft"])
        total_cement_metric_tonnes = (total_cement_bags * 50) / 1000.0
        consumed_cement_bags = int(total_cement_bags * (completion_pct / 100.0))
        consumed_cement_mt = (consumed_cement_bags * 50) / 1000.0

        # Milestone Stage Detection
        if completion_pct < 15:
            current_stage = "Substructure & Deep Foundation (Piling / Raft)"
            stage_color = "#3B82F6"
        elif completion_pct < 50:
            current_stage = "RCC Superstructure & Slab Casting"
            stage_color = "#F59E0B"
        elif completion_pct < 75:
            current_stage = "Masonry, External Facade & Rough MEP"
            stage_color = "#8B5CF6"
        elif completion_pct < 95:
            current_stage = "Architectural Finishes, Elevators & Commissioning"
            stage_color = "#10B981"
        else:
            current_stage = "Final Inspection, Snagging & Occupancy Handover"
            stage_color = "#059669"

        # Cost Breakdown by Trade
        discipline_breakdown = {
            "Civil Structure & Concrete": total_construction_budget * 0.48,
            "Finishes, Façade & Waterproofing": total_construction_budget * 0.22,
            "MEP, HVAC & Firefighting": total_construction_budget * 0.16,
            "Site Infrastructure & Landscaping": total_construction_budget * 0.08,
            "Statutory, PMC & Contingencies": total_construction_budget * 0.06
        }

        return {
            "total_budget_inr": total_construction_budget,
            "total_budget_formatted": format_inr(total_construction_budget),
            "capex_incurred_inr": capex_incurred,
            "capex_incurred_formatted": format_inr(capex_incurred),
            "current_market_asset_valuation_inr": current_market_asset_valuation,
            "current_market_valuation_formatted": format_inr(current_market_asset_valuation),
            "full_completed_gdvalue_formatted": format_inr(completed_gdvalue),
            "base_rate_per_sqft": base_rate,
            "market_rate_per_sqft": market_rate,
            "total_steel_mt": round(total_steel_metric_tonnes, 1),
            "consumed_steel_mt": round(consumed_steel_mt, 1),
            "total_cement_bags": total_cement_bags,
            "consumed_cement_bags": consumed_cement_bags,
            "total_cement_mt": round(total_cement_metric_tonnes, 1),
            "consumed_cement_mt": round(consumed_cement_mt, 1),
            "current_stage": current_stage,
            "stage_color": stage_color,
            "discipline_breakdown": discipline_breakdown
        }

    @classmethod
    def generate_pollinations_rendering_prompt(
        cls,
        structure_type: str,
        location_tier: str,
        completion_pct: float,
        architectural_style: str = "Modern Sustainable Biomimetic"
    ) -> Tuple[str, str]:
        """
        Synthesizes a hyper-detailed architectural visual prompt and returns the direct
        Pollinations AI image generation URL.
        """
        # Clean city name from tier
        city_ref = location_tier.split("(")[-1].replace(")", "").split(",")[0].strip()

        base_desc = {
            "Residential High-Rise (G+24)": "high-rise residential skyscraper tower with cascading sky gardens, cantilevered balconies, energy-efficient triple glazed curtain walls",
            "Commercial IT Park & Office Tower": "futuristic Class-A commercial headquarters campus with double skin glass facade, solar louvers, atrium water features",
            "Industrial Logistics & PEB Warehouse": "modern automated logistics hub with pre-engineered steel framing, expansive clear-span portal bays, solar roof array",
            "Gated Luxury Villa Community": "contemporary luxury private villa enclave with infinity pools, local sandstone accents, teak pergola sunscreens",
            "Infrastructure / Flyover & Bridge Section": "cable-stayed urban flyover viaduct with post-tensioned segmental concrete box girders, architectural LED night illumination"
        }.get(structure_type, "architectural landmark")

        stage_desc = ""
        if completion_pct < 35:
            stage_desc = "construction in progress with high-tech yellow tower cranes, exposed reinforced concrete formwork, steel rebar cage assemblies"
        elif completion_pct < 85:
            stage_desc = "near-completion architectural view with facade installation in progress, safety scaffolding, architectural cladding"
        else:
            stage_desc = "pristine finished building, immaculate landscaping, evening architectural dusk lighting, cinematic luxury presentation"

        prompt_text = (
            f"Photorealistic 8k architectural render of {base_desc}, {stage_desc}, "
            f"set in modern {city_ref} metropolis skyline, {architectural_style} design philosophy, "
            f"Unreal Engine 5 render, cinematic lighting, volumetric atmospheric rays, masterwork architectural photography"
        )

        import urllib.parse
        encoded_prompt = urllib.parse.quote_plus(prompt_text)
        # Seed based on prompt length and completion pct for stable reproducible image
        seed = int(completion_pct * 17 + len(structure_type) * 31)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=640&seed={seed}&nologo=true"

        return prompt_text, image_url
