# SPDX-FileCopyrightText: Copyright contributors to the Software Quality Assurance as a Service (SQAaaS) project.
#
# SPDX-License-Identifier: GPL-3.0-only

import argparse
import json
import logging
import os
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


def get_tooling_args(tool, lang):
    req = requests.get(
        url=TOOLING_URL
    )
    data = req.json()
    tooling_args_before = data['tools'][lang][tool]['args']
    tooling_args_after = {}
    for arg in tooling_args_before:
        arg_id = arg.pop('id')
        tooling_args_after[arg_id] = arg

    return tooling_args_after


def generate_step_json(args, tooling_args):
    tool_args = []
    for arg_k, arg_v in args.__dict__.items():
        if arg_k not in tooling_args.keys():
            logger.debug('Tool argument <%s> not in SQAaaS tooling' % arg_k)
        else:
            logger.debug(tooling_args[arg_k])
            tool_args.append({
                'id': arg_k,
                'type': tooling_args[arg_k]['type'],
                'value': arg_v
            })

    return {
        'name': args.tool,
        'args': tool_args
    }


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

    tooling_args = get_tooling_args(tool, lang)
    logger.debug('Format tool args as a dict: %s' % tooling_args)

    step_json = generate_step_json(args, tooling_args)
    logger.info('Step definition (JSON format): %s' % step_json)

    github_workspace = os.environ['GITHUB_WORKSPACE']
    if github_workspace:
        logger.debug('Found GitHub workspace: %s' % github_workspace)
    else:
        logger.error(
            'Cannot store step definition: GitHub workspace not defined '
            'through GITHUB_WORKSPACE variable'
        )
        sys.exit(3)
    step_file = '.'.join([args.name, 'json'])
    step_file_abspath = os.path.join(github_workspace, step_file)
    with open(step_file_abspath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logger.info(
        'Step definition (JSON format) dumped to file: %s' % step_file_abspath
    )
