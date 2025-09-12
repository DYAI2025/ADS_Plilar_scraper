import importlib


def test_calc_revenue_day_and_month():
    gui = importlib.import_module("gui_app")
    monthly = gui.ADSPillarGUI.calc_revenue(100_000, 15.0, period="month")
    daily = gui.ADSPillarGUI.calc_revenue(100_000, 15.0, period="day")
    assert abs(monthly - 1500.0) < 1e-6
    assert abs(daily - (1500.0 / 30.0)) < 1e-6
