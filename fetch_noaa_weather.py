#!/usr/bin/env python
"""Download NOAA GHCN-Daily station data and write a weather CSV for the pipeline (date, state_id, temp).

    python scripts/fetch_noaa_weather.py --out data/raw/weather_m5.csv \
        --station CA=USW00023174 --station TX=USW00012960 --station WI=USW00014839

Default stations are one representative airport station per M5 state (Los Angeles, Houston, Milwaukee) - M5 does not
reveal store locations, so state-level weather is the best available link. Then set data.noaa.path in the config.
Needs internet access to ncei.noaa.gov (no API key). The parsing is unit-tested offline with a sample file.
"""
import argparse
import io
import sys
from pathlib import Path
from urllib.request import urlopen

import pandas as pd

URL = "https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/access/{station}.csv"
DEFAULT_STATIONS = {"CA": "USW00023174", "TX": "USW00012960", "WI": "USW00014839"}


def parse_ghcn_daily(csv_text: str, state_id: str) -> pd.DataFrame:
    """GHCN-Daily CSV -> DataFrame[date, state_id, temp] with temp = mean of TMAX and TMIN in degrees C."""
    raw = pd.read_csv(io.StringIO(csv_text), usecols=lambda c: c in ("DATE", "TMAX", "TMIN"))
    raw["date"] = pd.to_datetime(raw["DATE"])
    tmax, tmin = raw["TMAX"].astype(float), raw["TMIN"].astype(float)
    if max(tmax.abs().median(), tmin.abs().median()) > 60:  # raw GHCN units are tenths of a degree C
        tmax, tmin = tmax / 10.0, tmin / 10.0
    out = pd.DataFrame({"date": raw["date"], "state_id": state_id, "temp": (tmax + tmin) / 2.0})
    out = out.dropna(subset=["temp"]).sort_values("date")
    out["temp"] = out["temp"].round(1)
    return out.reset_index(drop=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="data/raw/weather_m5.csv")
    ap.add_argument("--station", action="append", default=[], help="STATE=STATION_ID (repeatable)")
    ap.add_argument("--start", default="2011-01-01")
    ap.add_argument("--end", default="2016-12-31")
    args = ap.parse_args()
    stations = dict(s.split("=") for s in args.station) or DEFAULT_STATIONS

    frames = []
    for state, station in stations.items():
        print(f"Downloading {station} for {state} ...")
        text = urlopen(URL.format(station=station), timeout=120).read().decode()
        df = parse_ghcn_daily(text, state)
        frames.append(df[(df["date"] >= args.start) & (df["date"] <= args.end)])
    out = pd.concat(frames, ignore_index=True)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out, index=False)
    print(f"Wrote {len(out):,} rows to {args.out}. Set data.noaa.path to this file.")


if __name__ == "__main__":
    sys.exit(main())
