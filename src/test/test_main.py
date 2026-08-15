from types import SimpleNamespace
from unittest.mock import patch
from fsw_assm.main import hk_main


def test_hk_main_success():
    args = SimpleNamespace(
        hk_telemetry="telemetry.json",
        config="thresholds.json",
        output="events.json",
    )

    packets = [{
        "timestamp": "2026-08-15T12:00:00Z",
        "payload": {"temperature_C": 20},
    }]
    config = {"thresholds": []}

    with patch("fsw_assm.main.load_json_file", side_effect=[packets, config]), \
         patch("fsw_assm.main.monitor_telemetry", return_value=[]), \
         patch("fsw_assm.main.print_event_log") as print_log, \
         patch("fsw_assm.main.write_event_log") as write_log:

        result = hk_main(args)

    assert result is None
    print_log.assert_called_once_with([])
    write_log.assert_called_once_with([], "events.json")


def test_hk_main_missing_thresholds_returns_error():
    args = SimpleNamespace(
        hk_telemetry="telemetry.json",
        config="thresholds.json",
        output="events.json",
    )

    with patch("fsw_assm.main.load_json_file",
               side_effect=[[{"timestamp": "2026-08-15T12:00:00Z"}], {}]), \
         patch("builtins.print") as mock_print:

        result = hk_main(args)

    assert result == 1
    assert "Configuration is missing required field: thresholds" in str(
        mock_print.call_args
    )


def test_hk_main_invalid_config_type_returns_error():
    args = SimpleNamespace(
        hk_telemetry="telemetry.json",
        config="thresholds.json",
        output="events.json",
    )

    with patch("fsw_assm.main.load_json_file",
               side_effect=[[{"timestamp": "2026-08-15T12:00:00Z"}], []]), \
         patch("builtins.print") as mock_print:

        result = hk_main(args)

    assert result == 1
    assert "Configuration JSON must contain an object" in str(
        mock_print.call_args
    )


def test_hk_main_load_error_returns_error():
    args = SimpleNamespace(
        hk_telemetry="missing.json",
        config="thresholds.json",
        output="events.json",
    )

    with patch("fsw_assm.main.load_json_file",
               side_effect=FileNotFoundError("missing.json")), \
         patch("builtins.print") as mock_print:

        result = hk_main(args)

    assert result == 1
    assert "Housekeeping monitor error" in str(mock_print.call_args)
