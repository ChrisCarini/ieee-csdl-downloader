#!/bin/bash

source activate

ruff check
mypy ieee_csdl_downloader/ test/
