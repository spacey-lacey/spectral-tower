#!/bin/bash

# set repo directory in mapping interface to pwd
interface_file="bit_slicer/mapping_interface.py"

if sed -i "" "12s|Path(\".*\")|Path(\"$(pwd)\")|" $interface_file
then
    echo "Updated git_repo_path in $interface_file to $(pwd)"
else
    echo "Error: Could not update git_repo_path in $interface_file"
fi
