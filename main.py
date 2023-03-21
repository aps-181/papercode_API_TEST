from flask import Flask, request
from flask_restful import Api, Resource
import cv2
import numpy as np
import base64

app = Flask(__name__)
api = Api(app)


def gamma_correction(src, gamma):

    # output pixel value [0,255] = (i/255)^(1/gamma) * 255
    gamma = 1 / gamma
    table = [((i / 255) ** gamma) * 255 for i in range(256)]
    table = np.array(table, np.uint8)
    # For each pixel value in the range [0, 255] is calculated
    # corresponding gamma corrected value.
    # OpenCV provides LUT function which performs a lookup table transform.
    return cv2.LUT(src, table)
    # γ - gamma that controls image brightness.
    # If gamma < 1 then image will be darker,
    # if gamma > 1 then image will be lighter.
    # A gamma = 1 has no effect.


class HelloWorld(Resource):
    def get(self):
        return {"data": "Hello World"}

    def post(self, img):
        # with open("new1_image3.jpg", "rb") as f:
        #     image = base64.b64encode(f.read())
        image = request.form['image']
        decoded_data = base64.b64decode(image)
        np_data = np.frombuffer(decoded_data, np.uint8)
        img = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)
        img = gamma_correction(img, 3)
        cv2.imshow("test", img)
        cv2.waitKey(0)
        string = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
        return {"status": "done"}


api.add_resource(HelloWorld, "/helloworld/<string:img>")

if __name__ == '__main__':
    app.run(debug=True)
