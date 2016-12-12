#!/bin/sh
python players.py
python website.py
cd ../../bradyb.github.io/
git add -A
git commit -m "from script"
git push origin master
