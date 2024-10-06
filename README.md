# Human Benchmark Automation

This project automates several tests from the [Human Benchmark](https://humanbenchmark.com/) website using Selenium. The automation script can perform tasks such as reaction time measurement, aim training, typing tests, memory tests (sequence, number, verbal, and visual), and more. Customizations like typing speed realism and stopping conditions for endless tests are also supported.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Running a Test](#running-a-test)
  - [Available Tests](#available-tests)
  - [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

## Features

- Automates the following Human Benchmark tests:
  - Reaction Time
  - Aim Trainer
  - Chimp Test
  - Typing Test
  - Sequence Memory
  - Number Memory
  - Verbal Memory
  - Visual Memory
- Simulates typing with either realistic or instant typing speed in the typing test.
- Allows for customization of the number of tries for tests like Reaction Time.
- Supports stopping conditions for endless tests like Sequence Memory with a custom stop key.
- Automatically handles start/continue buttons and removes ads when they obstruct the UI.
- Allows the user to run all the tests consecutively.

## Prerequisites

Before you can run the script, ensure you have the following installed:

- Python 3.x
- `selenium` package (`pip install selenium`)
- `keyboard` package (`pip install keyboard`)
- Chrome browser

## Installation

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/Devcom439/human-benchmark-bot
   cd human-benchmark-bot
   ```
2. Install the required dependencies:
   ```bash
   pip install selenium keyboard
   ```

## Usage

### Running a Test
To run any test, launch the script:
```bash
python HumanBenchmark_Bot.py
```
 
## Available Tests

You can run the following tests by calling their respective functions:

| Test Name       | Function       | Parameters                          |
|:-----------------|:----------------|:----------------------------------|
| Reaction Time   | `reaction_time`| `tries` (number of attempts)        |
| Aim Trainer     | `aim`          | N/A                                 |
| Chimp Test      | `chimp`        | N/A                                 |
| Typing Test     | `typing`       | `realism`                           |
| Sequence Memory | `sequence`     | `stop_key`                          |
| Number Memory   | `number`       | N/A                                 |
| Verbal Memory   | `verbal`       | `stop_key`                          |
| Visual Memory   | `visual`       | `stop_key`                          |

## Contributions

Contributions are welcome! If you have ideas for new features, optimizations, or improvements, feel free to fork the project and submit a pull request. You can also open issues for bug reports
