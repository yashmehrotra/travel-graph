`cd ..`
lint=`flake8 .`
if [ -z "$lint" ]; then
    echo "Ready to go, good job following pep8!"
else
    echo $lint
fi
