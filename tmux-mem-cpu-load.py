#!/usr/bin/python3
"""Expansion of tmux-mem-cpu-load plugin.
The idea is to parse sensor information and prepend it to the output of the
original plugin.
In my .tmux.conf I set:
set -g status-right '#($TMUX_PLUGIN_MANAGER_PATH/tmux-mem-cpu-load/tmux-mem-cpu-load.py)#[default]'
"""

import re
import subprocess
import sys
import os.path
from datetime import datetime as dt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

temperature = ""

try:
    # for Raspberry Pi
    with open("/sys/class/thermal/thermal_zone0/temp") as f:
        temperature = "{}°C".format(int(float(f.read()) * 0.001))
except IOError:
    try:
        # shamelessly copied from bumblebee-status (module 'sensors')
        temperature_pattern = re.compile(r"^\s*temp1_input:\s*([\d.]+)$", re.MULTILINE)

        temperature_info = subprocess.check_output(["sensors", "-u"]).decode("ascii")
        match = temperature_pattern.findall(temperature_info)

        if match:
            temperature = "{}°C".format(int(float(match[0])))
    except subprocess.CalledProcessError:
        pass

# get the original output and prepend the temperature info
plugin_output = subprocess.check_output(
        [os.path.join(SCRIPT_DIR, "./tmux-mem-cpu-load")] + sys.argv[1:]
        ).decode("utf-8")

print(" ".join([
    dt.now().strftime("%m-%d %H:%M:%S"), temperature, plugin_output]))

# not required in python, script will return 0 (success) anyway
# sys.exit(0)
