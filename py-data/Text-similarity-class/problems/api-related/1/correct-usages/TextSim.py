import numpy as np
import pandas as pd
import time
from sklearn.feature_extraction.text import TfidfVectorizer
import string
import warnings
warnings.filterwarnings('ignore')
from contextlib import contextmanager
import mysql.connector
from sqlalchemy import create_engine
import pygsheets
from tqdm import tqdm
import yaml
import os
import binascii
import random
from numba import jit

class TextSim(object): 
 
 def create_shingles(self, data):
        text_list = list(data[self.text_column])
        shingles_all = []
        maxshingleID = 0
        for i in tqdm(range(0, len(text_list))):       
            words = text_list[i].split(" ")
            shingles_set = self._create_shingle(words)
            maxID = max(shingles_set) if shingles_set else 0
            if maxID > maxshingleID:
                maxshingleID = maxID
            shingles_all.append(shingles_set)
        return shingles_all, maxshingleID
