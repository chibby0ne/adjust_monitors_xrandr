.PHONY: install start enable stop disable uninstall

INSTALL_DIR=/usr/local/bin
SYSTEMD_INSTALL_DIR=/etc/systemd/system

install:
	sudo install -D adjust_monitors.py $(INSTALL_DIR)/adjust_monitors.py
	sudo install -D adjust_monitors/just_laptop.sh $(INSTALL_DIR)/adjust_monitors/just_laptop.sh
	sudo install -D adjust_monitors/laptop_and_screen_on_top.sh $(INSTALL_DIR)/adjust_monitors/laptop_and_screen_on_top.sh
	sudo install -D adjust_monitors.service $(SYSTEMD_INSTALL_DIR)/adjust_monitors.service

start:
	sudo systemctl start adjust_monitors.service

enable:
	sudo systemctl enable adjust_monitors.service

stop:
	sudo systemctl stop adjust_monitors.service

disable:
	sudo systemctl disable adjust_monitors.service

uninstall:
	sudo rm -f $(INSTALL_DIR)/adjust_monitors.py
	sudo rm -f $(INSTALL_DIR)/adjust_monitors/just_laptop.sh
	sudo rm -f $(INSTALL_DIR)/adjust_monitors/laptop_and_screen_on_top.sh
	sudo rm -f $(SYSTEMD_INSTALL_DIR)/adjust_monitors.service
