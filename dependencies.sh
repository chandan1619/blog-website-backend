#!/bin/bash

# Activate Conda environment
conda create -y -n blog_api python=3.11.0

conda activate blog_api

# Install dependencies using Poetry
poetry install
