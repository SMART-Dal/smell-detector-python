import argparse
import logging
import os

from export.exporter import export_class_metrics, export_module_metrics, export_method_metrics, export_to_json
from log_config import setup_logging
from sourcemodel.ast_parser import ASTParser
from sourcemodel.sm_project import PyProject

setup_logging()


def get_project_name(input_path):
    return os.path.basename(input_path) \
        if os.path.isdir(input_path) \
        else os.path.splitext(os.path.basename(input_path))[0]


def process_file(file_path, project):
    try:
        parser = ASTParser(project)
        module = parser.parse_file(file_path)
        return module.analyze()
    except Exception as e:
        logging.error(f"Error in processing file {file_path}: {e}", exc_info=True)
    return None


def process_directory(directory_path, project):
    aggregated_metrics = {'class': [], 'method': [], 'module': []}
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                logging.info(f"Analyzing file: {file_path}")
                file_metrics = process_file(file_path, project)
                if file_metrics:
                    aggregated_metrics['class'].extend(file_metrics.get('class_metrics', []))
                    aggregated_metrics['method'].extend(file_metrics.get('method_metrics', []))
                    aggregated_metrics['module'].append(file_metrics.get('module_metrics', {}))
    return aggregated_metrics


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

    project_name = get_project_name(args.input)
    project = PyProject(project_name)

    if os.path.isdir(args.input):
        all_metrics = process_directory(args.input, project)
    else:
        all_metrics = process_file(args.input, project)

        # Exporting results
    if args.format == 'csv':
        export_class_metrics(all_metrics['class'], args.output_dir, project_name)
        export_method_metrics(all_metrics['method'], args.output_dir, project_name)
        export_module_metrics(all_metrics['module'], args.output_dir, project_name)
    elif args.format == 'json':
        export_to_json(all_metrics, args.output_dir, project_name)


if __name__ == "__main__":
    main()
