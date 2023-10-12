#!/usr/bin/env bash

set -e
set -x

#pytest --cov=aerial_photography --cov-report=term-missing aerial_photography/tests "${@}"
pytest  aerial_photography/tests  --asyncio-mode=strict # "${@}"