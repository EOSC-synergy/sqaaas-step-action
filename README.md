<!--
SPDX-FileCopyrightText: Copyright contributors to the Software Quality Assurance as a Service (SQAaaS) project.
SPDX-FileContributor: Pablo Orviz <orviz@ifca.unican.es>

SPDX-License-Identifier: GPL-3.0-only
-->

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![REUSE status](https://api.reuse.software/badge/git.fsfe.org/reuse/api)](https://api.reuse.software/info/git.fsfe.org/reuse/api)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# SQAaaS Step action

This action generates a step definition to be used in a SQAaaS quality assessment. A step is composed of a tool execution, including its input arguments.

## Inputs

## `name`

**required** The name of the step.

## `tool`

**required** The name of the tool to be executed within the step. Tools currently supported are:
- `commands`: executes bash command/s
- Python's tools: `pytest` and `tox`

Note: support for new tools shall be aligned with the [SQAaaS tooling](https://github.com/eosc-synergy/sqaaas-tooling)

## `container`

**optional** The Docker image to run the step (defaults are taken from [SQAaaS tooling](https://github.com/eosc-synergy/sqaaas-tooling)).

## `commands`

A list of shell commands to run.

## `test_path`

**required for `pytest`** The location of the test cases.

## `tox_env`

**required for `tox``** The name for the tox environment to run.

## Outputs

## `step`

Definition of the step in JSON format (in accordance with SQAaaS API specification).

## Example usage
```yaml
uses: eosc-synergy/sqaaas-step-action@v1
with:
  name: pytest-step
  tool: pytest
  container: myownpytestimage:latest
  test-path: ./tests
```
