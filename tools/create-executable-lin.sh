echo "--------------------------------------------------------"
echo "PyORPG Executable Tool for GNU/Linux (using PyInstaller)"
echo "--------------------------------------------------------"

read -p "Choose a name for your executable: " execname

echo "Building executable using PyInstaller..."
pyinstaller ../src/pyorpg.py -F -o ../tmp -n $execname

echo "Making bin folder if it doesnt exist..."
mkdir ../bin

echo "Moving binary into the bin folder..."
mv ../tmp/dist/$execname ../bin/

echo "Generating launcher for executable..."
