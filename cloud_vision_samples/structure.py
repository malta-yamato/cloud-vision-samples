import json
import sys

from cloud_vision_samples.args import parse_structure_args
from cloud_vision_samples.joyson import structure


def main():
    # read stdin if sent
    data = None
    if not sys.stdin.isatty():
        data = sys.stdin.readlines()

    # parse arguments
    input_loc, filters = parse_structure_args(data is None)
    # print(filters)
    filters.reverse()

    #
    json_data = None
    if input_loc is not None:
        with open(input_loc, 'r') as f:
            json_data = json.load(f)
    else:
        json_data = json.loads(''.join(data))

    #
    if json_data is not None:
        structure(json_data, filters)
    else:
        raise ValueError('can not open json data')


if __name__ == '__main__':
    main()
