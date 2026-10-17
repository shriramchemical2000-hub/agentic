# Data guide

The pipeline runs on built-in **synthetic data** by default, so everyone can develop without downloads.
Switch to real data with `--source m5` once the files are in place.

## M5 Forecasting (primary dataset)

1. Download from Kaggle: https://www.kaggle.com/competitions/m5-forecasting-accuracy (accept the rules first).
2. Put these files in `data/raw/m5/`:
   - `calendar.csv`
   - `sales_train_evaluation.csv` (or `sales_train_validation.csv`)
   - `sell_prices.csv`
3. Run `python scripts/run_pipeline.py --source m5 --output-dir outputs/m5_pilot`.

`load_m5` drops rows before an item's first priced week (not yet launched in that store), so launch-period zeros are
not mistaken for demand, and takes a **pilot subset** (`data.m5.n_stores`, `n_items`, `max_days` in the config) - the
highest-volume items in the first N stores. Keep it small until the pipeline is stable, then scale up.
The M5 events (`event_name_1`) become the `is_event` feature; there is no weather in M5 until NOAA is merged.

## NOAA weather (optional)

Automatic: `python scripts/fetch_noaa_weather.py --out data/raw/weather_m5.csv` downloads GHCN-Daily station files from
NOAA (no API key) and writes `date, state_id, temp` (mean of TMAX and TMIN in degrees C). Defaults: one airport station
per M5 state (CA = Los Angeles, TX = Houston, WI = Milwaukee); override with `--station CA=USW...`. M5 does not reveal
store locations, so state-level weather is the best available link; `merge_noaa` matches `state_id` to the prefix of
the store id (CA_1 -> CA). Then set `data.noaa.path: data/raw/weather_m5.csv`.

Manual: any CSV with `date, temp` plus optionally `store_id` or `state_id` works. Without weather the temperature
features are NaN and the Critic's weather flag never fires.

## Walmart weekly sales

Download https://www.kaggle.com/datasets/yasserh/walmart-dataset, put `Walmart.csv` in `data/raw/walmart/`, then run
`python scripts/run_pipeline.py --config config/walmart.yaml`. It is weekly store-level dollar sales (45 stores), so the
pipeline runs in weekly mode and treats one inventory "unit" as one dollar of sales volume. Holiday flag, temperature
(converted from Fahrenheit), fuel price, CPI and unemployment are used as features.
Without the file, `--source walmart_synthetic` generates data in the exact same column format for testing.

## Canonical schema

| column | meaning |
|---|---|
| `date` | day |
| `store_id`, `item_id`, `series_id` | `series_id = store_id + "_" + item_id` |
| `sales` | units sold (demand) |
| `sell_price` | price that day |
| `is_event` | 1 on holidays / events |
| `temp` | daily mean temperature (NaN if unavailable) |
| `shock_type`, `is_shock` | synthetic data only: ground-truth shocks for evaluating the Critic |
