#! /usr/bin/env bash
set -e
#set PYTHONPATH=.
export PYTHONPATH=.

python aerial_photography/tests_pre_start.py

bash aerial_photography/scripts/test.sh # "$@"