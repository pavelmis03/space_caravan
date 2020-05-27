pyinstaller run.py -p . -F -n space_caravan --hidden-import packaging.requirements --exclude-module pkg_resources
cp -r images dist/.
cp -r sounds dist/.