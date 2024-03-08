#!/bin/sh -l

# SPDX-FileCopyrightText: Copyright contributors to the Software Quality Assurance as a Service (SQAaaS) project.
# SPDX-FileContributor: Pablo Orviz <orviz@ifca.unican.es>
#
# SPDX-License-Identifier: GPL-3.0-only

python /usr/bin/step.py --name $1 \
                        --tool $2 \
                        --commands $3 \
                        --test-path $4
