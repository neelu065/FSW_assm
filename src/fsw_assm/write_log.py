import json
import os


def write_event_log(events, filename, output_dir='outputs'):
    # breakpoint()
    os.makedirs(output_dir, exist_ok=True)
    # filename = os.path.join(output_dir, "events.json")

    with open(os.path.join(output_dir, filename), "w") as file:
        json.dump(events, file, indent=2)


def print_event_log(events):
    """Print log to console"""

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
