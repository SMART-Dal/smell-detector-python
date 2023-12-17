import csv
import json
import logging
import os


def export_data(data, output_dir, file_name, exp_format):
    """Generic data export function."""
    try:
        if exp_format == 'json':
            export_to_json(data, output_dir, file_name)
        elif exp_format == 'csv':
            export_to_csv(data, output_dir, file_name)
        logging.info(f"Successfully exported {exp_format.upper()} data to {file_name}.{exp_format}")
    except Exception as e:
        logging.error(f"Failed to export data to {file_name}.{exp_format}: {e}")


def export_to_csv(data, output_dir, file_name):
    if not data:
        logging.error(f"No data provided to export for {file_name}.csv")
        return

    output_path = os.path.join(output_dir, f"{file_name}.csv")
    try:
        with open(output_path, 'w', newline='') as csv_file:
            # Dynamically determine headers from the first row of the data
            headers = data[0].keys()
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            for row in data:
                if not isinstance(row, dict):
                    logging.error(f"Invalid row format in data for {file_name}.csv: {row}")
                    continue
                writer.writerow(row)
        logging.info(f"CSV data successfully exported to {output_path}")
    except IOError as e:
        logging.error(f"IOError while writing CSV to {output_path}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error while writing CSV to {output_path}: {e}")


def export_to_json(data, output_dir, file_name):
    output_path = os.path.join(output_dir, f"{file_name}.json")
    try:
        with open(output_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        logging.info(f"JSON data successfully exported to {output_path}")
    except IOError as e:
        logging.error(f"IOError while writing JSON to {output_path}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error while writing JSON to {output_path}: {e}")


def export_implementation_smells(implementation_smells, output_dir, file_name, exp_format):
    export_data(implementation_smells, output_dir, f"{file_name}_implementation_smells", exp_format)


def export_design_smells(design_smells, output_dir, file_name, exp_format):
    export_data(design_smells, output_dir, f"{file_name}_design_smells", exp_format)
