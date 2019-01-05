import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from cloud_vision_samples.args import parse_plot_vertices
from cloud_vision_samples.joyson import extract


def main():
    # read stdin if sent
    data = None
    if not sys.stdin.isatty():
        data = sys.stdin.readlines()

    # parse arguments
    image_file, input_loc = parse_plot_vertices(data is None)

    print(image_file)
    print(input_loc)

    #
    json_data = None
    if input_loc is not None:
        with open(input_loc, 'r') as f:
            json_data = json.load(f)
    else:
        json_data = json.loads(''.join(data))

    #
    extracted = extract(json_data, ['vertices'], False)

    #
    plt_count = 0
    im = Image.open(image_file, 'r')
    plt.imshow(np.asarray(im))
    for box_vertices in extracted:
        box_x = []
        box_y = []
        for vertex in box_vertices:
            box_x.append(vertex['x'])
            box_y.append(vertex['y'])
        box_x.append(box_vertices[0]['x'])
        box_y.append(box_vertices[0]['y'])
        plt.plot(box_x, box_y, 'b-', linewidth=1)
        plt_count = plt_count + 1

    print('{} plots'.format(plt_count))
    plt.show()


if __name__ == '__main__':
    main()
