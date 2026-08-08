import json
from .threshold_check import check_threshold


def load_json_file(filename):
    "Parse json files"
    with open(filename, "r") as file:
        return json.load(file)


def get_parameter(packet, subsystem, parameter):
    "Parse data for telemetry parameter"
    subsystem_data = packet.get(subsystem, {})

    if parameter in subsystem_data:
        return subsystem_data[parameter]

    return None


def create_event(packet, rule, value, severity, action):
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
    events = []
    # breakpoint()
    for packet in packets:
        packet_events = evaluate_packet(packet, rules)
        events.extend(packet_events)

    return events
