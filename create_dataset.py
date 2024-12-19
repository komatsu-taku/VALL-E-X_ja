import argparse
from customs.make_custom_dataset import create_dataset

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', '-i', type=str)

    return parser.parse_args()


def main(args: argparse.Namespace):
    data_dir = args.input
    create_dataset(data_dir, dataloader_process_only=True)


if __name__ == "__main__":
    main(parse_args())