#!/usr/bin/env bash
rm -rf templates
rm -rf static 

cd ../../ops
git pull
cd ../bmp/bmp

ln -s ../../ops/static/ templates
ln -s ../../ops/static/ static
