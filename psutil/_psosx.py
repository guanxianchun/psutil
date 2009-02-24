#!/usr/bin/env python
# _psosx.py

import os
import signal
import errno

import _psutil_osx

NoSuchProcess = _psutil_osx.NoSuchProcess

class Impl(object):

    def get_process_info(self, pid):
        """Returns a tuple that can be passed to the psutil.ProcessInfo class
        constructor.
        """
        # XXX - figure out why it can't be imported globally (see r54)
        import psutil
        infoTuple = _psutil_osx.get_process_info(pid)
        return psutil.ProcessInfo(*infoTuple)

    def kill_process(self, pid, sig=signal.SIGKILL):
        """Terminates the process with the given PID."""
        # XXX - figure out why it can't be imported globally (see r54)
        import psutil
        if sig is None:
            sig = signal.SIGKILL
        try:
            os.kill(pid, sig)
        except OSError, err:
            if err.errno == errno.ESRCH:
                raise psutil.NoSuchProcess(pid)
            raise

    def get_pid_list(self):
        """Returns a list of PIDs currently running on the system."""
        return _psutil_osx.get_pid_list()

    def pid_exists(self, pid):
        """ Check For the existence of a unix pid."""
        if pid <= 0:
            return False

        try:
            os.kill(pid, 0)
        except OSError, e:
            return e.errno == errno.EPERM
        else:
            return True

