import argparse
import logging

parser = argparse.ArgumentParser()

parser.add_argument('--input_dir', required=True, help='')
parser.add_argument('--data_type', required=True, help='')
parser.add_argument('--for_what', default='extracting', help='')
parser.add_argument('--refining', type=bool, default=True, help = '')


if __name__ == '__main__':
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
