<!--
SPDX-FileCopyrightText: Copyright contributors to the Software Quality Assurance as a Service (SQAaaS) project.

SPDX-License-Identifier: GPL-3.0-only
-->

# SQAaaS Step action

This action generates a step definition to be used in a SQAaaS quality assessment. A step is composed of a tool execution, including its input arguments.

## Inputs

## `name`

**required** The name of the step.

## `tool`

**required** The name of the tool to be executed within the step. This tool shall be supported in the [SQAaaS tooling](https://github.com/eosc-synergy/sqaaas-tooling)

## `container`

**optional** The Docker image to run the step (defaults are taken from [SQAaaS tooling](https://github.com/eosc-synergy/sqaaas-tooling)).

## `commands`

A list of shell commands to run.

## `test-path`

**required for `pytest`** The location of the test cases.

## Outputs

## `step`

Definition of the step in JSON format (in accordance with SQAaaS API specification).

## Example usage
```yaml
uses: actions/sqaaas-step@v1
with:
  name: pytest-step
  tool: pytest
  container: myownpytestimage:latest
  test-path: ./tests
```
