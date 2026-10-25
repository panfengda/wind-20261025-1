from __future__ import annotations
import pandas as pd

DISCLAIMER = (
    "LEE exposure proxy only. It is not coating mass loss, erosion depth, damage percentage, "
    "failure probability, or remaining useful life."
)


def add_exposure_proxy(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transparent screening index, not a calibrated erosion model.
    It ranks weather exposure using wind and rain inputs only.
    Do not interpret as physical erosion damage.
    """
    out = df.copy()
    wind = pd.to_numeric(out.get("wind_speed_100m"), errors="coerce")
    if wind is None or wind.isna().all():
        wind = pd.to_numeric(out.get("wind_speed_10m"), errors="coerce")
    rain = pd.to_numeric(out.get("rain", out.get("precipitation")), errors="coerce")
    gust = pd.to_numeric(out.get("wind_gusts_10m"), errors="coerce")
    # Normalize to documented reference scales solely for a unitless screening score.
    wind_term = (wind.clip(lower=0, upper=30) / 30).fillna(0)
    rain_term = (rain.clip(lower=0, upper=10) / 10).fillna(0)
    gust_term = (gust.clip(lower=0, upper=40) / 40).fillna(0)
    out["lee_exposure_proxy_0_100"] = (
        100 * (0.50 * wind_term + 0.35 * rain_term + 0.15 * gust_term)
    ).round(3)
    out["model_status"] = "screening_proxy_not_validated"
    out["model_assumptions"] = (
        "Linear normalized wind/rain/gust score; no droplet-size distribution, blade geometry, "
        "relative blade speed, coating properties, UV ageing, or erosion-test calibration."
    )
    return out


def aggregate_site_exposure(df: pd.DataFrame) -> pd.DataFrame:
    if "lee_exposure_proxy_0_100" not in df:
        df = add_exposure_proxy(df)
    return df.groupby(["site_id", "site_type"], as_index=False).agg(
        records=("timestamp_utc", "count"),
        mean_wind_100m_ms=("wind_speed_100m", "mean"),
        total_rain_mm=("rain", "sum"),
        max_gust_ms=("wind_gusts_10m", "max"),
        mean_lee_exposure_proxy=("lee_exposure_proxy_0_100", "mean"),
        p95_lee_exposure_proxy=("lee_exposure_proxy_0_100", lambda s: s.quantile(.95)),
    )
