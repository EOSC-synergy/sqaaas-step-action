# SPDX-FileCopyrightText: Copyright contributors to the Software Quality Assurance as a Service (SQAaaS) project.
#
# SPDX-License-Identifier: GPL-3.0-only

import argparse
import logging
import requests


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('sqaaas-step-action')


TOOLING_URL = 'https://raw.githubusercontent.com/EOSC-synergy/sqaaas-tooling/release/1.8.0/tooling.json'


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

def get_tool_args(tool, lang):
    req = requests.get(
        url=TOOLING_URL
    )
    data = req.json()
    tool_args_before = data['tools'][lang][tool]['args']
    tool_args_after = {}
    for arg in tool_args_before:
        print(arg)
        arg_id = arg.pop('id')
        tool_args_after[arg_id] = tool_args_before

    return tool_args_after


if __name__ == "__main__":
    args = get_input_args()
    tool = args.tool

    if tool in ['commands']:
        lang = 'default'
    elif tool in ['pytest']:
        lang = 'Python'
    else:
        logger.error('Tool <%s> not supported' % tool)
        logger.debug(e)
        sys.exit(2)

    args_dict = get_tool_args(tool, lang)
    logger.debug('Format tool args as a dict: %s' % args_dict)
