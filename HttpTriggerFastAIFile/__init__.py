import logging
import azure.functions as func
from __app__.Shared import load_model, utility
from io import BytesIO
from fastai.vision import open_image

learn = None

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        image_file = req.files['petimage'].stream
    except:
        return func.HttpResponse(
            "Failed to get image. Check the URL",
            status_code=400
        )
    
    global learn
    if learn is None:
        learn = load_model.load_fastai()  

    # fetch image from uploaded file then predict
    try:
        img = open_image(BytesIO(image_file.read()))
        _,_,losses = learn.predict(img)
    except Exception as e:
        logging.error('predict image failed', exc_info=True)
        return func.HttpResponse(
            "Failed to get image. Check the URL",
            status_code=400
        )

    res = sorted(zip(learn.data.classes, map(float, losses)),key=lambda x:x[1],reverse=True)
    result_class = res[0][0]

    return func.HttpResponse(
            "Is your image {0} ?".format(result_class),
            status_code=200
            )