cd ../src/

xgettext *.py */*.py
sed messages.po --in-place --expression=s/CHARSET/UTF-8/
