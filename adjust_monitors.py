#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyudev
import subprocess
import time
import os
import logging

logging.basicConfig(filename='/tmp/adjust_monitors.log',
                    level=logging.INFO)

INSTALL_DIR = os.getenv('ADJUST_MONITOR_INSTALLDIR')


def adjust_monitor_xrandr(num_monitors):
    """ Runs a specific xrandr script to adjust i3 depending on the
    num_monitors

    Parameters
    ----------

    num_monitors: int
        Number of monitors connected at this moment in time

    """
    logging.info(f'Number of monitors: {num_monitors}')
    if num_monitors == 1:
        logging.info('Executing just_laptop.sh')
        if subprocess.call(INSTALL_DIR + '/just_laptop.sh') != 0:
            logging.warning("Couldn't execute just_laptop.sh")
    else:
        logging.info('Executing laptop_and_screen_on_top.sh')
        if subprocess.call(INSTALL_DIR + '/laptop_and_screen_on_top.sh') != 0:
            logging.warning("Couldn't execute laptop_and_screen_on_top.sh")


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
        adjust_monitor_xrandr(get_number_of_monitors_connected())


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
    except Exception as e:
        logging.error(e.with_traceback)
