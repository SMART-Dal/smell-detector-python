import argparse
import logging
import os

from config_loader import load_config
from export.exporter import export_data, export_implementation_smells, export_design_smells
from log_config import setup_logging
from smells import get_detector
from smells.smell_detector import ImplementationSmellDetector, DesignSmellDetector
from sourcemodel.ast_parser import ASTParser
from sourcemodel.sm_project import PyProject

setup_logging()


def get_root_path(input_path):
    if os.path.isdir(input_path):
        return input_path
    else:
        return os.path.dirname(input_path)


def get_project_name(input_path):
    return os.path.basename(input_path) \
        if os.path.isdir(input_path) \
        else os.path.splitext(os.path.basename(input_path))[0]


def process_file(file_path, project, project_root):
    try:
        parser = ASTParser(project)
        return parser.parse(file_path, project_root)  # Just parse and return the PyModule object
    except Exception as e:
        logging.error(f"Error in processing file {file_path}: {e}", exc_info=True)
    return None


def process_directory(directory_path, project, project_root):
    modules = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                logging.info(f"Parsing file: {file_path}")
                module = process_file(file_path, project, project_root)
                if module:
                    modules.append(module)
    return modules


def analyze_modules(modules):
    aggregated_metrics = {'module': [], 'class': [], 'method': [], 'function': []}
    for module in modules:
        logging.info(f"Analyzing module: {module.name}")
        file_metrics = module.analyze()
        if file_metrics:
            aggregated_metrics['module'].append(file_metrics.get('module_metrics', {}))
            aggregated_metrics['class'].extend(file_metrics.get('class_metrics', []))
            aggregated_metrics['method'].extend(file_metrics.get('method_metrics', []))
            aggregated_metrics['function'].extend(file_metrics.get('function_metrics', []))
    return aggregated_metrics


def detect_smells(module, config):
    detected_smells = {'implementation': [], 'design': []}
    for smell_name, settings in config['Smells'].items():
        if settings.get('enable', False):
            detector = get_detector(smell_name)
            if detector:
                smells = detector.detect(module, settings)
                if isinstance(detector, ImplementationSmellDetector):
                    detected_smells['implementation'].extend(smells)
                elif isinstance(detector, DesignSmellDetector):
                    detected_smells['design'].extend(smells)
    return detected_smells


def main():
    parser = argparse.ArgumentParser(description="PyCodeSmells Analysis Tool")
    parser.add_argument('-i', '--input', required=True, help="Input Python file or directory for analysis")
    parser.add_argument('-o', '--output_dir', required=True, help="Output directory for the results")
    parser.add_argument('-f', '--format', choices=['json', 'csv'], required=True, help="Output format")
    parser.add_argument('-c', '--config', help="Path to custom configuration file", default=None)
    args = parser.parse_args()

    if not os.path.exists(args.input):
        logging.error(f"Input path does not exist: {args.input}")
        return

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir, exist_ok=True)

    project_root = get_root_path(args.input)
    project_name = get_project_name(args.input)
    project = PyProject(project_name)

    modules = []
    if os.path.isdir(args.input):
        modules = process_directory(args.input, project, project_root)
    else:
        module = process_file(args.input, project, project_root)
        if module:
            modules.append(module)

    all_metrics = analyze_modules(modules)

    config = load_config(user_path=args.config)

    all_smells = {'implementation': [], 'design': []}

    for module in modules:
        smells = detect_smells(module, config)
        for smell_type in all_smells:
            all_smells[smell_type].extend(smells[smell_type])

    if all_metrics:

        export_data(all_metrics['module'], args.output_dir, f"{project_name}_module_metrics", args.format)
        export_data(all_metrics['class'], args.output_dir, f"{project_name}_class_metrics", args.format)
        export_data(all_metrics['method'], args.output_dir, f"{project_name}_method_metrics", args.format)
        export_data(all_metrics['function'], args.output_dir, f"{project_name}_function_metrics", args.format)

    if all_smells['implementation']:
        export_implementation_smells(all_smells['implementation'], args.output_dir, project_name, args.format)

    if all_smells['design']:
        export_design_smells(all_smells['design'], args.output_dir, project_name, args.format)

    else:
        logging.info("No data available for export.")


if __name__ == "__main__":
    main()
