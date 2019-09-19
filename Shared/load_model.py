from fastai.basic_train import load_learner, defaults
from torch import device
from pathlib import Path
import os
import logging


def load_fastai():
    modelpath = Path(__file__).parent
    modelpath = modelpath/'trained'
    logging.info('load model path {0}'.format(os.getcwd()))
    defaults.device = device('cpu')
    learn = load_learner(modelpath)
    learn.load('stage-2')
    return learn
