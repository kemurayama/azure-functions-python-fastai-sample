import logging
import azure.functions as func
from fastai.vision import open_image
from __app__.Shared import load_model, utility
from io import BytesIO

learn = None

async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Start my function')

    # fetch image from form data
    try:
        url = req.form['url']
    except:
        logging.error('Customer didn\'t pass URL', exc_info=True)
        return func.HttpResponse(
            "Please pass URL for Prediction",
            status_code=400
            )

    # load model as global to cache
    global learn
    if learn is None:
        learn = load_model.load_fastai()    

    # fetch image from URL then predict
    try:
        image = await utility.get_bytes(url)
        img = open_image(BytesIO(image))
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