import pytest
from fsw_assm.threshold_check import check_threshold

@pytest.fixture
def rule():
    return {
        "warning": 25,
        "error": 50,
        "critical": 55,
        "warning_action": "Check",
        "error_action": "Investigate",
        "critical_action": "Recover",
    }

def test_info_when_value_is_within_warning(rule):
    # rule = {
    #     "warning": 25,
    #     "error": 50,
    #     "critical": 55,
    #     "warning_action": "Check",
    #     "error_action": "Investigate",
    #     "critical_action": "Recover",
    # }
    assert check_threshold(20, rule) == ("INFO", "No action required.")


def test_warning_when_value_exceeds_warning(rule):
    # rule = {
    #     "warning": 25,
    #     "error": 50,
    #     "critical": 55,
    #     "warning_action": "Check",
    #     "error_action": "Investigate",
    #     "critical_action": "Recover",
    # }
    assert check_threshold(30, rule) == ("WARNING", "Check")


def test_error_when_value_exceeds_error(rule):
    # rule = {
    #     "warning": 25,
    #     "error": 50,
    #     "critical": 55,
    #     "warning_action": "Check",
    #     "error_action": "Investigate",
    #     "critical_action": "Recover",
    # }
    assert check_threshold(51, rule) == ("ERROR", "Investigate")


def test_critical_has_highest_priority(rule):
    # rule = {
    #     "warning": 25,
    #     "error": 50,
    #     "critical": 55,
    #     "warning_action": "Check",
    #     "error_action": "Investigate",
    #     "critical_action": "Recover",
    # }
    assert check_threshold(60, rule) == ("CRITICAL", "Recover")


def test_invalid_rule_type():
    with pytest.raises(TypeError, match="Threshold rule must be a dictionary"):
        check_threshold(20, [])


def test_missing_actions_are_reported_by_lookup():
    rule = {"warning": 25}
    with pytest.raises(KeyError):
        check_threshold(30, rule)
