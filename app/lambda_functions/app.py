import boto3
import cv2
import numpy as np
import tempfile

dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")


def lambda_handler(event, *_):
    table_name = "CloudThumb-Table"
    key = event["key"]

    table = dynamodb.Table(table_name)
    response = table.get_item(Key={'UserId': key})
    item = response.get("Item")
    if not item:
        return {"error": "Item not found"}

    bucket_name = "cloud-thumb-bucket"

    image_color = 'RGB'
    with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp:
        s3.download_file(bucket_name, item['FileName'], tmp.name)
        image = cv2.imread(tmp.name)

        if image is None:
            return {"error": "Not an Image"}

        if len(image.shape) == 3:
            if np.array_equal(image[:, :, 0], image[:, :, 1])\
                and np.array_equal(image[:, :, 1], image[:, :, 2]):
                image_color = "Greyscale"

        nr_white_pixels = np.all(image == 255, axis=-1)
        nr_black_pixels = np.all(image == 0, axis=-1)
        binary_pixels = np.logical_or(nr_white_pixels, nr_black_pixels)

        if np.all(binary_pixels):
            image_color = "Black and White"

    return {
        "result": image_color
    }
