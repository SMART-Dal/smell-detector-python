import csv
import json
import os
import logging


def export_metrics(data, output_dir, file_name, format, headers):
    try:
        if format == 'json':
            export_to_json(data, output_dir, file_name)
        elif format == 'csv':
            export_to_csv(data, headers, output_dir, file_name)
        logging.info(f"Exported {format.upper()} data to {file_name}.{format}")
    except Exception as e:
        logging.error(f"Failed to export data: {e}")


def export_to_json(data, output_dir, file_name):
    output_path = os.path.join(output_dir, f"{file_name}.json")
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def export_to_csv(data, headers, output_dir, file_name):
    output_path = os.path.join(output_dir, f"{file_name}.csv")
    with open(output_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        for row in data:
            if row is not None and isinstance(row, dict):
                writer.writerow(row)
