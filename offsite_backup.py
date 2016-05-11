#!/usr/bin/env python
"""
Runs a series of commands to backup the media folder to an encrypted sparse
bundle attached to this MacBook.
"""

import pexpect
from getpass import getpass
from script_utils import get_password

OFFSITE_BACKUP_DRIVE = '/Volumes/OffsiteBackupDrive'
OFFSITE_BACKUP_IMAGE = 'OffsiteBackup.sparsebundle'
OFFSITE_BACKUP_MOUNT = '/Volumes/OffsiteBackup'
PASSWORD_PROMPT = 'Enter disk image passphrase:'

def main():
    """The main app"""
    password = get_password('offsite_backup')
    exec_command('hdiutil attach -stdinpass ' + OFFSITE_BACKUP_DRIVE + '/' + 
                    OFFSITE_BACKUP_IMAGE, password)
    exec_command('ssh rounders bin/offsite_backup.sh')
    exec_command('hdiutil detach ' + OFFSITE_BACKUP_MOUNT)
    exec_command('hdiutil compact -stdinpass ' + OFFSITE_BACKUP_DRIVE + '/' + 
                    OFFSITE_BACKUP_IMAGE, password)
    exec_command('hdiutil detach ' + OFFSITE_BACKUP_DRIVE)
    # exec_command('exit')

def exec_command(command, password = None):
    """Executes a command, optionally handling a password prompt"""
    print '\n# ' + command + '\n'
    process = pexpect.spawn(command)
    if password:
        process.expect(PASSWORD_PROMPT)
        process.sendline(password)
    process.interact()

if __name__ == '__main__':
    main()
