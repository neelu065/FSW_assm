import argparse
from src.fsw_assm.main import hk_main


def main():
    parser = argparse.ArgumentParser(
        description="Housekeeping Monitor"
    )

    parser.add_argument(
        "--hk_telemetry",
        default='inputs/housekeeping_nominal.json',
        help="JSON housekeeping telemetry file"
    )

    parser.add_argument(
        "--config",
        default="inputs/define_threshold.json",
        help="Threshold configuration file"
    )

    parser.add_argument(
        "--output",
        default="event_log.json",
        help="Output event log"
    )

    args = parser.parse_args()

    hk_main(args)


if __name__ == "__main__":
    main()