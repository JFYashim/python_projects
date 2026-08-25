import json
import os
from engine.solver import FeedOptimizer

def run():
    # Construct paths relative to this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ingredients_path = os.path.join(base_dir, "data", "ingredients.json")
    profiles_path = os.path.join(base_dir, "data", "profiles.json")

    # 1. Load data
    with open(ingredients_path, "r") as f:
        ingredients = json.load(f)
    
    with open(profiles_path, "r") as f:
        profiles = json.load(f)

    # 2. Initialize optimizer engine
    optimizer = FeedOptimizer(ingredients)
    
    # 3. Choose a target profile (e.g., broiler_finisher, noiler_grower, pig_grower)
    profile_key = "broiler_finisher"
    selected_profile = profiles[profile_key]
    batch_kg = 100.0

    # 4. Run solver
    recipe, total_cost, status = optimizer.solve(selected_profile, batch_size_kg=batch_kg)

    if status != "Optimal":
        print(f"Error formulating feed: {status}")
        return

    # 5. Output formatted results
    print("=" * 55)
    print(f"  KUTUNBAN LEAST-COST FEED ENGINE (KLCF)")
    print(f"  Target Formula: {selected_profile['name']} ({batch_kg} kg batch)")
    print("=" * 55)
    
    for ing, weight in recipe.items():
        pct = (weight / batch_kg) * 100
        cost = weight * ingredients[ing]["cost_per_kg"]
        print(f" - {ing:<16}: {weight:>6.2f} kg ({pct:>5.1f}%) | ₦{cost:,.2f}")

    print("-" * 55)
    print(f" Total Cost per 100 kg Batch : ₦{total_cost:,.2f}")
    print(f" Cost per 25 kg Bag           : ₦{(total_cost / batch_kg) * 25:,.2f}")
    print(f" Cost per 1 kg Feed           : ₦{total_cost / batch_kg:,.2f}")
    print("=" * 55)

if __name__ == "__main__":
    run()
