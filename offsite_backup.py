#!/usr/bin/env python
"""
Runs a series of commands to backup the media folder to an encrypted sparse
bundle attached to this MacBook.
"""

import pexpect
import smtplib
import json
import os
import string
from getpass import getpass
from script_utils import get_password
from StringIO import StringIO

OFFSITE_BACKUP_DRIVE = '/Volumes/OffsiteBackupDrive'
OFFSITE_BACKUP_IMAGE = 'OffsiteBackup.sparsebundle'
OFFSITE_BACKUP_MOUNT = '/Volumes/OffsiteBackup'
PASSWORD_PROMPT = 'Enter disk image passphrase:'

def main():
    """The main app"""
    password = get_password('offsite_backup')
    output = ""
    output += exec_command('hdiutil attach -stdinpass ' + OFFSITE_BACKUP_DRIVE + '/' + 
                    OFFSITE_BACKUP_IMAGE, password)
    output += exec_command('ssh rounders bin/offsite_backup.sh')
    output += exec_command('hdiutil detach ' + OFFSITE_BACKUP_MOUNT)
    output += exec_command('hdiutil compact -stdinpass ' + OFFSITE_BACKUP_DRIVE + '/' + 
                    OFFSITE_BACKUP_IMAGE, password)
    output += exec_command('hdiutil detach ' + OFFSITE_BACKUP_DRIVE)

    report_results(output)

def exec_command(command, password = None):
    """Executes a command, optionally handling a password prompt"""
    output = StringIO()

    cmd_log = '\n# ' + command + '\n'
    print cmd_log
    if output:
        output.write(cmd_log)

    process = pexpect.spawn(command)
    if password:
        process.expect(PASSWORD_PROMPT)
        process.sendline(password)
    process.logfile = output
    process.interact()

    cmd_output = output.getvalue()
    output.close()

    return cmd_output

def report_results(output):
    config_path = os.path.expanduser("~/.offsite_backup_config.json")

    if not os.path.exists(config_path):
        print "# No config file, skip emailing report"
        return

    with open(config_path) as cfg_file:
        cfg = json.load(cfg_file)
    
    server = cfg['smtp']['server']
    username = cfg['smtp']['username']
    password = cfg['smtp']['password']
    from_addr = cfg['smtp']['from_addr']
    to_addr = cfg['report']['to_addr']
    subject = 'Offsite Backup Report'

    body = string.join((
        'From: {0}'.format(from_addr),
        'To: {0}'.format(to_addr),
        'Subject: {0}'.format(subject),
        '',
        output
        ), "\r\n")

    server = smtplib.SMTP(server)
    server.starttls()
    server.login(username, password)
    server.sendmail(from_addr, [to_addr], body)
    server.quit()

    print output


if __name__ == '__main__':
    main()
