coverage run -m unittest tests/*.py
coverage report -m > report.txt
cat report.txt