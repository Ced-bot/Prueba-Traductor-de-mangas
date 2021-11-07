# -*- coding: utf-8 -*-
from textblob import TextBlob
import time
inicio = time.time()
from googletrans import Translator

t='  بوكور. '
print(t)
blob = TextBlob(t)

print(blob.detect_language())
print(blob.translate(to='es'))

fin = time.time()
print(fin-inicio)