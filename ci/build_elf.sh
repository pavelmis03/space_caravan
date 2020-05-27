pyinstaller run.py -p . -F -n space_caravan --hidden-import pygame --windowed
cp -r images dist/.
cp -r sounds dist/.