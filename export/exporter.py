import csv
import json
import os
import logging


def export_data(data, output_dir, file_name, exp_format, headers=None):
    """Generic data export function."""
    try:
        if exp_format == 'json':
            export_to_json(data, output_dir, file_name)
        logging.info(f"Exported {exp_format.upper()} data to {file_name}.{exp_format}")
    except Exception as e:
        logging.error(f"Failed to export data: {e}")


def export_to_json(data, output_dir, file_name):
    output_path = os.path.join(output_dir, f"{file_name}.json")
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def export_implementation_smells(implementation_smells, output_dir, file_name, exp_format):
    headers = ['Type', 'Entity Name', 'Location', 'Details']
    export_data(implementation_smells, output_dir, f"{file_name}_implementation_smells", exp_format, headers)


def export_design_smells(design_smells, output_dir, file_name, exp_format):
    headers = ['Type', 'Entity Name', 'Location', 'Details']
    export_data(design_smells, output_dir, f"{file_name}_design_smells", exp_format, headers)
