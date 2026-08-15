import json
import pytest
from fsw_assm.write_log import write_event_log, print_event_log


def sample_events():
    return [{
        "timestamp": "2026-08-15T12:00:00Z",
        "subsystem": "payload",
        "parameter": "temperature_C",
        "value": 60.0,
        "severity": "CRITICAL",
        "recommended_action": "Recover",
    }]


def test_write_event_log_creates_json_file(tmp_path):
    write_event_log(sample_events(), "events.json", str(tmp_path))

    output = tmp_path / "events.json"
    assert output.exists()
    assert json.loads(output.read_text()) == sample_events()


def test_write_event_log_rejects_non_list():
    with pytest.raises(TypeError, match="events must be a list"):
        write_event_log({}, "events.json")


def test_write_event_log_rejects_empty_filename():
    with pytest.raises(ValueError, match="output filename must be a non-empty string"):
        write_event_log([], "")


def test_write_event_log_creates_output_directory(tmp_path):
    output_dir = tmp_path / "nested" / "logs"

    write_event_log([], "events.json", str(output_dir))
    assert (output_dir / "events.json").exists()


def test_print_event_log_rejects_non_list():
    with pytest.raises(TypeError, match="events must be a list"):
        print_event_log({})
