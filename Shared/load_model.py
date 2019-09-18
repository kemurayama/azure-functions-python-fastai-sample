from fastai.basic_train import load_learner, defaults
from torch import device
import aiohttp
import asyncio

def load_fastai():
    defaults.device = device('cpu')
    learn = load_learner('trained')
    learn.load('stage-2')
    return learn
