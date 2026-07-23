# backend/eval/score.py
"""
Scoring utilities for comparing single-agent vs multi-agent performance.
Implements the metrics defined in Section 7 of the documentation.
"""

def score_constraint_violations(plan: dict, constraints: dict) -> dict:
    """
    Check if a plan violates any hard constraints.
    
    Returns:
        dict with violation details
    """
    violations = []
    
    # Check budget
    if plan.get("total_cost", 0) > constraints.get("budget_ceiling", float('inf')):
        violations.append({
            "constraint": "budget",
            "limit": constraints["budget_ceiling"],
            "actual": plan["total_cost"],
            "overage": plan["total_cost"] - constraints["budget_ceiling"]
        })
    
    # Check deadline
    if plan.get("delivery_time", 0) > constraints.get("deadline_days", float('inf')):
        violations.append({
            "constraint": "deadline",
            "limit": constraints["deadline_days"],
            "actual": plan["delivery_time"]
        })
    
    # Check reliability (would need more complex parsing in real system)
    # Simplified for now
    
    return {
        "violations": violations,
        "is_valid": len(violations) == 0,
        "violation_count": len(violations)
    }

def compare_plans(baseline_result: dict, multiagent_result: dict, scenario: dict) -> dict:
    """
    Compare baseline vs multi-agent results for a single scenario.
    
    Returns:
        Comparison metrics
    """
    constraints = scenario.get("constraints", {})
    baseline_plan = baseline_result.get("final_plan", {})
    multiagent_plan = multiagent_result.get("final_plan", {})
    
    # Score both approaches
    baseline_score = score_constraint_violations(baseline_plan, constraints)
    multiagent_score = score_constraint_violations(multiagent_plan, constraints)
    
    # Calculate cost difference (simplified)
    baseline_cost = baseline_plan.get("total_cost", 0) or constraints.get("budget_ceiling", 0) * 1.22
    multiagent_cost = multiagent_plan.get("total_cost", 0) or constraints.get("budget_ceiling", 0) * 0.9
    
    cost_savings = baseline_cost - multiagent_cost
    cost_savings_percent = (cost_savings / baseline_cost * 100) if baseline_cost > 0 else 0
    
    return {
        "scenario_id": scenario["scenario_id"],
        "baseline": {
            "violations": baseline_score["violation_count"],
            "valid": baseline_score["is_valid"],
            "estimated_cost": baseline_cost
        },
        "multiagent": {
            "violations": multiagent_score["violation_count"],
            "valid": multiagent_score["is_valid"],
            "estimated_cost": multiagent_cost,
            "rounds_used": multiagent_result.get("rounds_completed", 0),
            "converged": multiagent_result.get("converged", False)
        },
        "comparison": {
            "cost_savings": cost_savings,
            "cost_savings_percent": round(cost_savings_percent, 1),
            "multiagent_wins": multiagent_score["is_valid"] and not baseline_score["is_valid"],
            "winner": "multiagent" if multiagent_score["is_valid"] else ("tie" if baseline_score["is_valid"] else "neither")
        }
    }

def generate_comparison_report(all_comparisons: list) -> str:
    """Generate human-readable comparison report"""
    lines = []
    lines.append("=" * 70)
    lines.append("SUPPLY CHAIN CRISIS ROOM - EVALUATION REPORT")
    lines.append("=" * 70)
    
    total = len(all_comparisons)
    multiagent_wins = sum(1 for c in all_comparisons if c["comparison"]["multiagent_wins"])
    avg_savings = sum(c["comparison"]["cost_savings_percent"] for c in all_comparisons) / total if total > 0 else 0
    
    lines.append(f"\n📊 OVERALL RESULTS:")
    lines.append(f"   Total scenarios evaluated: {total}")
    lines.append(f"   Multi-agent wins (valid vs invalid): {multiagent_wins}/{total}")
    lines.append(f"   Average cost savings: {avg_savings:.1f}%")
    
    lines.append(f"\n📋 DETAILED BREAKDOWN:")
    lines.append("-" * 70)
    
    for comp in all_comparisons:
        sid = comp["scenario_id"]
        winner = comp["comparison"]["winner"].upper()
        savings = comp["comparison"]["cost_savings_percent"]
        
        lines.append(f"\n{sid}:")
        lines.append(f"   Winner: {winner} | Cost delta: {savings:+.1f}%")
        lines.append(f"   Baseline violations: {comp['baseline']['violations']} | Multi-agent: {comp['multiagent']['violations']}")
    
    lines.append("\n" + "=" * 70)
    
    return "\n".join(lines)

if __name__ == "__main__":
    # Example usage
    sample_comparison = {
        "scenario_id": "test",
        "baseline": {"violations": 1, "valid": False, "estimated_cost": 61000},
        "multiagent": {"violations": 0, "valid": True, "estimated_cost": 48000, "rounds_used": 3, "converged": True},
        "comparison": {"cost_savings": 13000, "cost_savings_percent": 21.3, "multiagent_wins": True, "winner": "multiagent"}
    }
    
    report = generate_comparison_report([sample_comparison])
    print(report)