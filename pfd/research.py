PUBLIC_REFERENCES = [
    {
        "title": "An Atlas of Wind Turbine Blade Leading Edge Erosion for CONUS",
        "authors": "Pryor et al. (2024)",
        "type": "Public site-level erosion-potential atlas",
        "url": "https://zenodo.org/records/14247620",
        "use": "External plausibility comparison for CONUS site-level erosion potential; not hourly blade damage ground truth.",
        "limitation": "Atlas reports accumulated distance-to-failure (ADF) derived from meteorological measurements and modeling. It does not provide an hourly measured coating-loss time series for validating this app's proxy.",
    },
    {
        "title": "Impact of meteorological data factors and material characterization method on predictions of leading edge erosion",
        "authors": "Renewable Energy (2024), DOI 10.1016/j.renene.2024.120549",
        "type": "Open-access research paper",
        "url": "https://www.sciencedirect.com/science/article/pii/S0960148124006141",
        "use": "Supports the need for site-specific joint wind/rain and material erosion-test data.",
        "limitation": "Paper results cannot be treated as a training dataset unless the underlying data are available and licensed for reuse.",
    },
    {
        "title": "Fast prediction of rain erosion in wind turbine blades using a data-based computational tool",
        "authors": "Journal of Hydrodynamics (2024), DOI 10.1007/s42241-024-0044-4",
        "type": "Model-method paper",
        "url": "https://pubs-en.cstam.org.cn/article/doi/10.1007/s42241-024-0044-4",
        "use": "Method reference for combining droplet-impact simulation data, surrogate models and fatigue-based erosion estimates.",
        "limitation": "A paper description is not a substitute for the authors' training data, material parameters or independent validation data.",
    },
]


def validation_readiness():
    return [
        ("Weather input integrity", "Can be checked now", "Units, timestamps, missing values, duplicates, provenance"),
        ("Site-level exposure plausibility", "Partly possible", "Compare against public LEE atlas where site coverage overlaps; not a direct validation of hourly damage"),
        ("Actual coating damage prediction", "Not yet possible", "Needs coating rain-erosion test data, blade inspection/damage ratings, or field observations"),
        ("Remaining useful life", "Not justified yet", "Needs calibrated damage model, material/geometry/operating data and independent validation"),
    ]
