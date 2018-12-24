import json
import sys

from cloud_vision_samples.args import parse_structure_args
from cloud_vision_samples.joyson import extract


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
        extracted = extract(json_data, filters)
    else:
        raise ValueError('can not open json data')

    if len(extracted) == 1:
        print(extracted[0])
    else:
        print(extracted)


if __name__ == '__main__':
    main()
