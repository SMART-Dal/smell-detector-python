
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
  cd smell-detector-python
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


### Code Smells Explanation

The PyCodeSmells Analysis Tool can detect a wide range of code smells. Below is a description of each smell and the configurable parameters available to tailor the tool to your needs.


#### Hierarchy Smells
- **BrokenHierarchy**: Detects when a subclass does not properly utilize inheritance from its superclass.
  - `enable`: Turn detection on (true) or off (false).
- **DeepHierarchy**: Identifies class hierarchies that are excessively deep, indicating overly complex inheritance structures.
  - `enable`: Turn detection on or off.
  - `max_depth`: The maximum depth of a class hierarchy before it's considered too deep.
- **MissingHierarchy**: Flags instances where a hierarchy should be present but is not, often indicated by a set of classes with similar methods and attributes.
  - `enable`: Turn detection on or off.
  - `max_branches`: The maximum number of branches a hierarchy can have before it's considered missing.
- **MultipathHierarchy**: Detects hierarchies where a subclass inherits from multiple parent classes, potentially leading to complexity and ambiguity.
  - `enable`: Turn detection on or off.
- **RebelliousHierarchy**: Flags subclasses that do not properly fit into the hierarchy, often overriding and not utilizing inherited functionality.
  - `enable`: Turn detection on or off.
- **WideHierarchy**: Identifies hierarchies that are excessively wide with too many subclasses deriving from a single parent class.
  - `enable`: Turn detection on or off.
  - `threshold`: The maximum number of subclasses a single class can have before the hierarchy is considered too wide.

#### Modularization Smells
- **BrokenModularization**: Flags modules that have excessive interdependencies, indicating poor separation of concerns.
  - `enable`: Turn detection on or off.
  - `x_references`: The maximum number of external references a module can have before it's considered "broken" in terms of modularization.
- **HubLikeModularization**: Detects modules that act as central hubs, with an excessive number of incoming and outgoing dependencies.
  - `enable`: Turn detection on or off.
  - `max_fan_in`: The maximum allowable fan-in (incoming dependencies).
  - `max_fan_out`: The maximum allowable fan-out (outgoing dependencies).
- **InsufficientModularization**: Identifies modules that are too large or doing too much, suggesting they should be broken down into smaller, more focused units.
  - `enable`: Turn detection on or off.
  - `max_loc`: The maximum Lines Of Code in a module.
  - `max_nom`: The maximum number of methods.
  - `max_nopm`: The maximum number of public methods per module.
  - `max_wmc`: The maximum Weighted Methods per Class.

#### Encapsulation Smells
- **DeficientEncapsulation**: Flags when the internal workings of a class or module are too exposed, violating the principle of encapsulation.
  - `enable`: Turn detection on or off.
- **UnexploitedEncapsulation**: Detects when the potential benefits of encapsulation are not being fully utilized within the system's design.
  - `enable`: Turn detection on or off.

#### Abstraction Smells
- **ImperativeAbstraction**: Identifies abstractions that contain too many imperative style instructions, suggesting a procedural rather than an object-oriented approach.
  - `enable`: Turn detection on or off.
  - `max_line`: The maximum number of lines allowed in an abstraction.
  - `threshold`: The maximum allowable imperativeness in an abstraction.
- **MultifacetedAbstraction**: Flags abstractions that are trying to do too much, indicated by a high lack of cohesion.
  - `enable`: Turn detection on or off.
  - `max_lcom4`: The maximum Lack of Cohesion in Methods (LCOM4) score before an abstraction is considered multifaceted.
  - `min_methods`: The minimum number of methods an abstraction must have to be considered for this smell.
- **UnnecessaryAbstraction**: Detects when an abstraction is not providing sufficient value, possibly indicating it should be refactored or removed.
  - `enable`: Turn detection on or off.
  - `max_fields`: The maximum number of fields an abstraction can have before it's considered unnecessary.
  - `max_methods`: The maximum number of methods an abstraction can have before it's considered unnecessary.
  - `min_method_loc`: The minimum number of lines of code a method should have to avoid being considered an unnecessary abstraction.
- **UnutilizedAbstraction**: Identifies abstractions that are not being used to their full potential, often indicating dead or redundant code.
  - `enable`: Turn detection on or off.

#### Implementation Code Smells
- **ComplexConditional**: Flags overly complex conditional structures, which can make code difficult to read and maintain.
  - `enable`: Turn detection on or off.
  - `threshold`: The maximum allowable complexity in a conditional statement.
- **ComplexMethod**: Detects methods that are too complex, making them hard to understand and maintain.
  - `enable`: Turn detection on or off.
  - `threshold`: The maximum complexity score a method can have.
- **EmptyCatchBlock**: Identifies catch blocks that are empty, potentially swallowing errors and exceptions silently.
  - `enable`: Turn detection on or off.
- **LongIdentifier**: Flags identifiers that are excessively long, potentially making code harder to read.
  - `enable`: Turn detection on or off.
  - `threshold`: The maximum length of an identifier.
- **LongMethod**: Detects methods that are too long, indicating they might be doing too much and should be refactored.
  - `enable`: Turn detection on or off.
  - `threshold`: The maximum number of lines a method can have.
- **LongParameterList**: Identifies methods with too many parameters, which can make them challenging to understand and use.
  - `enable`: Turn detection on or off.
  - `threshold`: The maximum number of parameters a method can have.
- **LongStatement**: Flags single statements that are too long, suggesting they should be broken down for better readability.
  - `enable`: Turn detection on or off.
  - `threshold`: The maximum length of a single statement.
- **MagicNumber**: Detects the use of 'magic numbers', or hard-coded values, which can make code less understandable and maintainable.
  - `enable`: Turn detection on or off.
- **MissingDefault**: Flags switch statements without a default case, potentially leaving out important handling for unexpected cases.
  - `enable`: Turn detection on or off.


#### Notes:

- The `enable` key for each smell is a boolean value (`true` or `false`) indicating whether that particular smell should be checked during analysis.
- The `threshold` and other numerical parameters are flexible and should be adjusted based on the size and complexity of your codebase, as well as your team's specific coding standards and practices.
- Some smells, like `EmptyCatchBlock`, do not have configurable thresholds as they are either present or not, and thus are only toggleable.
- Adjusting these settings allows you to fine-tune the sensitivity of the smell detection and focus on the most pertinent issues for your project.


Customize the detection settings for these smells in your configuration JSON file to ensure the analysis is most effective for your specific codebase and standards.


## Contact

- Harsh Vaghani | [Email](mailto:harshvaghani00@gmail.com) | [LinkedIn](https://www.linkedin.com/in/harsh-vaghani/)


## Acknowledgements

- **Dr. Tushar Sharma**: For providing guidance and inspiration throughout the development of this tool. His expertise in the field of software engineering and code quality has been invaluable.
- **Python's `ast` Library**: Python's built-in `ast` library was instrumental in enabling code analysis and detection of code smells.
- **DesigniteJava**: [DesigniteJava](https://github.com/tushartushar/DesigniteJava) – A valuable resource that greatly influenced the development of this project, particularly in shaping the source model and enhancing design smell detection capabilities.

