pyinstaller run.py -p . -F -n space_caravan --hidden-import packaging.requirements --hidden-import pkg_resources.py2_warn --windowed
cp -r images dist/.
cp -r sounds dist/.