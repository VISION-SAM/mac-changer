#!/usr/bin/env python

import subprocess
import optparse
import re

def get_arg():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="Assign a new mac address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify an mac, use --help for more info.")
    return options

def changemac(interface, new_mac):
    print("[+] Changing MAC for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def print_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_add_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_add_search_result:
        return mac_add_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")


options = get_arg()

current_mac = print_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

changemac(options.interface, options.new_mac)

current_mac = print_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed.")

