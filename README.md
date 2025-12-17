# SSHMASS

SSHMASS is a Python-based tool designed to manage, consult, and execute commands on multiple Linux hosts over SSH.

It takes as input an .xlsx file containing:

  - hosts (IP addresses or hostnames)
  - commands or scripts to execute

It then generates a second .xlsx file used for reporting purposes.

Some may argue that Ansible already provides similar features; however, SSHMASS focuses on simplicity, portability, and lightweight reporting without requiring an agent or complex configuration.

### Requirements

- Python 3
- Python libraries:
  - paramiko
  - pandas
- Currently tested on:
  - Powershell 
  - Visual Studio Code
  - VSCodium

Minor adaptations may be required for Linux or WSL environments.

### How it works 

- The project is currently composed of three Python files:
  - varfile.py
  - functions.py
  - main.py
(this structure may evolve over time)

- The script automatically loads all .xlsx files located in a dedicated directory and converts them into pandas DataFrames.
- The DataFrame is dynamically enriched using menu-based input, then parsed to execute SSH commands on each target host.
- Command execution results are exported to results.xlsx.

- The current reporting focuses on:
  - binary version checks
  - conditional formatting (color highlighting)

This was initially developed to quickly verify software versions prior to patching, especially in response to 0-day vulnerability announcements.
