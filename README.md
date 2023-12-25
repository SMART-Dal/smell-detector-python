
# Python Code Smell Detector

The PyCodeSmells Analysis Tool is a powerful static analysis tool designed to detect various code smells in Python codebases. It helps developers identify patterns that might be indicative of deeper problems, promoting better code quality, maintainability, and readability.

## Features

- **Wide Range of Smell Detection**: Detects both implementation and design smells, including complex methods, long parameter lists, and more.
- **Configurable Thresholds**: Customize the sensitivity of smell detection to fit the needs of your project.
- **Detailed Reporting**: Provides comprehensive reports detailing the type, location, and nature of each detected smell.
- **Multiple Export Formats**: Supports exporting results in JSON and CSV formats for easy integration with other tools and workflows.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Pip for installing dependencies

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/SMART-Dal/smell-detector-python.git
    ```

2. Navigate to the cloned directory:
    
    ```bash
    cd PyCodeSmells
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Usage

Run the tool using the command-line interface:

```bash
python main.py -i /path/to/your/python/project -o /path/to/output/directory -f json -c /path/to/your/config.json
```

- `-i, --input:` The input Python file or directory for analysis.
- `-o, --output_dir:` The output directory for the results.
- `-f, --format:` The output format (choices: 'json', 'csv').
- `-c, --config:` (Optional) Path to a custom configuration file.
- `-l, --log_dir:` (Optional) Directory to store log files.


### Configuration

You can customize the detection thresholds and other settings by providing a JSON configuration file. Refer to default_config.json 

Example:
```json
{
  "Smells": {
    "LongParameterList": {
      "enable": true,
      "threshold": 4
    },
    "LongIdentifier": {
      "enable": true,
      "threshold": 30
    },
    "LongMethod": {
      "enable": true,
      "threshold": 20
    },
    "ComplexMethod": {
      "enable": true,
      "threshold": 10
    }
  }
}
```




## Contact

- Harsh Vaghani
- Email: [harshvaghani00@gmail.com](harshvaghani00@gmail.com)

## Acknowledgements

- **Dr. Tushar Sharma**: For providing guidance and inspiration throughout the development of this tool. His expertise in the field of software engineering and code quality has been invaluable.
- **Python's `ast` Library**: Python's built-in `ast` library was instrumental in enabling code analysis and detection of code smells.
- **DesigniteJava**: [DesigniteJava](https://github.com/tushartushar/DesigniteJava) – A valuable resource that greatly influenced the development of this project, particularly in shaping the source model and enhancing design smell detection capabilities.

