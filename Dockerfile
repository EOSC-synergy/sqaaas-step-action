# SPDX-FileCopyrightText: Copyright contributors to the Software Quality Assurance as a Service (SQAaaS) project.
# SPDX-FileContributor: Pablo Orviz <orviz@ifca.unican.es>
#
# SPDX-License-Identifier: GPL-3.0-only

# Container image that runs your code
FROM python:3.12.0b3-alpine3.18

RUN pip install requests

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY step.py /usr/bin/step.py
COPY entrypoint.sh /entrypoint.sh

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]
