#!/usr/bin/env bash

_pwd=$(exec pwd)

echo $_pwd
cd _pwd && ../
echo pwd

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete && find . -path "*/migrations/*.pyc"  -delete &&
#rm teleblog.dat &&
#rm -rf uploads/ &&

echo "Ok"
