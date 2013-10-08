#!/usr/bin/python

import subprocess

def asrun(ascript):
    "Run the given AppleScript and return the standard output and error."

    ascript = ascript.encode('utf-8')
    osa = subprocess.Popen(['osascript', '-'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    return osa.communicate(ascript)[0]

def asquote(astr):
    "Return the AppleScript equivalent of the given string."

    # TODO Not sure if this handles backslash characters correctly
    astr = astr.replace('"', '" & quote & "')
    return u'"{}"'.format(astr)

