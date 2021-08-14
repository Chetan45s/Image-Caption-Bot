# Image-Caption-Bot

## Description of the project


Created a Deep Learning Model that Caption the Image with good
accuracy using RNN,CNN,word2vec and Keras.

In this project we worked on the flicker8k dataset and tried to train a deep learning model that can caption the image by itself. Further more we hosted
the trained model using django and connect the model to the bot that can take a image as a input and output the image with captions on it.

### Some sample captions that are generated
1       	  | 2		| 	3             
:-------------------------:|:-------------------------:|:------------------------:
![](https://raw.githubusercontent.com/adityajn105/image-caption-bot/master/samples/sample1.png)  |  ![](https://raw.githubusercontent.com/adityajn105/image-caption-bot/master/samples/sample2.png)		| ![](https://raw.githubusercontent.com/adityajn105/image-caption-bot/master/samples/sample3.png) 

## Tech

Image Caption Bot uses following technologies:

- [HTML CSS] - For good GUI.
- [Python] - All the backend and machine learning code is writtern in Python.
- [Tensorflow] - To server keras a backend
- [Django] - For backend services

## Installation

Image Caption Bot requires [Python](https://www.python.org/) v3+ to run.

```sh
git clone https://github.com/Chetan45s/Image-Caption-Bot.git

cd Image-Caption-Bot

```


```sh
pip install virtualenv

mkvirtualenv image_bot

workon image_bot

pip install -r requirement.txt (This may take some time as we required to install tensorflow)

python manage.py runserver

```

Now, switch to https://locahost:8000

It will look something like this

![alt text](https://raw.githubusercontent.com/Chetan45s/Image-Caption-Bot/master/media/icb_1.jpg)
![alt text](https://raw.githubusercontent.com/Chetan45s/Image-Caption-Bot/master/media/icb_2.jpg)
