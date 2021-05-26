from django.shortcuts import render
from django.shortcuts import get_object_or_404
from Bot.forms import BotForm
from PIL import Image, ImageDraw, ImageFont
import base64
import io

import numpy as np
import cv2
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model,load_model
import pickle

model_new_loaded = load_model('./model_weights/resnet_model_.h5')
model = load_model('./model_weights/model_14.h5')

with open("./model_weights/word_to_ind.pkl","rb") as f:
    word_to_ind = pickle.load(f)
    f.close()
    
with open("./model_weights/ind_to_word.pkl","rb") as f:
    ind_to_word = pickle.load(f)
    f.close()

def pre_processing(img):
    loaded_img = img.resize((224, 224))
    cvt2_array = image.img_to_array(loaded_img)
    ## as this model_new take 4D tensor as a input(batch_size, 3 channel image)
    ## and we are proceding with 1 image in a single batch so we expand dim and add btach_size = 1
    
    img_tnsr = np.expand_dims(cvt2_array,axis=0)
    
    ## Normalisation : For this we use preprocess_input function of the Resnet
    final_img = preprocess_input(img_tnsr)
    return final_img

def encode_image(img):
    img = pre_processing(img)
    feature_vector = model_new_loaded.predict(img)
    feature_vector = feature_vector.reshape((-1,))
    return feature_vector.reshape((1,2048))

def predict_caption(photo):
    max_len = 38
    in_text = "startseq"
    for i in range(max_len):
        sequence = [word_to_ind[w] for w in in_text.split() if w in word_to_ind]
        sequence = pad_sequences([sequence],maxlen=max_len,padding='post')
        
        ypred = model.predict([photo,sequence])
        ypred = ypred.argmax() #WOrd with max prob always - Greedy Sampling
        word = ind_to_word[ypred]
        in_text += (' ' + word)
        
        if word == "endseq":
            break
    
    final_caption = in_text.split()[1:-1]
    final_caption = ' '.join(final_caption)
    return final_caption

def bot(request):
    bot_form = BotForm()
    if request.method == 'POST':
        bot_form = BotForm(request.FILES,request.POST)
        image = request.FILES["image_value"]
        img = Image.open(image) 
        width,height = img.size
        encoded_image_2048 = encode_image(img)
        caption = predict_caption(encoded_image_2048)


        background = Image.new('RGBA',(width+10,height+int(height/9)),'white')
        background.paste(img,(5,5,(width+5),(height+5)))


        title_font = ImageFont.truetype('./model_weights/Pattaya-Regular.ttf',20)

        image_editable = ImageDraw.Draw(background)
        image_editable.text((30,height+10), caption, font=title_font,fill="black")

        img = background

        img = img.convert('RGB')
        data = io.BytesIO()
        img.save(data, "JPEG") # just an example, load the image into BytesIO any way you like.
        encoded_img = base64.b64encode(data.getvalue())
        decoded_img = encoded_img.decode('utf-8')
        img_data = f"data:image/jpeg;base64,{decoded_img}"
        return render(request, 'bot1.html',{'img_data':img_data})
    return render(request, 'bot.html',{'bot_form':bot_form})

