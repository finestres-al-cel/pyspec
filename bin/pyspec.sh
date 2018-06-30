#!/bin/bash

cd ../src
ipython pyspec.py 2> temp
rm temp
cd ../bin
