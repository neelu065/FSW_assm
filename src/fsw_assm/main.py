from .utils import load_json_file, monitor_telemetry
from .write_log import print_event_log, write_event_log

def hk_main(args):

    # Read both json files
    packets = load_json_file(args.hk_telemetry)
    config = load_json_file(args.config)

    # Parse the threshold
    rules = config["thresholds"]

    # Compare the telemetry data with threshold values
    events = monitor_telemetry(packets, rules)

    # print the log to the console and save it to json
    print_event_log(events)
    write_event_log(events, args.output)

    print(f"Event log written to: {args.output}")

    return None