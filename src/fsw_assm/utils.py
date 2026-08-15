import json
from .threshold_check import check_threshold


def load_json_file(filename):

    "Parse json files"
    if not isinstance(filename, str) or not filename.strip():
        raise ValueError("JSON filename must be a non-empty string")

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError as e:
        raise FileNotFoundError(f"JSON file not found: {filename}") from e
    except OSError as error:
        raise OSError(f"Unable to read JSON file '{filename}': {error}") from error


def get_parameter(packet, subsystem, parameter):
    "Parse data for telemetry parameter"
    if not isinstance(packet, dict):
        raise TypeError("Telemetry packet must be a dictionary")

    if not isinstance(subsystem, str) or not subsystem:
        raise ValueError("Subsystem name must be string")

    if not isinstance(parameter, str) or not parameter:
        raise ValueError("Parameter name must be string")

    subsystem_data = packet.get(subsystem, {})

    if parameter in subsystem_data:
        return subsystem_data[parameter]

    return None


def create_event(packet, rule, value, severity, action):

    if not isinstance(packet, dict):
        raise TypeError("Telemetry packet must be a dictionary")

    if "timestamp" not in packet:
        raise KeyError("Telemetry packet is missing required field: timestamp")

    return {
        "timestamp": packet["timestamp"],
        "subsystem": rule["subsystem"],
        "parameter": rule["parameter"],
        "value": value,
        "severity": severity,
        "recommended_action": action,
    }


def evaluate_packet(packet, rules):
    """Evaluate packets against the telemetry rules."""

    if not isinstance(packet, dict):
        raise TypeError("Each telemetry packet must be a dictionary")

    if not isinstance(rules, list):
        raise TypeError("Threshold rules must be provided as a list")

    events = []

    for rule in rules:
        value = get_parameter(
            packet,
            rule["subsystem"],
            rule["parameter"],
        )
        
        severity, action = check_threshold(value, rule)

        if severity is not None:
            event = create_event(
                packet,
                rule,
                value,
                severity,
                action,
            )
            events.append(event)

    return events


def monitor_telemetry(packets, rules):
    """House keeping monitor"""
    if not isinstance(packets, list):
        raise TypeError("Housekeeping telemetry must be a list of packets")

    if not isinstance(rules, list):
        raise TypeError("Threshold configuration must be a list")

    events = []

    # breakpoint()
    for index, packet in enumerate(packets):
        try:
            packet_events = evaluate_packet(packet, rules)
            events.extend(packet_events)
        # breakpoint()
        except (TypeError, ValueError, KeyError) as exrr:
            raise ValueError(
                f"Invalid telemetry packet at index {index}: {exrr}"
            ) from exrr

    return events
