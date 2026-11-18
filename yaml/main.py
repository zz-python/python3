#!/usr/bin/env python3
"""Entry point — extract key-value pairs from a YAML localization file."""

import sys
import os

# Ensure the script's directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from yaml_extract import main

main("C:/project/ui_remote_module/locales/zh-CN.yaml", "socAlert")