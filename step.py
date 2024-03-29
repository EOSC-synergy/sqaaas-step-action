# SPDX-FileCopyrightText: Copyright contributors to the Software Quality Assurance as a Service (SQAaaS) project.
# SPDX-FileContributor: 2017-2024 Pablo Orviz <orviz@ifca.unican.es>
#
# SPDX-License-Identifier: GPL-3.0-only

import json
import logging
import os
import sys

import requests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("sqaaas-step-action")


TOOLING_URL = "https://raw.githubusercontent.com/EOSC-synergy/sqaaas-tooling/release/2.0.0/tooling.json"


def get_tool_data(tool, lang):
    """Return tool data from the SQAaaS tooling.

    Keyword arguments:
    tool -- the tool to get the tooling arguments from
    lang -- the language that the tool is mapped to
    """
    logger.debug("Using SQAaaS tooling metadata: %s" % TOOLING_URL)
    req = requests.get(url=TOOLING_URL)
    data = req.json()

    return data["tools"][lang][tool]


def get_tooling_args(args):
    """Format args indexed by tool id.

    Keyword arguments:
    args -- List of argument objects as defined in the SQAaaS tooling
    """
    tooling_args_before = args
    tooling_args_after = {}
    for arg in tooling_args_before:
        try:
            arg_id = arg.pop("id")
        except KeyError:
            logger.debug(
                "Ignoring argument <%s> as it does not provide the <id> property in SQAaaS tooling"
                % arg
            )
        else:
            tooling_args_after[arg_id] = arg

    return tooling_args_after


def get_envvar(envvar=None, prefix=None, ignore_envvars=[]):
    """Return a dictionary with the requested environment variables, either
    individually or through a matching prefix (following this order).

    Keyword arguments:
    envvar -- the environment variable to get
    prefix -- the prefix of the environment variable to match
    ignore_envvars -- a list of environment variables that will be ignored
    """
    envvars = {}
    try:
        if envvar:
            envvars = {envvar: os.environ[envvar]}
        elif prefix:
            envvars = dict(
                [
                    (key, os.environ[key])
                    for key in os.environ.keys()
                    if key.startswith(prefix)
                ]
            )
    except KeyError:
        logger.error("Could not find environment variable: %s" % envvar)

    if ignore_envvars:
        logger.debug("Request to ignore environment variables: %s" % ignore_envvars)
        for key in ignore_envvars:
            logger.debug("Ignoring environment variable <%s>" % key)
            try:
                del envvars[key]
            except KeyError as e:
                logger.error(str(e))
                logger.debug("Cannot ignore variable. Variable not set: %s" % key)
        logger.debug(
            "Resultant set of environment variables after ignoring "
            "process: %s" % envvars
        )

    return envvars


def generate_args_json(tooling_args):
    """Generate JSON payload corresponding to the given tool arguments.

    Keyword arguments:
    tooling_args -- a dict with the SQAaaS tooling data
    """
    input_envvars = get_envvar(
        prefix="INPUT", ignore_envvars=["INPUT_TOOL", "INPUT_NAME", "INPUT_CONTAINER"]
    )

    tooling_args_keys = tooling_args.keys()
    tool_args = []
    for arg_k, arg_v in input_envvars.items():
        action_arg = arg_k.replace("INPUT_", "").lower()
        if action_arg not in tooling_args_keys:
            logger.debug(
                "Tool argument <%s> not in SQAaaS tooling: "
                "(tooling args: %s)" % (action_arg, tooling_args_keys)
            )
        else:
            _arg = tooling_args[action_arg]
            logger.debug(
                "Found matching tooling argument <%s>: %s" % (action_arg, _arg)
            )
            # If arg has 'repeatable=true' it might contain YAML multiline string
            if _arg.get("repeatable", False):
                arg_v = arg_v.split("\n")
                arg_v = list(filter(None, arg_v))
                logger.debug(
                    "Action input <%s> contains multiline value: %s"
                    % (action_arg, arg_v)
                )
            # Compose tool_args
            _arg.update({"id": action_arg, "value": arg_v})
            tool_args.append(_arg)
            logger.debug("Tracking tooling argument: %s" % tool_args)

    return tool_args


def generate_container_json():
    """Generate JSON payload corresponding to a Docker definition."""
    payload = {}
    container = get_envvar(envvar="INPUT_CONTAINER").get("INPUT_CONTAINER", "")
    if container:
        payload = {"image": container}
        logger.debug("New 'docker' payload: %s" % payload)

    return payload


def generate_step_json(tool, lang):
    """Generate JSON payload corresponding to a step definition.

    Keyword arguments:
    tool -- the tool to get the tooling arguments from
    lang -- the language that the tool is mapped to
    """
    payload = get_tool_data(tool, lang)
    # container
    container_payload = generate_container_json()
    if container_payload:
        payload["docker"] = container_payload
    # args
    args = payload.get("args", [])
    if args:
        tooling_args = get_tooling_args(args)
        args = generate_args_json(tooling_args)
    payload["args"] = args
    payload.update(
        {
            "name": tool,
            "lang": lang,
        }
    )

    return payload


if __name__ == "__main__":
    action_tool = get_envvar(envvar="INPUT_TOOL")["INPUT_TOOL"]
    if action_tool in ["commands"]:
        lang = "default"
    elif action_tool in ["pytest", "tox"]:
        lang = "Python"
    else:
        logger.error("Tool <%s> not supported" % action_tool)
        sys.exit(2)

    step_json = generate_step_json(action_tool, lang)
    logger.info("Step definition (JSON format): %s" % step_json)

    github_workspace = get_envvar(envvar="GITHUB_WORKSPACE")["GITHUB_WORKSPACE"]
    if github_workspace:
        logger.debug("Found GitHub workspace: %s" % github_workspace)
    else:
        logger.error(
            "Cannot store step definition: GitHub workspace not defined "
            "through GITHUB_WORKSPACE variable"
        )
        sys.exit(3)
    action_name = get_envvar(envvar="INPUT_NAME")["INPUT_NAME"]
    step_file = ".".join([action_name, "json"])
    step_file_abspath = os.path.join(github_workspace, step_file)
    with open(step_file_abspath, "w", encoding="utf-8") as f:
        json.dump(step_json, f, ensure_ascii=False, indent=4)
    logger.info("Step definition (JSON format) dumped to file: %s" % step_file_abspath)
