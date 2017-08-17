#!/usr/bin/python3
"""Expansion of tmux-mem-cpu-load plugin (not functioning).
The idea is to parse sensor information and prepend it to the output of the
original plugin.
In my .tmux.conf I set:
set -g status-right '#($TMUX_PLUGIN_MANAGER_PATH/tmux-mem-cpu-load/tmux-mem-cpu-load.py)#[default]'
"""

import re
import subprocess
import sys

# shamelessly copied from bumblebee-status (module 'sensors')
temperature_pattern = re.compile(r"^\s*temp1_input:\s*([\d.]+)$", re.MULTILINE)

temperature_info = subprocess.check_output(["sensors", "-u"]).decode("ascii")
match = temperature_pattern.findall(temperature_info)

temperature = ""
if match:
    temperature = "{}°C ".format(int(float(match[0])))

# get the original output and prepend the temperature info
plugin_output = subprocess.check_output("./tmux-mem-cpu-load").decode("ascii")

# neither of these gives any output in tmux status
# print(temperature + plugin_output)
sys.stdout.write(temperature + plugin_output)
sys.stdout.flush()

# not required in python, script will return 0 (success) anyway
# sys.exit(0)
