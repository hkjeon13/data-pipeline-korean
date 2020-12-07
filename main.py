import argparse
import logging

parser = argparse.ArgumentParser()

parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', type=str, required=True, help='Directory for the input data.')
parser.add_argument('--output_dir', type=str, required=True, help='Directory for the output data.')


if __name__ == '__main__':
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
