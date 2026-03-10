import hilbert_curve as hc
from PIL import Image
import math
from time import sleep
import alsaaudio
import numpy as np
from threading import Thread, Lock

def main():

    while True:
        img = Image.open(input_file).convert("L")
        pixels = img.load()
        output = []
        for i in range(0, x ** 2):
            hilbert = hc.d2xy(math.log(x * y, 2), i)
            output.append(pixels[hilbert])
