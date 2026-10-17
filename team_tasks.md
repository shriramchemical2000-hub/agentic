# Team task board

Names follow the roles in the first-draft submission, in the same order. Swap them if assignments change.
`[x]` = implemented and tested in this repository (read it, do not redo it). `[ ]` = still open - and everything still open
needs either **real data, a real decision, or a human**; no remaining item is "more code on synthetic data".

**Milestone 0 - first draft due 25 October 2026** (title, abstract, roles). A working pilot exists.

## Already learned from the first real run (M5 pilot)
At equal fill rate the Critic and nowcast layers did not reduce stock; the forecast blend is ~5% better than ETS; calibrated sigma reaches
higher fill rates than static sigma. **Fix made:** the Critic now learns its risk weights from validation errors and the nowcast trigger is
stricter; on calm synthetic worlds the extra stock fell from +8% to +2%, and in shock worlds the saving grew from 5% to 8% (see README).
Open: confirm the fix on real M5 (rerun the notebook), add weather, test on windows with real events.

## The 5 things that must happen (in this order)
1. **Run on real data.** Open `notebooks/colab_runner.ipynb` in Colab, add a Kaggle token, switch on `RUN_M5` and `RUN_WALMART_REAL`.
2. **Re-tune on the real validation window** (Critic weights, thresholds) - never on the test window.
3. **Replace placeholder costs and lead time** with justified values (`docs/assumptions.md`).
4. **Rate the agent traces** (`scripts/export_trace_review.py`, rubric in `docs/trace_review.md`).
5. **Write the report** (`scripts/build_report.py` drafts section 4 automatically; the TODO sections are yours).

---

## Suvigya Gangele - Data Engineering Lead  (`src/demand_agents/data/`)
- [x] Synthetic daily data with known shocks; Walmart-format weekly generator; M5 loader (pre-launch filter); Walmart loader; NOAA fetch script + merge
- [ ] Download M5 and Walmart and run both (Colab notebook does the download); fix any loader surprises
- [ ] Run `scripts/fetch_noaa_weather.py` (never tested against the live NOAA service) and check the merged temperatures
- [ ] Data-quality report on the real files (missing prices, zero stretches, outliers) and a justified pilot subset
- [ ] Optional features: SNAP days, days to/from event, promotion frequency

## Krishna Kumar - Forecasting Lead  (`models/`, `agents/forecaster.py`)
- [x] Gradient boosting, LightGBM option, seasonal naive / ETS / ARIMA baselines, model selection incl. ETS blend, leakage test
- [ ] Tune hyper-parameters with time-based cross-validation on real data; try per-category models
- [ ] Report WAPE / RMSE / bias on the real data (overall and on shock days); add Prophet if time permits

## Shriram P - Uncertainty Lead  (`models/uncertainty.py`, `agents/uncertainty.py`)
- [x] Conformal intervals (count / continuous), shrinkage, risk-aware widening, adaptive conformal updating, multi-period
      sigma correction, reliability scores, calibration curves and coverage by store/item (dashboard "Calibration" tab)
- [ ] Surge shocks remain under-covered (~68%) because of the information delay; try quantile gradient boosting or a shorter-horizon
      model for the intervals and measure it against `interval_metrics.csv`
- [ ] Study the real-data calibration plots and explain any differences from the synthetic ones

## Sonali Pattanaik - Critic and Evaluation Lead  (`agents/critic.py`, `evaluation/`, `experiments.py`)
- [x] Learned weather sensitivity, drift / event / price signals, precision and recall, five-policy ablation ladder, multi-seed suite,
      service-level / lead-time / cost sweeps, efficiency frontier, trace-review export
- [ ] Re-tune thresholds and risk weights on real validation data (we tuned on synthetic seeds 201-203 only)
- [ ] Organise the qualitative review: two raters, `docs/trace_review.md`, quote the traces in the report

## Bhaskara Veera Kumar Rayavarapu - Inventory Planning Lead  (`inventory/`, `agents/planner.py`)
- [x] Base-stock and (s, S) policies, nowcast correction, random supplier delays, batch / MOQ, fixed order cost, ABC service levels,
      lead-time buffer, what-if tab in the dashboard
- [ ] **Justify and cite the cost parameters and lead time** (`docs/assumptions.md` lists what to fill in)
- [ ] Decide how to present the Walmart "units" (dollars of sales)

## Dilip S Biradar - Integration and Delivery Lead  (`orchestrator.py`, `tracing.py`, `dashboard/`, report, repo)
- [x] Orchestrator + revision loop, JSONL traces, 8-tab dashboard, Colab notebook, CI workflow, `CONTRIBUTING.md`, 37 tests
- [ ] Create the Git repository, push this code, protect `main`, confirm CI is green
- [ ] Coordinate the final report (`scripts/build_report.py` output + the team's sections) and record the demo video
- [ ] Optional: port the agents to CrewAI / LangGraph while keeping the trace format

---

## Everyone
- Choose settings on validation data; report the test window once.
- Report synthetic and real-data results separately.
- Be able to explain your own agent and the overall flow in the viva; read the "Known limitations" in the README.
