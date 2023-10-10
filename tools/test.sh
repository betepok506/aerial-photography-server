#!/usr/bin/env bash

set -e
set -x
# Linux
#set PYTHONPATH=.

# Windows
export PYTHONPATH=.

pytest --cov=aerial_photography --cov-report=term-missing aerial_photography/tests "${@}"
