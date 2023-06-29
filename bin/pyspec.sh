#!/bin/bash

cd ../src
ipython pyspec_old.py 2> temp
rm temp
cd ../bin
