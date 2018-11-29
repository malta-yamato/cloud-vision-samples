from cloud_vision_samples.args import parse_request_vision_args
from cloud_vision_samples.vision_api import create_single_post, request_post


def main():
    # parse arguments
    input_loc, api_key, detection_types, = parse_request_vision_args()

    # print(input_loc)
    # print(detection_types)
    # print(vision_url(api_key))
    # print(create_post_single(input_loc, detection_types))

    response = request_post(api_key, create_single_post(input_loc, detection_types))
    print(response.text)


if __name__ == '__main__':
    main()
