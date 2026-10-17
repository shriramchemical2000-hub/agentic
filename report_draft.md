# Agentic Demand Forecasting & Inventory Optimization - Final Report (DRAFT)

_Auto-generated from `outputs/latest` (data source: **synthetic**). Replace every TODO before submitting._

## 1. Problem and objectives
TODO: reuse the abstract from the first draft; state the four objectives of the brief.

## 2. System design
Four collaborating agents (Forecaster, Uncertainty, Critic, Planner) coordinated by an orchestrator; see `docs/architecture.md` and the diagram in the README. All reasoning is logged to `traces.jsonl`.

## 3. Data
TODO (Data Engineering Lead): sources, pilot subset, cleaning, data-quality findings, weather source.

## 4. Quantitative evaluation

### 4.1 Forecast accuracy on the test window (WAPE, lower is better)
| model | all | normal_days | shock_days |
|---|---|---|---|
| agentic_forecast | 0.318 | 0.310 | 0.336 |
| ets | 0.399 | 0.371 | 0.456 |
| gbm_only | 0.318 | 0.310 | 0.336 |
| seasonal_naive | 0.528 | 0.526 | 0.532 |

The Forecaster chose **gbm** on held-out validation data.

### 4.2 Prediction intervals (90% target)
| segment | n | coverage | mean_width |
|---|---|---|---|
| all | 2016 | 0.884 | 17.345 |
| shock_days | 393 | 0.753 | 21.859 |
| normal_days | 1623 | 0.916 | 16.252 |
| shock:event | 117 | 0.829 | 25.090 |
| shock:heatwave | 150 | 0.813 | 22.077 |
| shock:surge | 126 | 0.611 | 18.598 |

### 4.3 Critic quality
- flagged_share: 0.308
- mean_abs_error_flagged: 1.427
- mean_abs_error_unflagged: 0.986
- error_ratio_flagged_vs_unflagged: 1.447
- precision: 0.524
- recall: 0.827

### 4.4 Inventory simulation (same demand for every policy)
| policy | fill_rate | stockout_rate | avg_on_hand_units | total_cost |
|---|---|---|---|---|
| classical_ets | 0.911 | 0.120 | 16.933 | 13331.201 |
| gbm_static | 0.946 | 0.088 | 14.092 | 8213.502 |
| gbm_calibrated | 0.949 | 0.083 | 14.673 | 7687.063 |
| agentic_risk | 0.957 | 0.068 | 15.494 | 6572.254 |
| agentic | 0.965 | 0.058 | 16.739 | 5436.307 |

Stock is measured in: units.

### 4.5 Fair comparison: average stock needed for a target fill rate (lower is better)
| target_fill_rate | agentic | agentic_risk | classical_ets | gbm_calibrated | gbm_static |
|---|---|---|---|---|---|
| 93.0% | 10.9 | 11.3 | 21.0 | 11.6 | 11.6 |
| 95.1% | 13.8 | 14.4 | not reached | 15.1 | 15.3 |
| 96.7% | 17.3 | 18.3 | not reached | 19.6 | 20.6 |

'not reached' = the policy never hits that fill rate within the tested service levels (80-99.5%).

### 4.6 Robustness over independent synthetic worlds (mean and std)
| name | fill_rate_mean | fill_rate_std | total_cost_mean | total_cost_std |
|---|---|---|---|---|
| agentic | 0.972 | 0.006 | 3684.316 | 839.934 |
| agentic_risk | 0.962 | 0.007 | 4965.081 | 1425.109 |
| classical_ets | 0.926 | 0.010 | 9431.055 | 1956.001 |
| gbm_calibrated | 0.954 | 0.008 | 5927.910 | 1540.349 |
| gbm_static | 0.951 | 0.008 | 6320.583 | 1483.737 |

Figures: `outputs/figures/` (run `scripts/make_report_figures.py`).

## 5. Qualitative evaluation
TODO (Critic and Evaluation Lead): ratings from `scripts/export_trace_review.py`, quoted traces, lessons. See `docs/trace_review.md`.

## 6. Limitations
TODO: copy and update the 'Known limitations' of the README with what the real-data runs showed.

## 7. Conclusions and future work
TODO.

## 8. Team contributions
TODO: one paragraph per member, matching the roles in the first draft.
