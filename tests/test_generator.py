import pytest
from src.generator import generate_progression_tab

EXPECTED_CD = "\n".join ([
    "   C           D           ",
    "e|-0-----------2----------|",
    "B|-1-----------3----------|",
    "G|-0-----------2----------|",
    "D|-2-----------0----------|",
    "A|-3-----------X----------|",
    "E|-X-----------X----------|",
])

def test_c_d_exact_output ():
    assert generate_progression_tab(["C","D"]) == EXPECTED_CD

def test_unknown_chord():
    with pytest.raises(ValueError):
        generate_progression_tab(["C", "H"])

def test_too_short():
    with pytest.raises(ValueError):
        generate_progression_tab(["C"])