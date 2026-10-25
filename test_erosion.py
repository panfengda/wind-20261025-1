import pandas as pd
from pfd.erosion import add_exposure_proxy


def test_exposure_proxy_is_bounded_and_marked():
    df = pd.DataFrame({
        "wind_speed_100m": [0.0, 15.0, 30.0],
        "wind_gusts_10m": [0.0, 20.0, 40.0],
        "rain": [0.0, 5.0, 10.0],
    })
    out = add_exposure_proxy(df)
    assert out["lee_exposure_proxy_0_100"].between(0, 100).all()
    assert (out["model_status"] == "screening_proxy_not_validated").all()
