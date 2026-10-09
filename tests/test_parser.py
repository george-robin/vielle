import pytest
from src.input_parser import parse_progression
def test_lowercase():
    assert parse_progression("c g dm am") == ["C","G","Dm","Am"]
def test_comma_seperators():
    assert parse_progression(",c,d,g,am,") == ["C","D","G","Am"]
def test_dash_seperators():
    assert parse_progression("-c-d-g-am-") == ["C","D","G","Am"]
def test_mixed_seperators():
    assert parse_progression("-c-d,g,am-") == ["C","D","G","Am"]
def test_unsupported_chord():
    with pytest.raises(ValueError):
        parse_progression("c g dm am w")