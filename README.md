# Word Prediction

## Requirements
- Linux platform
- [poetry](https://python-poetry.org/) for packaging and dependency management.

## Installation
On project root:
1. Install project dependencies: `poetry install`
2. Download the corpus data: `poetry run download-data`
3. Download pre-trained models: `poetry run download-models`

## Run/Test
`poetry run pytest -s`
