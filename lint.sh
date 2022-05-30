#!/bin/bash

source activate

isort ieee_csdl_downloader/ test/
mypy ieee_csdl_downloader/ test/
flake8 ieee_csdl_downloader/ test/
blue ieee_csdl_downloader/ test/