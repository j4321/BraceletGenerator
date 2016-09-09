#! /usr/bin/python2
# -*- coding:Utf-8 -*-

# Uninstall previous version if installed

import os
import sys
import shutil

local_path = os.path.expanduser("~")

paths = os.environ["PATH"].split(":")
for path in paths:
    p = os.path.join(path, "BraceletGenerator")
    if os.path.exists(p):
        os.remove(p)
    if os.path.exists(p + ".py"):
        os.remove(p + ".py")

module_paths = sys.path
for path in module_paths:
    mod = os.path.join(path, "BraceletGeneratorModules")
    if os.path.exists(mod):
        shutil.rmtree(mod)

menu_entry = os.path.join(local_path, ".local", "share", "applications", "BraceletGenerator.desktop")
if os.path.exists(menu_entry):
    os.remove(menu_entry)

config = os.path.join(local_path, "BraceletGenerator")
if os.path.exists(config):
    l = os.listdir(config)
    to_delete = [f for f in l if (l[-3:] == "log" or l[-6:] == "config")]
    for f in to_delete:
        os.remove(os.path.join(config, f))