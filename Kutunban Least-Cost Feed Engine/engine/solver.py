import pulp
from typing import Dict, Any, Tuple, Optional

class FeedOptimizer:
    def __init__(self, ingredients: Dict[str, Any]):
        self.ingredients = ingredients

    def solve(
        self, 
        profile: Dict[str, Any], 
        batch_size_kg: float = 100.0
    ) -> Tuple[Optional[Dict[str, float]], Optional[float], str]:
        """
        Formulates least-cost feed using Linear Programming (PuLP).
        """
        model = pulp.LpProblem("Kaduna_Least_Cost_Feed", pulp.LpMinimize)
        
        ing_keys = list(self.ingredients.keys())
        vars_dict = {
            name: pulp.LpVariable(f"ing_{name}", lowBound=0) 
            for name in ing_keys
        }
        
        # Objective Function: Total batch cost minimization
        model += pulp.lpSum([
            vars_dict[name] * self.ingredients[name]["cost_per_kg"] 
            for name in ing_keys
        ]), "Total_Batch_Cost"
        
        # Weight Constraint
        model += pulp.lpSum([vars_dict[name] for name in ing_keys]) == batch_size_kg, "Total_Batch_Weight"
        
        # Nutrient Minimums
        min_reqs = profile.get("min_constraints", {})
        for nutrient, min_val in min_reqs.items():
            model += pulp.lpSum([
                vars_dict[name] * self.ingredients[name]["nutrients"].get(nutrient, 0.0)
                for name in ing_keys
            ]) >= min_val * batch_size_kg, f"Min_{nutrient}"

        # Nutrient Maximums
        max_reqs = profile.get("max_constraints", {})
        for nutrient, max_val in max_reqs.items():
            model += pulp.lpSum([
                vars_dict[name] * self.ingredients[name]["nutrients"].get(nutrient, 0.0)
                for name in ing_keys
            ]) <= max_val * batch_size_kg, f"Max_{nutrient}"

        model.solve(pulp.PULP_CBC_CMD(msg=False))
        
        status = pulp.LpStatus[model.status]
        if status != "Optimal":
            return None, None, f"Infeasible formulation: {status}"

        recipe = {name: round(vars_dict[name].varValue, 2) for name in ing_keys if vars_dict[name].varValue > 0.001}
        total_cost = round(pulp.value(model.objective), 2)

        return recipe, total_cost, "Optimal"
