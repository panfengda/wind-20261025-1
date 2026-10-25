from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import requests
import pandas as pd

API_URL = "https://archive-api.open-meteo.com/v1/archive"
HOURLY = [
    "temperature_2m", "relative_humidity_2m", "precipitation",
    "rain", "wind_speed_10m", "wind_gusts_10m", "wind_direction_10m",
    "wind_speed_100m",
]
UNITS = {
    "temperature_2m": "°C", "relative_humidity_2m": "%",
    "precipitation": "mm/hour", "rain": "mm/hour",
    "wind_speed_10m": "m/s", "wind_gusts_10m": "m/s",
    "wind_direction_10m": "degree", "wind_speed_100m": "m/s",
}
SITES = {
    "North Sea example (offshore)": {"latitude": 54.5, "longitude": 2.0, "site_type": "offshore", "elevation_m": None},
    "Central US example (plain)": {"latitude": 35.2, "longitude": -101.8, "site_type": "plain", "elevation_m": 1000},
    "Sierra Nevada example (mountain)": {"latitude": 39.5, "longitude": -120.2, "site_type": "mountain", "elevation_m": 2000},
}


def fetch_archive(site_name: str, site: dict, start_date: str, end_date: str, timeout: int = 40):
    params = {
        "latitude": site["latitude"],
        "longitude": site["longitude"],
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ",".join(HOURLY),
        "timezone": "UTC",
        "wind_speed_unit": "ms",
        "precipitation_unit": "mm",
        "cell_selection": "sea" if site["site_type"] == "offshore" else "land",
    }
    if site.get("elevation_m") is not None:
        params["elevation"] = site["elevation_m"]
    response = requests.get(API_URL, params=params, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    hourly = payload.get("hourly")
    if not hourly or "time" not in hourly:
        raise ValueError("API 响应缺少 hourly.time")
    df = pd.DataFrame(hourly)
    df["timestamp_utc"] = pd.to_datetime(df.pop("time"), utc=True, errors="coerce")
    df["site_id"] = site_name
    df["site_type"] = site["site_type"]
    df["latitude"] = site["latitude"]
    df["longitude"] = site["longitude"]
    df["source_type"] = "reanalysis"
    df["source_name"] = "Open-Meteo Historical Weather API / ERA5-family reanalysis"
    df["retrieved_at_utc"] = datetime.now(timezone.utc).isoformat()
    df["api_response_sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")
    ).hexdigest()
    df["time_zone"] = "UTC"
    return df, payload


def quality_check(df: pd.DataFrame) -> pd.DataFrame:
    """Flag, do not silently delete, missing/duplicate/out-of-range records."""
    out = df.copy()
    out["quality_flags"] = ""
    ranges = {
        "temperature_2m": (-70, 65),
        "relative_humidity_2m": (0, 100),
        "precipitation": (0, 500),
        "rain": (0, 500),
        "wind_speed_10m": (0, 80),
        "wind_gusts_10m": (0, 100),
        "wind_direction_10m": (0, 360),
        "wind_speed_100m": (0, 100),
    }
    flags = [[] for _ in range(len(out))]
    for col, (lo, hi) in ranges.items():
        if col not in out:
            continue
        values = pd.to_numeric(out[col], errors="coerce")
        for i, val in enumerate(values):
            if pd.isna(val):
                flags[i].append(f"{col}:missing")
            elif not lo <= float(val) <= hi:
                flags[i].append(f"{col}:out_of_range")
    duplicated = out.duplicated(["site_id", "timestamp_utc"], keep=False)
    for i, is_dup in enumerate(duplicated):
        if is_dup:
            flags[i].append("duplicate_site_timestamp")
    out["quality_flags"] = [";".join(x) for x in flags]
    out["quality_status"] = out["quality_flags"].map(
        lambda x: "flagged" if x else "range_checks_passed"
    )
    # Keep duplicate rows for audit; a separate deduplicated analytical copy can be created.
    return out


def analysis_copy(df: pd.DataFrame) -> pd.DataFrame:
    """Deduplicate only for analysis, keeping raw data untouched."""
    return (
        df.sort_values(["site_id", "timestamp_utc", "retrieved_at_utc"])
          .drop_duplicates(["site_id", "timestamp_utc"], keep="last")
          .copy()
    )


def save_dataset(df: pd.DataFrame, output_dir: str | Path = "data"):
    output_dir = Path(output_dir)
    raw_dir = output_dir / "raw"
    processed_dir = output_dir / "processed"
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    sites = "-".join(sorted(df["site_id"].astype(str).unique())).replace("/", "_").replace(" ", "_")[:60]
    raw_path = raw_dir / f"weather_raw_{stamp}_{sites}.csv"
    processed_path = processed_dir / f"weather_checked_{stamp}_{sites}.csv"
    df.to_csv(raw_path, index=False)
    checked = quality_check(df)
    checked.to_csv(processed_path, index=False)
    return raw_path, processed_path
