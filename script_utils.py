#!/usr/bin/env python

import pexpect

def get_password(account, service=None):
    SECURITY = '/usr/bin/security'
    pw_type = 'find-generic-password'
    if service != None:
        pw_type = 'find-internet-password -s {}'.format(service)
    cmd = '{} {} -a {} -w'.format(SECURITY, pw_type, account)
    password = run_command(cmd).rstrip()
    return password

def run_command(command):
    return pexpect.run(command)

