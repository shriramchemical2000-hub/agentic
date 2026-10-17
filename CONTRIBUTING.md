# Working together

## Ownership
Every folder has an owner (see `docs/team_tasks.md`). You may edit any file, but the owner reviews changes to theirs.

| Area | Owner role |
|---|---|
| `src/demand_agents/data/`, `scripts/fetch_noaa_weather.py` | Data Engineering Lead |
| `src/demand_agents/models/gbm.py`, `baselines.py`, `agents/forecaster.py` | Forecasting Lead |
| `src/demand_agents/models/uncertainty.py`, `agents/uncertainty.py` | Uncertainty Lead |
| `src/demand_agents/agents/critic.py`, `evaluation/`, `experiments.py` | Critic and Evaluation Lead |
| `src/demand_agents/inventory/`, `agents/planner.py` | Inventory Planning Lead |
| `orchestrator.py`, `tracing.py`, `dashboard/`, `docs/`, report | Integration and Delivery Lead |

## Workflow
1. `git checkout -b <your-name>/<short-topic>` - never commit directly to `main`.
2. Make a change **with a test or a documented result**; run `pytest -q`.
3. Open a pull request; one other member reviews (CI also runs the tests).
4. Squash-merge. Keep `README.md` and `docs/` accurate when behaviour changes.

## Rules for results
- Choose settings on validation data; look at the test window once.
- Report synthetic and real-data results separately and never present synthetic results as real.
- If you change a metric or a default in `config/default.yaml`, rerun `python scripts/run_experiments.py all` and update the README tables.
