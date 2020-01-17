#!/usr/bin/env python3

import os
from constantes import DCMTEMP 


os.system("storescp 1104 -v -dhl --fork -od " + DCMTEMP + " -xcr  './import.py \#f'")
    