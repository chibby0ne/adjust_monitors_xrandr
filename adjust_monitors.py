#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyudev
import subprocess
import time
import os
import logging

logging.basicConfig(filename='/tmp/adjust_monitors.log',
                    level=logging.INFO)


PRIMARY_MONITOR = 'xrandr --output %s --primary --mode 1920x1080 --pos 0x%s --rotate normal'
APPEND_MONITOR = '--output %s --mode 2560x1080 --pos 0x0 --rotate normal '


def adjust_monitor_xrandr(monitors):
    """ Runs a specific xrandr script to adjust i3 depending on the
    num_monitors

    Parameters
    ----------

    num_monitors: array of str
        Number of monitors connected at this moment in time

    """
    logging.info('Monitors: %s', monitors)
    if len(monitors) == 1:
        cmd = PRIMARY_MONITOR % ('eDP1', '0')
        subprocess.call(cmd)
    else:
        # If one of the monitors is a laptop, use the laptop as primary display
        if 'eDP1' in monitors:
            cmd = PRIMARY_MONITOR % ('eDP1', '1080')
            monitors.remove('eDP1')
            for mon in monitors:
                cmd += APPEND_MONITOR % mon
            subprocess.call(cmd)
        else:
            mon = monitors.pop()
            cmd = PRIMARY_MONITOR % ('eDP1', '1080')
            for mon in monitors:
                cmd += APPEND_MONITOR % mon
            subprocess.call(cmd)


def get_monitors_connected():
    """
    Gets the monitors connected to the computer

    Returns
    -------

    list of str, of monitors connected. For a laptop, this values is always
    [eDP1 + ... ]
    """
    # Commands to execute
    xrandr_cmd = ('xrandr', '-q')
    grep_cmd = ('grep', '-w', 'connected')
    awk_cmd = ('awk', '\'{print $1}\'')

    # Start each command in a separate process and pipe each others
    # output/input. This is done in order to avoid using shell=True, in one
    # simple, check_output, which is less secure because it allows shell
    # injection
    xrandr_proc = subprocess.Popen(xrandr_cmd,
                                   stdout=subprocess.PIPE)
    grep_proc = subprocess.Popen(grep_cmd,
                                 stdout=subprocess.PIPE,
                                 stdin=xrandr_proc.stdout)
    output_displays = subprocess.check_output(awk_cmd,
                                              stdin=grep_proc.stdout)

    # Strip the newline character appended at the end and convert the monitors
    # ids into list of str
    displays_str_array = output_displays.rstrip(b'\n').decode().split('\n')
    return displays_str_array


def check_monitors_change(action, device):
    """
    Event handler which is asynchronously call on every event of the monitor.
    It will call run the adjust_monitor_xrandr using the current number of
    monitor if the event was of type 'change' and happened on DRM device
    'card0'. Parameters are mandatory for MonitorObserver's event handlers.

    Parameters
    ----------

    action: str
        String representation of the type of action of the event

    device: pyudev.Device
        Device on which the event happened
    """
    if action == 'change' and device.device_node.endswith('card0'):
        adjust_monitor_xrandr(get_monitors_connected())


if __name__ == "__main__":
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    # monitors are part of the drm subsystem
    try:
        monitor.filter_by('drm')
        observer = pyudev.MonitorObserver(monitor, check_monitors_change)
        observer.start()
        while True:
            time.sleep(1)
    except Exception:
        logging.exception('Something went wrong')
