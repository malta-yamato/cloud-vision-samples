import os
import argparse
from pathlib import Path
from cloud_vision_samples.detection_types import DETECTION_TYPES
from cloud_vision_samples.detection_types import DETECTION_TYPES_ABBR


def parse_request_vision_args():
    # parse arguments
    parser = argparse.ArgumentParser(description='request annotations to cloud vision API')
    parser.add_argument('input', help='image file to annotate detections')
    parser.add_argument('-k', '--key', help='specify using Cloud Vision API KEY')
    parser.add_argument('-t', '--types', nargs='+', default=None, help='select annotation type and count')
    args = parser.parse_args()

    # input
    input_loc = Path(args.input)
    if not input_loc.exists():
        raise ValueError('file not found')

    # key
    api_key = args.key
    if api_key is None:
        api_key = os.environ['GOOGLE_CLOUD_VISION_API_KEY']

    # types
    detection_types = {}
    arg_types = args.types
    if arg_types is not None and len(arg_types) > 0:
        for elm in arg_types:
            #
            spls = elm.split(':')
            if len(spls) == 0:
                raise ValueError('no types')
            if len(spls) > 2:
                raise ValueError('specify the type with [DETECTION_TYPE]:[COUNT]')
            #
            typ = str(spls[0])
            if typ not in DETECTION_TYPES:
                if typ in DETECTION_TYPES_ABBR:
                    typ = DETECTION_TYPES_ABBR[typ]
                else:
                    raise ValueError('unsupported detection type ... ' + typ)
            #
            cnt = 1
            if len(spls) == 2:
                cnt = int(spls[1])
            #
            detection_types.update([(typ, cnt)])
    else:
        detection_types.update(TYPE_UNSPECIFIED=1)

    return input_loc, api_key, detection_types,
