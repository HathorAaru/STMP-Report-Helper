from datetime import date

from report_helper.name_matching import display_name, name_key
from report_helper.report_builder import academic_year, percent_text, tracker_band


def test_display_name_accepts_attendance_format():
    assert display_name("Groves, Thea-Rose") == "Thea-Rose Groves"


def test_name_key_matches_both_formats():
    assert name_key("Groves, Thea-Rose") == name_key("Thea-Rose Groves")


def test_percent_text_formats_decimal_percentages():
    assert percent_text(1) == "100%"
    assert percent_text(0.952381) == "95.2%"


def test_academic_year_rolls_over_in_september():
    assert academic_year(date(2026, 7, 9)) == "2025 - 2026"
    assert academic_year(date(2026, 9, 1)) == "2026 - 2027"


def test_tracker_band_mapping():
    assert tracker_band("Ex -") == "at"
    assert tracker_band("Exc-") == "above"
    assert tracker_band("Em") == "working toward"
