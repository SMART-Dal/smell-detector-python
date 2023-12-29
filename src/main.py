import argparse
import logging
import os
import re

from src.config_loader import load_config
from src.export.exporter import export_data, export_implementation_smells, export_design_smells
from src.log_config import setup_logging
from src.smells import get_detector
from src.smells.smell_detector import ImplementationSmellDetector, DesignSmellDetector
from src.sourcemodel.ast_parser import ASTParser
from src.sourcemodel.sm_project import SMProject


def get_root_path(input_path):
    """Get the root path of the input file or directory."""
    return input_path if os.path.isdir(input_path) else os.path.dirname(input_path)


def get_project_name(input_path):
    """Extract the project name from the input path."""
    return os.path.basename(input_path) if os.path.isdir(input_path) else \
        os.path.splitext(os.path.basename(input_path))[0]


config = load_config()
skip_directories = set(config['skip_directories']['names'])
skip_patterns = [re.compile(pattern) for pattern in config['skip_directories']['patterns']]


def should_skip(path):
    # Normalize and lower the path for comparison
    path = path.replace('\\', '/').lower()

    # Check if any part of the path is in the skip directories
    for part in path.split('/'):
        if part in skip_directories:
            return True

    # Check if the path matches any of the skip patterns
    for pattern in skip_patterns:
        if pattern.search(path):
            return True

    return False


def process_file(file_path, project, project_root, parser=None):
    """Process an individual Python file."""
    if should_skip(file_path):
        logging.info(f"Skipping file: {file_path}")
        return None

    parser = parser or ASTParser(project)
    try:
        return parser.parse(file_path, project_root)
    except Exception as e:
        logging.error(f"Error in processing file {file_path}: {e}", exc_info=True)
    return None


def process_directory(directory_path, project, project_root):
    modules = []

    for root, dirs, files in os.walk(directory_path):
        # Modify dirs in place to skip unwanted directories
        dirs[:] = [d for d in dirs if not should_skip(os.path.join(root, d))]

        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.py') and not should_skip(file_path):
                logging.info(f"Parsing file: {file_path}")
                print(f"Parsing file: {file_path}")
                module = process_file(file_path, project, project_root)
                if module:
                    modules.append(module)

    return modules


def analyze_modules(modules):
    """Analyze parsed modules to gather metrics and identify smells."""
    aggregated_metrics = {'module': [], 'class': [], 'method': [], 'function': []}
    for module in modules:
        logging.info(f"Analyzing module: {module.name}")
        print(f"Analyzing module: {module.name}")

        file_metrics = module.analyze()
        if file_metrics:
            aggregated_metrics['module'].append(file_metrics.get('module_metrics', {}))
            aggregated_metrics['class'].extend(file_metrics.get('class_metrics', []))
            aggregated_metrics['method'].extend(file_metrics.get('method_metrics', []))
            aggregated_metrics['function'].extend(file_metrics.get('function_metrics', []))
    return aggregated_metrics


def detect_smells(module, config):
    """Detect code smells within a module based on the provided configuration."""
    implementation_smells = []
    design_smells = []

    for smell_name, settings in config['Smells'].items():
        if not settings.get('enable', False):
            continue  # Skip if the smell is not enabled

        detector = get_detector(smell_name)
        if detector is None:
            logging.warning(f"Detector not found for smell: {smell_name}")
            continue
        try:
            smells = detector.detect(module, settings)
            if not isinstance(smells, list):
                logging.error(f"Expected list from detector but got {type(smells)} for {smell_name}")
                continue

            if isinstance(detector, ImplementationSmellDetector):
                implementation_smells.extend(smells)
            elif isinstance(detector, DesignSmellDetector):
                design_smells.extend(smells)

        except Exception as e:
            logging.error(f"Exception during detection of {smell_name}: {e}", exc_info=True)

    # Combine the collected smells into a single dictionary before returning
    detected_smells = {
        'implementation': implementation_smells,
        'design': design_smells
    }

    return detected_smells


def configure_environment(args):
    """Set up the environment before analysis starts, including logging and path checks."""
    log_directory = args.log_dir if args.log_dir else args.output_dir
    setup_logging(log_directory)

    if not os.path.exists(args.input):
        logging.error(f"Input path does not exist: {args.input}")
        return False  # Indicates that the environment setup was not successful

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir, exist_ok=True)

    return True  # Indicates successful environment setup


def perform_analysis(args):
    """Conduct the main analysis workflow."""
    try:
        project_root = get_root_path(args.input)
        project_name = get_project_name(args.input)
        project = SMProject(project_name)
        config = load_config(user_path=args.config)

        modules = process_directory(args.input, project, project_root) if os.path.isdir(args.input) else [
            process_file(args.input, project, project_root)]
        all_metrics = analyze_modules(modules)
        print("AST Parsing and Metrics calculation done!")

        all_smells = {'implementation': [], 'design': []}
        for module in modules:
            smells = detect_smells(module, config)
            for smell_type in all_smells:
                all_smells[smell_type].extend(smells[smell_type])
        print("Analysis Completed!!")

        return all_metrics, all_smells, project_name
    except Exception as e:
        logging.error(f"An error occurred during analysis: {e}")
        raise  # Re-raising the exception after logging


def export_results(all_metrics, all_smells, project_name, args):
    """Export the analysis results based on user-specified formats."""
    try:
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
    except Exception as e:
        logging.error(f"Failed to export results: {e}")
        raise  # Re-raising the exception after logging


def main(args):
    """Entry point of the application."""

    if configure_environment(args):
        try:
            all_metrics, all_smells, project_name = perform_analysis(args)
            export_results(all_metrics, all_smells, project_name, args)

        except Exception as e:
            logging.error(f"Analysis failed: {e}")
            print(f"Analysis failed. Check logs for details.")


if __name__ == "__main__":
    main()
