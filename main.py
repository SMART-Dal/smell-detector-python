import argparse
import logging
import os

from analyzer import analyze_code
from export.exporter import export_to_json, export_to_csv
from log_config import setup_logging

setup_logging()


def process_file(file_path):
    try:
        return analyze_code(file_path)
    except Exception as e:
        logging.error(f"Error in processing file {file_path}: {e}", exc_info=True)


def process_directory(directory_path):
    metrics_data = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                logging.info(f"Analyzing file: {file_path}")
                file_metrics = process_file(file_path)
                if file_metrics:
                    metrics_data.extend(file_metrics)
    return metrics_data


def main():
    setup_logging()

    parser = argparse.ArgumentParser(description="PyCodeSmells Analysis Tool")
    parser.add_argument('-i', '--input', required=True, help="Input Python file or directory for analysis")
    parser.add_argument('-o', '--output_dir', required=True, help="Output directory for the results")
    parser.add_argument('-f', '--format', choices=['json', 'csv'], required=True, help="Output format")
    args = parser.parse_args()

    # Ensure input path exists
    if not os.path.exists(args.input):
        logging.error(f"Input path does not exist: {args.input}")
        return

    # Ensure output directory exists
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir, exist_ok=True)

    output_path = os.path.join(args.output_dir, os.path.basename(args.input) + f"_metrics.{args.format}")

    if os.path.isdir(args.input):
        metrics_data = process_directory(args.input)
    else:
        metrics_data = process_file(args.input)

    if args.format == 'json':
        export_to_json(metrics_data, output_path)
    elif args.format == 'csv':
        export_to_csv(metrics_data, output_path)


if __name__ == "__main__":
    main()
