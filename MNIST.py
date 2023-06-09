# -*- coding: utf-8 -*-
"""Assignment1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jZiUIbjhUQgAK5WIqpljb-nroYMqZIat

## Assignment 1
AndrewID: aarushis

Import Statements
"""

import struct
import gzip
import numpy as np
import matplotlib.pyplot as plt
import sklearn
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.model_selection import cross_val_score,GridSearchCV
from sklearn.metrics import accuracy_score,confusion_matrix
from sklearn.linear_model import LogisticRegression
import pickle

"""Unzip the files, and unpack ubyte into numpy array"""

#code source: Professor
def unzipData(file_name):
  data = None
  with gzip.open(file_name, 'rb') as f:
    magic, size = struct.unpack(">II", f.read(8))
    nrows, ncols = struct.unpack(">II", f.read(8))
    data = np.frombuffer(f.read(), dtype=np.dtype(np.uint8).newbyteorder('>'))
    data = data.reshape((size,nrows,ncols))
  print(data.shape)
  return data
def unzipLabelData(file_name):
  data = None
  with gzip.open(file_name, 'rb') as f:
    magic, size = struct.unpack(">II", f.read(8))
    data = np.frombuffer(f.read(), dtype=np.dtype(np.uint8).newbyteorder('>'))
    data = data.reshape((size))
  print(data.shape)
  return data

test_images=unzipData("t10k-images-idx3-ubyte.gz")
test_labels=unzipLabelData("t10k-labels-idx1-ubyte.gz")
train_images=unzipData("train-images-idx3-ubyte.gz")
train_labels=unzipLabelData("train-labels-idx1-ubyte.gz")

#Plotting the data to help visualize
plt.imshow(test_images[0,:,:], cmap='Purples')
plt.show()

"""MNIST is a discrete dataset. It consists of 28x28 pixel grayscale images of handwritten digits (0-9) which can only take on specific values for each pixel (0-255). The values are not continuous and can only take on certain discrete values, so it is considered a discrete dataset.

A Source: http://proceedings.mlr.press/v97/jeong19d/jeong19d.pdf 

Below I am training both Gaussian and Multinomial Naive Bayes model to see which perfoms better.
"""

multiNB = MultinomialNB()
gaussNB = GaussianNB()
test_images.shape

# https://stackoverflow.com/questions/34972142/sklearn-logistic-regression-valueerror-found-array-with-dim-3-estimator-expec
nsamples, nx, ny = test_images.shape
test_images_reshaped = test_images.reshape((nsamples,nx*ny))
nsamples, nx, ny = train_images.shape
train_images_reshaped = train_images.reshape((nsamples,nx*ny))

multiNB.fit(train_images_reshaped,train_labels)
gaussNB.fit(train_images_reshaped,train_labels)

"""Getting the Accuracy of both models using score.
Clearly Multinomial NB has a better accuracy and we will take that as our Naive Bayes model.
"""

print("multiNB " , multiNB.score(test_images_reshaped,test_labels))
print("gaussNB " , gaussNB.score(test_images_reshaped,test_labels))

"""Confusion Matrix for Multinomial"""

gnb_predict = multiNB.predict(test_images_reshaped)
cm1= confusion_matrix(test_labels,gnb_predict)
print(cm1)

"""Hyperparameter tuning on Multinomial - This does not change the accuracyby a lot

"""

param_grid = {'alpha': [0.1,0.5,1,2,5]}
mnb = MultinomialNB()
grid_search = GridSearchCV(mnb, param_grid)
grid_search.fit(train_images_reshaped, train_labels)
best_params = grid_search.best_params_
mnb2 = MultinomialNB(alpha=best_params['alpha'])
mnb2.fit(train_images_reshaped, train_labels)
print(mnb2.score(test_images_reshaped, test_labels))

"""Logistic Regression Model and its Accuracy"""

lr = LogisticRegression()
lr.fit(train_images_reshaped, train_labels)
print("Accuracy for Logistic Regression",lr.score(test_images_reshaped, test_labels) )

"""Confusion Matrix for Logistic Regression"""

lr_predict = logisticRegr.predict(test_images_reshaped)
cm= confusion_matrix(test_labels,lr_predict)
print(cm)

"""Adding both models to pickle file"""

pickle.dump(logisticRegr, open('lr.model.pkl', 'wb'))
pickle.dump(multiNB, open('nb.model.pkl', 'wb'))