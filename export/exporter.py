import csv
import json


def export_class_metrics(data, output_dir, file_name):
    headers = ['Name', 'LOC', 'WMC', 'LCOM', 'Fan-in', 'Fan-out', 'NOM', 'NOF']
    export_to_csv(data, headers, output_dir, f"{file_name}_class_metrics")


def export_method_metrics(data, output_dir, file_name):
    headers = ['Name', 'LOC', 'CC', 'PC']
    export_to_csv(data, headers, output_dir, f"{file_name}_method_metrics")


def export_module_metrics(data, output_dir, file_name):
    headers = ['Name', 'LOC', 'WMC', 'LCOM', 'Fan-in', 'Fan-out', 'NOM', 'NOF']
    export_to_csv(data, headers, output_dir, f"{file_name}_module_metrics")


def export_to_csv(data, headers, output_dir, file_name):
    output_path = f"{output_dir}/{file_name}.csv"
    with open(output_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def export_to_json(data, output_dir, file_name):
    output_path = f"{output_dir}/{file_name}.json"
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
