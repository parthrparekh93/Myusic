import numpy as np
import lda
import lda.datasets
import pandas as pd
from os import listdir
from os.path import isfile, join

mypath = '/home/parth/Documents/BigDataAnalytics/LDA/Myusic/Songs/'
#X = lda.datasets.load_reuters()
X = []
for line in open('Vectorized_Matrix.txt','r').readlines():
    X.append(map(lambda x:int(x),line.split()))

X = np.asarray(X)
#vocab = lda.datasets.load_reuters_vocab()
#titles = lda.datasets.load_reuters_titles()
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
files.sort()
X.shape
X.sum()
model = lda.LDA(n_topics=20, n_iter=1500, random_state=1)
model.fit(X)  # model.fit_transform(X) is also available
doc_topic = model.doc_topic_
for i in range(30):
  print("{} (top topic: {})".format(files[i], doc_topic[i].argmax()))
