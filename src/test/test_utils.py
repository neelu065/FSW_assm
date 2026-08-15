import pytest
from fsw_assm.utils import (
    load_json_file,
    get_parameter,
    create_event,
    evaluate_packet,
    monitor_telemetry,
)


@pytest.fixture
def rule():
    return {
        "subsystem": "payload",
        "parameter": "temperature_C",
        "warning": 25,
        "error": 50,
        "critical": 55,
        "warning_action": "Check",
        "error_action": "Investigate",
        "critical_action": "Recover",
    }


def test_load_json_file(tmp_path):
    path = tmp_path / "telemetry.json"
    path.write_text('{"message": "testing file"}')

    assert load_json_file(str(path)) == {
        "message": "testing file"
    }


def test_load_json_file_empty_filename():
    with pytest.raises(ValueError, match="JSON filename must be a non-empty string"):
        load_json_file("")


def test_load_json_file_missing_file():
    with pytest.raises(FileNotFoundError, match="JSON file not found"):
        load_json_file("does_not_exist.json")


def test_get_parameter_existing():
    packet = {"payload": {"temperature_C": 40.0}}
    assert get_parameter(packet, "payload", "temperature_C") == 40.0


def test_get_parameter_missing():
    packet = {"payload": {"temperature_C": 40.0}}
    assert get_parameter(packet, "payload", "cpu_usage_percent") is None


def test_get_parameter_invalid_packet():
    with pytest.raises(TypeError, match="Telemetry packet must be a dictionary"):
        get_parameter([], "payload", "temperature_C")


def test_create_event():
    packet = {"timestamp": "2026-08-15T12:00:00Z"}
    rule = {"subsystem": "payload", "parameter": "temperature_C"}

    event = create_event(packet, rule, 60.0, "CRITICAL", "Recover")

    assert event == {
        "timestamp": "2026-08-15T12:00:00Z",
        "subsystem": "payload",
        "parameter": "temperature_C",
        "value": 60.0,
        "severity": "CRITICAL",
        "recommended_action": "Recover",
    }


def test_create_event_missing_timestamp():
    with pytest.raises(KeyError, match="timestamp"):
        create_event({}, {"subsystem": "payload", "parameter": "temperature_C"},
                     60.0, "CRITICAL", "Recover")


def test_evaluate_packet_generates_event(rule):
    packet = {
        "timestamp": "2026-08-15T12:00:00Z",
        "payload": {"temperature_C": 60},
    }

    events = evaluate_packet(packet, [rule])

    assert len(events) == 1
    assert events[0]["severity"] == "CRITICAL"
    assert events[0]["value"] == 60


def test_evaluate_packet_invalid_packet(rule):
    with pytest.raises(TypeError, match="Each telemetry packet must be a dictionary"):
        evaluate_packet([], [rule])


def test_evaluate_packet_invalid_rules(rule):
    packet = {"timestamp": "2026-08-15T12:00:00Z"}

    with pytest.raises(TypeError, match="Threshold rules must be provided as a list"):
        evaluate_packet(packet, {})


def test_monitor_telemetry_multiple_packets(rule):
    packets = [
        {
            "timestamp": "2026-08-15T12:00:00Z",
            "payload": {"temperature_C": 60},
        },
        {
            "timestamp": "2026-08-15T12:01:00Z",
            "payload": {"temperature_C": 30},
        },
    ]

    events = monitor_telemetry(packets, [rule])

    assert len(events) == 2
    assert [event["severity"] for event in events] == ["CRITICAL", "WARNING"]


def test_monitor_telemetry_invalid_packet_is_wrapped(rule):
    packets = ["not a packet"]

    with pytest.raises(ValueError, match="Invalid telemetry packet at index 0"):
        monitor_telemetry(packets, [rule])
