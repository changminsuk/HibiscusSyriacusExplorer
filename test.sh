#!/usr/bin/env bash
set -eo pipefail

COLOR_GREEN=`tput setaf 2;`
COLOR_NC=`tput sgr0;` # No Color

echo "Starting black"
pipenv run black .
echo "OK"

echo "Starting isort"
pipenv run isort .
echo "OK"

#echo "Starting mypy"
#pipenv run mypy .
#echo "OK"

#echo "Sort pyproject.toml"
#poetry run toml-sort pyproject.toml --all --in-place
#echo "OK"

echo "Starting unittest"
pipenv run python -m unittest discover -s ./test -p '*_test.py' -v
echo "OK"

echo "${COLOR_GREEN}All tests passed successfully!${COLOR_NC}"
