# PFD Wind Twin Research Prototype — Blade Leading-Edge Erosion

A Streamlit research prototype for historical weather retrieval, multi-site comparison, data provenance, quality flags, and a clearly-labelled leading-edge-erosion (LEE) exposure screening proxy.

## Important scientific boundary

This repository does **not** currently predict real coating loss, erosion depth, failure probability, or remaining useful life. The LEE proxy is a transparent, unitless screening index built from historical weather variables. It is not calibrated to material rain-erosion tests or blade inspections. Do not present it as a validated physical model or AI predictor.

## Data source

- Open-Meteo Historical Weather API: https://open-meteo.com/en/docs/historical-weather-api
- Historical values are ERA5-family reanalysis estimates, not on-site turbine sensor measurements.
- Attribute Open-Meteo and its data sources as required by the applicable terms/licence. The public API is intended for non-commercial use; check current terms before other uses.
- API requests need no key for eligible non-commercial use.

## Public LEE reference

Pryor et al. (2024), *An Atlas of Wind Turbine Blade Leading Edge Erosion for CONUS*, Zenodo record 14247620:
https://zenodo.org/records/14247620

The atlas describes site-level LEE potential / accumulated distance-to-failure estimates based on meteorological measurements and modelling. It is not an hourly time series of measured coating damage. Use it only for exploratory external plausibility comparison at overlapping US sites, not as ground truth for hourly damage predictions.

Related papers:
- *Impact of meteorological data factors and material characterization method on predictions of leading edge erosion*, Renewable Energy (2024), DOI: 10.1016/j.renene.2024.120549.
- *Fast prediction of rain erosion in wind turbine blades using a data-based computational tool*, Journal of Hydrodynamics (2024), DOI: 10.1007/s42241-024-0044-4.

## Run locally

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

For local password protection, copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and replace the sample password. This secrets file is ignored by Git.

## Deploy to Streamlit Community Cloud

1. Push this repository to GitHub.
2. Create a new Streamlit app and choose `app.py` as the entry point.
3. Add `APP_PASSWORD = "your-long-random-password"` in the app's Streamlit Secrets settings.
4. Deploy. The shared-password gate is a lightweight prototype gate, not enterprise identity management.
5. Do not commit private secrets or sensitive turbine data to GitHub.

## Included pages

1. Historical weather and site comparison — fetch, view, and export CSV.
2. LEE exposure analysis — unitless proxy only, with explicit assumptions.
3. Data quality and provenance — missing/range/duplicate flags and source metadata.
4. Validation and research log — public reference atlas, validation readiness, and limits.

## Data handling design

- Raw API rows are saved separately under `data/raw/` with source, retrieval timestamp, units implied by API parameters, and API-response hash.
- Checked rows preserve original values and add quality flags.
- Duplicates remain in raw data; only an analysis copy is deduplicated.
- Network failures are shown to the user; the app does not silently replace failed real data with simulated data.
- Export buttons allow downloaded CSV snapshots.

## Validation plan

### Now
- Check API retrieval, timestamps, units, missing values, out-of-range values, duplicate timestamps.
- Compare weather summaries across candidate sites.
- Inspect source metadata and export repeatable CSV files.

### After downloading the public atlas
- Read the Zenodo record's data dictionary, method, and licence.
- Parse the NetCDF with `xarray` (add dependency only when needed).
- Compare overlapping US-site rankings / broad spatial patterns as a plausibility check.
- Document differences in resolution, variables, and assumptions.

### Before claiming damage prediction
Obtain at least one suitable target source: rain-erosion test (RET) material data, blade inspection/damage ratings, field observations, or a published dataset with usable target labels. Define target, time horizon, split strategy, and metrics before training. Use temporal and/or site-held-out testing to prevent leakage. Report uncertainty and the model's valid range.

## Suggested next data fields

`timestamp_utc`, `site_id`, `source_type`, `source_name`, `retrieved_at_utc`, `quality_flags`, `wind_speed_100m`, `wind_gusts_10m`, `rain`, `temperature_2m`, `relative_humidity_2m`.

For a future physical erosion model, add turbine model and rotor/blade geometry, rotor speed / blade pitch, droplet size and velocity distribution, coating material and thickness, RET calibration, UV/weathering history, and inspection labels.


## v2 交互式三维展示说明

首页已加入程序生成的三维海上风机示意模型、叶片分区颜色热图、环境参数控制、叶轮旋转控制和研究页面快捷入口。叶片模型不是购买的 CAD 资产，损伤颜色为交互式演示值，不应视为真实检测或寿命预测结果。

部署更新时请确保 `app.py`、`pfd/`、`pages/` 和 `requirements.txt` 位于 GitHub 仓库根目录。Streamlit Cloud 会根据 requirements.txt 安装新增依赖。
