#!/bin/bash

# set repo directory in mapping interface to pwd
mapping_interface_file="bit_slicer/mapping_interface_script.py"

if sed -i "" "12s|Path(\".*\")|Path(\"$(pwd)\")|" $mapping_interface_file
then
    echo "Updated git_repo_path in $mapping_interface_file to $(pwd)"
else
    echo "Error: Could not update git_repo_path in $mapping_interface_file"
fi
