#!/usr/bin/env bash

for file in bin/*py pyspec/*py pyspec/*/*py
do
  echo "yapf --style google $file -i"
  yapf --style google $file -i
done
