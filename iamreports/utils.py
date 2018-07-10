#!/usr/bin/env python
import yaml

def yamlfmt(obj):
    """Convert a dictionary object into a yaml formated string"""
    if isinstance(obj, str):
        return obj
    return yaml.dump(obj, default_flow_style=False)
