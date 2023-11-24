import json
import csv
import logging
from log_config import setup_logging

setup_logging()


def export_to_json(metrics_data, output_file):
    """Export metrics data to a JSON file."""
    try:
        with open(output_file, 'w') as f:
            json.dump(metrics_data, f, indent=4)
        logging.info(f"Data successfully exported to JSON file: {output_file}")
    except Exception as e:
        logging.error(f"Error exporting data to JSON: {e}", exc_info=True)


def standardize_data_for_csv(metrics_data, headers_order):
    """Standardize metrics data for CSV export."""
    standardized_data = []
    for data in metrics_data:
        standardized_entry = {header: data.get(header, '') for header in headers_order}
        standardized_data.append(standardized_entry)
    return standardized_data


def export_to_csv(metrics_data, output_file):
    """Export metrics data to a CSV file."""
    headers_order = ["type", "name", "loc", "number_of_fields", "number_of_methods",
                     "wmc", "cyclomatic_complexity", "parameter_count", "lcom3"]

    standardized_data = standardize_data_for_csv(metrics_data, headers_order)

    try:
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers_order)
            writer.writeheader()
            writer.writerows(standardized_data)
        logging.info(f"Data successfully exported to CSV file: {output_file}")
    except Exception as e:
        logging.error(f"Error exporting data to CSV: {e}", exc_info=True)
