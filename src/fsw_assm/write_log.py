import json
import os


def write_event_log(events, filename, output_dir='outputs'):
    # breakpoint()
    
    if not isinstance(events, list):
        raise TypeError("events must be a list")

    if not isinstance(filename, str) or not filename.strip():
        raise ValueError("output filename must be a non-empty string")

    try:
        os.makedirs(output_dir, exist_ok=True)
        # filename = os.path.join(output_dir, "events.json")
        output_path = os.path.join(output_dir, filename)

        with open(output_path, "w") as file:
            json.dump(events, file, indent=2)

    except OSError as exrr:
        raise OSError(f"Unable to write event log '{output_path}': {exrr}") from exrr


def print_event_log(events):
    """Print log to console"""
    if not isinstance(events, list):
        raise TypeError("events must be a list")
    
    print(
        f"{'|Timestamp|':<25} |"
        f"{'Subsystem|':<20} |"
        f"{'Parameter|':<20} |"
        f"{'Severity|':<25} |"
        f"Action|"
    )

    print("=" * 120)
    # breakpoint()
    for event in events:
        print(
            f"{event['timestamp']:<25} "
            f"{event['subsystem']:<20} "
            f"{event['parameter']:<25} "
            f"{event['severity']:<10} "
            f"{event['recommended_action']}"
        )
