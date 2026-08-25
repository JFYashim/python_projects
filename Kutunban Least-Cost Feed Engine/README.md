# Kutunban Livestock Least-Cost Feed Engine (KLCF)

An optimization backend built with Python and PuLP to calculate least-cost livestock feed formulations using local Kaduna market pricing and ingredient profiles.

## Project Structure

```text
kutunban-lcf-engine/
├── data/
│   ├── ingredients.json     # Local ingredient prices & nutritional matrix
│   └── profiles.json        # Animal target nutritional constraints
├── engine/
│   └── solver.py            # PuLP optimization engine implementation
├── README.md                # Project documentation & setup instructions
├── main.py                  # Pipeline execution script
└── requirements.txt         # Project dependencies (pulp, etc.)
