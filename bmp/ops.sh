rm -rf templates
rm -rf static 

cd ../../ops
git pull
cd ../bmp/bmp

ln -s ../../ops/static/templates/ templates 
ln -s ../../ops/static/static/ static
