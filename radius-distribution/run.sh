#!/bin/bash

# Generate the initial conditions if they are not present.
if [ ! -e IC.hdf5 ]
then
    echo "Generating initial conditions for the circumbinary accretion..."
    python3 create.py
fi

# Run SWIFT
# ../../../swift --self-gravity --threads=16 config.yml 2>&1 | tee output.log
../../../swift --hydro --self-gravity --threads=16 config.yml 2>&1 | tee output.log