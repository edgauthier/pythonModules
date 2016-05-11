#!/usr/bin/env python
"""
Runs a series of commands to backup the media folder to an encrypted sparse
bundle attached to this MacBook.
"""

import pexpect
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

    # TODO look at emailing this output
    print output

    # TODO Figure out how to terminate shell from within python
    # exec_command('exit')

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


if __name__ == '__main__':
    main()
