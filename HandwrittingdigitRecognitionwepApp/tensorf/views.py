from django.shortcuts import render
from django.http import JsonResponse
import numpy as np
import cv2
from keras.models import load_model
import base64
import keras
#from .apps import ProjetsConfig

# Create your views here.

import os
import re
from PIL import Image
import io

def index(request):
    context ={}
    return render (request,"index.html",context)
def predit_digit(request):
    
    imgdata = request.POST.get('image')
    imgstr = re.search(r'base64,(.*)',imgdata).group(1)
    imgdata = base64.b64decode(imgstr)
    x=np.frombuffer(imgdata,dtype=np.uint8)
    img=cv2.imdecode(x,cv2.IMREAD_GRAYSCALE)
    img = np.invert(img)
    img=cv2.resize(img, (28,28), interpolation = cv2.INTER_AREA)
    img= img.reshape(1,28,28,1)
    filename = os.path.join(os.getcwd(),'model_digits.h5')
    model_digit= load_model(filename)
    res= model_digit.predict_classes(img)
    res = np.array_str(res)
    res=int(res[1])
    print(res)
    model_digit= load_model(filename)
    keras.backend.clear_session()
    return JsonResponse({'result': res})
  
    