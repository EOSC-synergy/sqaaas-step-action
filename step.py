# SPDX-FileCopyrightText: Copyright contributors to the Software Quality Assurance as a Service (SQAaaS) project.
#
# SPDX-License-Identifier: GPL-3.0-only

import argparse
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('sqaaas-step-action')


def get_input_args():
    parser = argparse.ArgumentParser(description=(
        'SQAaaS step definition in a GitHub workflow.'
    ))
    parser.add_argument(
        '--name',
        metavar='NAME',
        type=str,
        help='Name of the step'
    )
    parser.add_argument(
        '--tool',
        metavar='TOOL',
        type=str,
        help='Name of the tool to be executed within the step'
    )
    parser.add_argument(
        '--commands',
        metavar='LIST',
        type=str,
        help='List of shell commands to execute'
    )
    parser.add_argument(
        '--test-path',
        metavar='PATH',
        type=str,
        help='Path to test cases'
    )

    return parser.parse_args()


def generate_step_json(tool, **kwargs):
    # args
    args_list = [for k,v in kwargs.items()]


    return {
        'name': tool,
    }


if __name__ == "__main__":
    args = get_input_args()
    tool = args.tool

    if tool in ['commands']:
        pass
    elif tool in ['pytest']:
        pass
    else:
        logger.error('Tool <%s> not supported' % tool)
        logger.debug(e)
