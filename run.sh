#!/bin/bash
python3 create.py
# Run SWIFT
../../../swift --self-gravity --hydro --threads=34 config.yml 2>&1 | tee output.log
