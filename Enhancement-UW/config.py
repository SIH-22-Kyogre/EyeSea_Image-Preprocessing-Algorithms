import os

config = dict(
    BASE_PATH = os.path.abspath(os.path.join(os.path.realpath(__file__), os.path.pardir)),
    INPUT_DIRNAME = 'input',
    OUTPUT_DIRNAME = 'output'
)