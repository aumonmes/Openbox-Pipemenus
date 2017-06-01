#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import re

# Config
FULL_UNICODE = False

# Globals
status = {
	'running': {
		'icon': '&#9654;',
		'actions': ['View', 'Shutdown', 'Pause', 'Reboot', 'Destroy']
	},
	'paused': {
		'icon': '&#9208;',
		'actions': ['Resume', 'Shutdown', 'Destroy']
	},
	'shut off': {
		'icon': '&#9209;',
		'actions': ['Start']
	},
	'crashed': {
		'icon': '&#8251',
		'actions': ['Start', 'Destroy']
	},
	'in shutdown': {
		'icon': '&#10071',
		'actions': []
	},
	'idle': {
		'icon': '&#8275',
		'actions': []
	},
	'dying': {
		'icon': '&#9762',
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
		'Start': {
			'icon': '&#9654;',
			'cmd': get_cmd('start', vm['name'])
		},
		'Shutdown': {
			'icon': '&#9209;',
			'cmd': get_cmd('shutdown', vm['id'])
		},
		'Reboot': {
			'icon': '&#10227;',
			'cmd': get_cmd('reboot', vm['id'])
		},
		'Pause': {
			'icon': '&#9208;',
			'cmd': get_cmd('suspend', vm['id'])
		},
		'Resume': {
			'icon': '&#9654;',
			'cmd': get_cmd('resume', vm['id'])
		},
		'Destroy': {
			'icon': '&#9762;',
			'cmd': get_cmd('destroy', vm['id'])
		},
		'View': {
			'icon': '&#128065;',
			'cmd': 'virt-viewer ' + vm['id']
		}
	}

	for action in status[vm['status']]['actions']:
		output += xml_vm_action(actions[action]['icon'], action, actions[action]['cmd'])

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
	label = (status[vm['status']]['icon'] + ' ' if FULL_UNICODE else '' ) + vm['name']
	output = '\t<menu id="' + vm['name'] + '" label="' + label + '">\n'
	output += get_vm_valid_actions(vm)
	output += '\t</menu>\n'
	return output

def xml_vm_action(icon, action, cmd):
	label = (icon + ' ' if FULL_UNICODE else '' ) + action
	output = '\t\t<item label="' + label + '">\n'
	output += '\t\t\t<action name="Execute">\n'
	output += '\t\t\t\t<execute>\n'
	output += '\t\t\t\t\t' + cmd
	output += '\t\t\t\t</execute>\n'
	output += '\t\t\t</action>\n'
	output += '\t\t</item>\n'
	return output

xml = xml_main()
print(xml)
