#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import pyudev
import subprocess


def adjust_monitor_xrandr(num_monitors):
    """ Runs a specific xrandr script to adjust i3 depending on the
    num_monitors

    Parameters
    ----------

    num_monitors: int
        Number of monitors connected at this moment in time

    """
    if num_monitors == 1:
        subprocess.call('just_laptop.sh')
    else:
        subprocess.call('laptop_and_screen_on_top.sh')


def get_number_of_monitors_connected():
    """
    Gets the number of monitors connected to the computer

    Returns
    -------
    int, number of monitors connected. For a laptop, this values is always >= 1
    """
    # Commands to execute
    xrandr_cmd = ('xrandr', '-q')
    grep_cmd = ('grep', '-w', 'connected')
    wc_l_cmd = ('wc', '-l')

    # Start each command in a separate process and pipe each others
    # output/input. This is done in order to avoid using shell=True, in one
    # simple, check_output, which is less secure because it allows shell
    # injection
    xrandr_proc = subprocess.Popen(xrandr_cmd,
                                   stdout=subprocess.PIPE)
    grep_proc = subprocess.Popen(grep_cmd,
                                 stdout=subprocess.PIPE,
                                 stdin=xrandr_proc.stdout)
    output = subprocess.check_output(wc_l_cmd,
                                     stdin=grep_proc.stdout)
    # Strip the newline character appended to the command output
    num_monitors = output.strip(b'\n')
    # Cast from bytes to int, and return it
    return int(num_monitors)


# context = pyudev.Context()
# monitor = pyudev.Monitor.from_netlink(context)

# monitors are part of the drm subsystem
# monitor.filter_by('drm')

num_monitors = get_number_of_monitors_connected()
print(f'num of monitors: {num_monitors}')
adjust_monitor_xrandr(num_monitors)
# observer = pyudev.MonitorObserver(monitor, adjust_monitor_xrandr(num_monitors))
# observer.start()
