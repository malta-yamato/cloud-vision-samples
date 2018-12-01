import base64
import json
import requests


def vision_url(api_key):
    if api_key is None:
        raise ValueError('api_key is NONE')
    return 'https://vision.googleapis.com/v1/images:annotate?key=' + api_key


def request_post(api_key, data):
    return requests.post(url=vision_url(api_key), data=data, headers={'Content-Type': 'application/json'})


def configure_item(image_path, types):
    # features
    features = []
    for typ, cnt in types.items():
        # print(typ, cnt)
        features.append({
            'type': typ,
            'maxResults': int(cnt),
        })
    # image
    with open(image_path, 'rb') as image_file:
        image = {
            'content': base64.b64encode(image_file.read()).decode('UTF-8')
        }

    return {'features': features, 'image': image}


def create_single_post(image_path, types):
    return json.dumps({'requests': [configure_item(image_path, types)]})
