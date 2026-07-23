# backend/scenarios/sample_scenarios.py

HURRICANE_PORT_CLOSURE = {
    "scenario_id": "hurricane_port_2024",
    "description": "Major port closed by hurricane. Need 10,000 units shipped urgently.",
    "max_rounds": 3,
    
    "constraints": {
        "units_needed": 10000,
        "deadline_days": 7,
        "budget_ceiling": 50000,
        "min_reliability": 0.95
    },
    
    # RESTRICTED VIEW: Only Logistics Chief sees this
    "logistics_view": {
        "carrier_capacity": {
            "air": 2000,    # Can only move 2000 by air
            "truck": 8000,  # Truck can handle 8000
            "ocean": 15000  # Ocean has capacity but slow
        },
        "transit_times": {
            "air": 1,       # 1 day by air
            "truck": 3,     # 3 days by truck
            "ocean": 14     # 14 days by ocean (too slow!)
        },
        "reliability": {
            "air": 0.99,    # Very reliable
            "truck": 0.92,  # Good but some risk
            "ocean": 0.85   # Risky due to congestion
        },
        "hidden_info": "Ocean route has 30% additional delay risk due to hurricane aftermath congestion"
    },
    
    # RESTRICTED VIEW: Only CFO sees this
    "cfo_view": {
        "cost_per_unit": {
            "air": 8,       # $8 per unit by air = $80K for 10K units (over budget!)
            "truck": 3,     # $3 per unit by truck = $30K (within budget)
            "ocean": 1      # $1 per unit by ocean = $10K (cheapest)
        },
        "budget_flexibility": "Can exceed by 10% ($55K max) if CEO approves, but requires 24hr notice",
        "hidden_info": "Q4 budget locks tomorrow at 5pm - after that no flexibility"
    },
    
    # PARTIAL VIEW: Mediator sees this plus debate transcript
    "operations_view": {
        "visible_constraints": ["units_needed", "deadline_days"],
        "hard_constraints": [
            "Must deliver within 7 days (contractual penalty: $10K/day late)",
            "Reliability must be ≥95% (customer will cancel if unreliable)"
        ],
        "mediator_only_data": "Customer relationship at stake - they've threatened to switch suppliers if this fails"
    }
}

BUDGET_CUT_CRISIS = {
    "scenario_id": "budget_cut_mid_shipment",
    "description": "Mid-Q4 budget cut announced. Must reship existing order with 40% less budget.",
    "max_rounds": 3,
    
    "constraints": {
        "units_needed": 5000,
        "deadline_days": 5,
        "budget_ceiling": 12000,  # Cut from $20K to $12K
        "min_reliability": 0.90
    },
    
    "logistics_view": {
        "carrier_capacity": {"air": 1500, "truck": 6000, "ocean": 10000},
        "transit_times": {"air": 1, "truck": 2, "ocean": 10},
        "reliability": {"air": 0.98, "truck": 0.88, "ocean": 0.82},
        "hidden_info": "Truck drivers threatening strike next week - capacity may drop 50%"
    },
    
    "cfo_view": {
        "cost_per_unit": {"air": 6, "truck": 2.4, "ocean": 0.8},
        "budget_flexibility": "ZERO flexibility - cuts already approved by board",
        "hidden_info": "If we exceed budget, department faces layoffs"
    },
    
    "operations_view": {
        "visible_constraints": ["deadline_days"],
        "hard_constraints": [
            "Must deliver in 5 days or lose $50K contract",
            "Cost cannot exceed $12,000 absolute maximum"
        ],
        "mediator_only_data": "This customer is our biggest account - losing them = company bankruptcy risk"
    }
}

CAPACITY_CRUNCH = {
    "scenario_id": "holiday_capacity_crunch",
    "description": "Holiday season surge. All carriers at 90%+ capacity. Need 15,000 units in 10 days.",
    "max_rounds": 3,
    
    "constraints": {
        "units_needed": 15000,
        "deadline_days": 10,
        "budget_ceiling": 75000,
        "min_reliability": 0.93
    },
    
    "logistics_view": {
        "carrier_capacity": {
            "air": 3000,     # Limited air cargo slots
            "truck": 9000,   # Trucks available but premium pricing
            "ocean": 20000   # Ocean has space but very slow
        },
        "transit_times": {"air": 1, "truck": 4, "ocean": 12},
        "reliability": {"air": 0.97, "truck": 0.89, "ocean": 0.80},
        "hidden_info": "Air cargo prices spike 3x during holidays - book NOW or lose slots"
    },
    
    "cfo_view": {
        "cost_per_unit": {"air": 10, "truck": 4, "ocean": 1.2},
        "budget_flexibility": "Can request emergency $15K contingency fund (requires VP approval)",
        "hidden_info": "Marketing spent over budget on holiday ads - limited goodwill for extra spend"
    },
    
    "operations_view": {
        "visible_constraints": ["units_needed", "deadline_days"],
        "hard_constraints": [
            "Must deliver before Black Friday (day 10)",
            "Stockout cost: $200K in lost sales per day"
        ],
        "mediator_only_data": "CEO personally promised this shipment to key retail partner"
    }
}

# List of all scenarios for easy iteration
ALL_SCENARIOS = [
    HURRICANE_PORT_CLOSURE,
    BUDGET_CUT_CRISIS,
    CAPACITY_CRUNCH
]

def get_scenario_by_id(scenario_id: str) -> dict:
    """Get scenario by ID"""
    for scenario in ALL_SCENARIOS:
        if scenario["scenario_id"] == scenario_id:
            return scenario
    raise ValueError(f"Scenario '{scenario_id}' not found")
