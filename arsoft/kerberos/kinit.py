#!/usr/bin/python
# -*- coding: utf-8 -*-
# kate: space-indent on; indent-width 4; mixedindent off; indent-mode python;

import pexpect
import sys
import os.path

class _kinit_output(object):
    def __init__(self, executable, verbose=False):
        self.executable_names = [ executable, os.path.basename(executable) ]
        self._verbose = False
        self._messages = []
    def write(self, s):
        if self._verbose:
            print(s)
        self._messages.append(s.decode('utf8').strip())
    def flush(self):
        pass

    @property
    def message(self):
        return '\n'.join(self._messages)

    @property
    def last_message(self):
        ret = None
        if self._messages:
            ret = self._messages[-1]
            if ':' in ret:
                (prefix, msg) = ret.split(':', 1)
                if prefix in self.executable_names:
                    ret = msg.strip()
        return ret

def kinit(principal, password, verbose=False, timeout=5, executable='/usr/bin/kinit'):
    ret = False
    if not principal.strip():
        error_message = 'No username specified.'
    elif not password:
        error_message = 'No password entered.'
    else:
        error_message = None
        child = pexpect.spawn(executable, [principal], env={'LANG':'C'}, timeout=5)
        child.logfile = _kinit_output(executable, verbose=verbose)
        if child:
            if child.expect(['[Pp]assword.*:', pexpect.EOF]) == 0:
                child.sendline(password)
                child.wait()
                last_message = child.read().strip().decode('utf8')
                error_message = last_message
                child.close()
                ret = True if child.exitstatus == 0 else False
                if not ret:
                    if ':' in last_message:
                        (status, message) = last_message.split(':', 1)
                        status = status.strip()
                        error_message = message.strip()
            else:
                error_message = child.logfile.last_message
                child.close()
        else:
            error_message = 'Failed to start kpasswd tool.'
    return (ret, error_message)

if __name__ == '__main__':
    x = kinit(sys.argv[1], sys.argv[2], verbose=True)
    print(x)
