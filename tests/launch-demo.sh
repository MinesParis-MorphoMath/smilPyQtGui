#! /bin/bash

TOP=$(pwd)

if [ -z "$PYTHONPATH" ]
then
  export PYTHONPATH=${TOP}/../src
else
  export PYTHONPATH=${TOP}/../src:$PYTHONPATH
fi

for demo in $*
do
  echo "Launching $demo"
  ./$demo
done
