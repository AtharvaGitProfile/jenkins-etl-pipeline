import pandas as pd
from pipeline import transform


def test_drops_nulls():
    df = pd.DataFrame({
        "customer_name": ["Alice", None],
        "product": ["A", "B"],
        "quantity": [5, 3],
        "unit_price": [10.0, 20.0],
        "order_date": ["2025-01-01", "2025-01-02"],
        "region": ["East", "West"],
        "status": ["completed", "completed"],
    })
    assert len(transform(df)) == 1


def test_removes_bad_quantities():
    df = pd.DataFrame({
        "customer_name": ["A", "B", "C"],
        "product": ["X", "Y", "Z"],
        "quantity": [-1, 0, 5],
        "unit_price": [10.0, 10.0, 10.0],
        "order_date": ["2025-01-01"] * 3,
        "region": ["E"] * 3,
        "status": ["completed"] * 3,
    })
    result = transform(df)
    assert len(result) == 1
    assert result["quantity"].iloc[0] == 5


def test_normalizes_status():
    df = pd.DataFrame({
        "customer_name": ["A"],
        "product": ["X"],
        "quantity": [1],
        "unit_price": [10.0],
        "order_date": ["2025-01-01"],
        "region": ["E"],
        "status": [" COMPLETED "],
    })
    assert transform(df)["status"].iloc[0] == "completed"


def test_adds_total():
    df = pd.DataFrame({
        "customer_name": ["A"],
        "product": ["X"],
        "quantity": [3],
        "unit_price": [12.99],
        "order_date": ["2025-01-01"],
        "region": ["E"],
        "status": ["done"],
    })
    result = transform(df)
    assert result["total_price"].iloc[0] == 38.97
