from fastapi import FastAPI
from typing import Dict
from itertools import permutations

app = FastAPI()

# Define product locations
warehouse_inventory = {
    'C1': ['A', 'B', 'C'],
    'C2': ['D', 'E', 'F'],
    'C3': ['G', 'H', 'I']
}

product_to_center = {p: c for c, products in warehouse_inventory.items() for p in products}

# Distances to L1
center_to_L1_distance = {
    'C1': 10,
    'C2': 15,
    'C3': 20
}

# Delivery cost rates per kg per km
center_rates = {
    'C1': 5.2,
    'C2': 12.0,
    'C3': 1.2
}

PRODUCT_WEIGHT = 0.5

@app.post("/calculate-min-cost")
async def calculate_min_cost(order: Dict[str, int]):
    center_weights = {'C1': 0, 'C2': 0, 'C3': 0}
    centers_needed = set()

    # Compute total weight to be picked up from each center
    for product, quantity in order.items():
        center = product_to_center.get(product)
        if center:
            weight = quantity * PRODUCT_WEIGHT
            center_weights[center] += weight
            centers_needed.add(center)

    # Now simulate all routes to pick up and deliver
    min_cost = float('inf')

    for start_center in centers_needed:
        other_centers = list(centers_needed - {start_center})
        for route in permutations(other_centers):
            path = [start_center] + list(route)
            total_cost = 0
            current = path[0]

            # Deliver from start to L1
            total_cost += (
                center_weights[current]
                * center_to_L1_distance[current]
                * center_rates[current]
            )

            for next_center in path[1:]:
                # Move empty to next center (free), pick up and deliver to L1
                total_cost += (
                    center_weights[next_center]
                    * center_to_L1_distance[next_center]
                    * center_rates[next_center]
                )
                current = next_center

            min_cost = min(min_cost, total_cost)

    return {"minimum_cost": int(round(min_cost))}

