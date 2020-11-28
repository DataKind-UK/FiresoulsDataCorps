
printf "\n###### 1. Running Pytest Tests ######\n"
pytest --cov=src tests

printf "\n###### 2. Running MyPy typing checks ######\n"
mypy . --ignore-missing-imports

printf "\n###### 3. Running black code cleanup ######\n"
black . 