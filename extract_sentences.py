import os
import argparse
import logging
from multiprocessing import cpu_count
from lib.load_data import korquad1_sentences, korquad2_sentences, kowiki_sentences, namuwiki_sentences

parser = argparse.ArgumentParser()

parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', type=str, required=True, help='Directory for the input data.')
parser.add_argument('--output_dir', type=str, required=True, help='Directory for the output data.')
parser.add_argument('--data_type', type=str, required=True, help='Type of input data("korquad2-sens-kor","kowiki-sens-kor" supported).')
parser.add_argument('--num_cores', type=int, default=None, metavar='N', help='The number of cpu cores.')
parser.add_argument('--prefix', type=str, default='', help='Prefix for the outputs.')


def save_sentences(path, contents):
    with open(path, 'w', encoding='utf-8') as w:
        w.write(contents)


if __name__ == '__main__':
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    num_cores = args.num_cores if args.num_cores else cpu_count()
    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)
        logging.info(f'directory is created in {args.output_dir}')

    logging.info(f'the number of cpu cores: {num_cores}')
    input_files = [os.path.join(args.input_dir, f) for f in os.listdir(args.input_dir)]
    output_files = [os.path.join(args.output_dir, args.prefix + '.'.join(os.path.basename(i).split('.')[:-1]))+'.txt' for i in input_files]

    for input_file, output_file in zip(input_files, output_files):
        logging.info(f'** Input file:{input_file}')
        if args.data_type == 'korquad1-sens-kor':
            sentences = korquad1_sentences(path=input_file, num_cores=num_cores, mode=args.data_type)
        elif args.data_type == 'korquad2-sens-kor':
            sentences = korquad2_sentences(path=input_file, num_cores=num_cores, mode=args.data_type)
        elif args.data_type =='namuwiki-sens-kor':
            sentences = namuwiki_sentences(path=input_file, num_cores=num_cores, mode=args.data_type)
        elif args.data_type == 'kowiki-sens-kor':
            logging.info(f'** The multiprocessing is not supported.')
            sentences = kowiki_sentences(path=input_file, mode=args.data_type) # kowiki_sentences has no attribute for multiprocessing.
        else:
            raise KeyError('Not supported!')

        sentences = '\n'.join(sentences)
        save_sentences(output_file, sentences)
        logging.info(f"Saved Successfully in {output_file}")
