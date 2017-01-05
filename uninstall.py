#! /usr/bin/python3
# -*- coding:Utf-8 -*-

# Uninstall BraceletGenerator >= 1.3.0 (only if installed with setup.py)

import os
import sys
import shutil

local_path = os.path.expanduser("~")

if os.path.exists("/usr/bin/bracelet-generator"):
    os.remove("/usr/bin/bracelet-generator")

module_paths = sys.path
for path in module_paths:
    mod = os.path.join(path, "BraceletGenerator")
    if os.path.exists(mod):
        shutil.rmtree(mod)

menu_entry = os.path.join(local_path, ".local", "share", "applications", "bracelet-generator.desktop")
if os.path.exists(menu_entry):
    os.remove(menu_entry)

config = os.path.join(local_path, "BraceletGenerator")
if os.path.exists(config):
    l = os.listdir(config)
    to_delete = [f for f in l if (l[-3:] in ["log", "ini"] or l[-6:] == "config")]
    for f in to_delete:
        os.remove(os.path.join(config, f))
    if not os.listdir(config):
        os.rmdir(config)
