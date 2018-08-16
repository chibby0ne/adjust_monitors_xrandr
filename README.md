## Simple script for adjusting laptop monitors through xrandr scripts

## Requirements

* python >= 3.5
* pyudev >= 0.21


Need to add root to the list of authorized X users, this is easily achieve
with xhost:

```
xhost si:localuser:root
```

## TODO

- Run systemd as the local user. Find a way of not adding root to xhost
