#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import re

# Globals
status = {
	'running': {
		'symbol': '&#9654;',
		'actions': ['Shutdown', 'Pause', 'Reboot', 'Destroy']
	},
	'paused': {
		'symbol': '&#9646;&#9646;',
		'actions': ['Resume', 'Shutdown', 'Destroy']
	},
	'shut off': {
		'symbol': '&#9724;',
		'actions': ['Start']
	},
	'crashed': {
		'symbol': '&#8251',
		'actions': ['Start', 'Destroy']
	},
	'in shutdown': {
		'symbol': '&#10071',
		'actions': []
	},
	'idle': {
		'symbol': '&#8275',
		'actions': []
	},
	'dying': {
		'symbol': '&#9760',
		'actions': []
	}
}

# Data parsing
def get_vms():
	vms = []
	output = subprocess.check_output(['virsh', 'list --all']).decode("utf-8").split('\n')[2:]
	for l in output:
		if l == "": continue
		vms.append(get_vms_extract(l))
	return vms

def get_vms_extract(line):
	vm = {}
	line = re.sub(r"[ ]{2,}", ",", line[1:]).split(",")
	vm = {
		"id": line[0],
		"name":  line[1],
		"status": line[2]
	}
	return vm

def get_cmd(action, vm):
	return 'virsh ' + action + ' ' + vm


def get_vm_valid_actions(vm):
	output = ""
	actions = {
		'Start': get_cmd('start', vm['name']),
		'Shutdown': get_cmd('shutdown', vm['id']),
		'Reboot': get_cmd('reboot', vm['id']),
		'Pause': get_cmd('suspend', vm['id']),
		'Resume': get_cmd('resume', vm['id']),
		'Destroy': get_cmd('destroy', vm['id'])
	}

	for action in status[vm['status']]['actions']:
		output += xml_vm_action(action, actions[action])

	return output


# XML generators
def xml_main():
	output = '<?xml version="1.0" encoding="UTF-8"?>\n'
	output += '<openbox_pipe_menu>\n'
	for vm in get_vms():
		output += xml_vm(vm)
	output += '</openbox_pipe_menu>\n'
	return output

def xml_vm(vm):
	output = '\t<menu id="' + vm['name'] + '" label="' + status[vm['status']]['symbol'] + ' ' + vm['name'] + '">\n'
	output += get_vm_valid_actions(vm)
	output += '\t</menu>\n'
	return output

def xml_vm_action(action, cmd):
	output = '\t\t<item label="' + action + '">\n'
	output += '\t\t\t<action name="Execute">\n'
	output += '\t\t\t\t<execute>\n'
	output += '\t\t\t\t\t' + cmd
	output += '\t\t\t\t</execute>\n'
	output += '\t\t\t</action>\n'
	output += '\t\t</item>\n'
	return output

xml = xml_main()
print(xml)
