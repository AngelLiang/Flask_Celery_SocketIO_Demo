# coding-utf-8
'''
Run celery as a Windows service

Install:
    pipenv install pywin32

Usage: 
    python celery_service.py install (start / stop / remove)
    
'''

import os
import sys
import time
import shlex
import logging
import subprocess

import win32service
import win32serviceutil
import win32api
import win32con
import win32event


# The directory for celery.log and celery_service.log
# Default: the directory of this script
INSTDIR = os.path.dirname(os.path.realpath(__file__))

# The path of python Scripts
# Usually it is in PYTHON_INSTALL_DIR/Scripts. e.g.
# r'C:\Python27\Scripts'
# If it is already in system PATH, then it can be set as ''
PYTHONSCRIPTPATH = os.path.join(INSTDIR, '.venv', 'Scripts')

# The directory name of project
PROJECTDIR = 'celery_app.celery'

# The logging directory
LOG_DIR = os.path.join(INSTDIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'celery_service.log'),
    level=logging.DEBUG,
    format='[%(asctime)-15s: %(levelname)-7.7s] %(message)s'
)


class CeleryService(win32serviceutil.ServiceFramework):

    _svc_name_ = "Celery"
    _svc_display_name_ = "Celery Distributed Task Queue Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        # create an event that SvcDoRun can wait on and SvcStop can set.
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        logging.info('Stopping {name} service ...'.format(
            name=self._svc_name_))
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        sys.exit()

    def SvcDoRun(self):
        logging.info('Starting {name} service ...'.format(
            name=self._svc_name_))
        os.chdir(INSTDIR)  # so that proj worker can be found
        logging.info('cwd: ' + os.getcwd())
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        command = '"{celery_path}" -A {proj_dir} worker -f "{log_path}" -l info'.format(
            celery_path=os.path.join(PYTHONSCRIPTPATH, 'celery.exe'),
            proj_dir=PROJECTDIR,
            log_path=os.path.join(LOG_DIR, 'celery.log'))
        logging.info('command: ' + command)
        args = shlex.split(command)
        proc = subprocess.Popen(args)
        logging.info('pid: {pid}'.format(pid=proc.pid))
        self.timeout = 3000
        while True:
            rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            if rc == win32event.WAIT_OBJECT_0:
                # stop signal encountered
                # terminate process 'proc'
                PROCESS_TERMINATE = 1
                handle = win32api.OpenProcess(
                    PROCESS_TERMINATE, False, proc.pid)
                win32api.TerminateProcess(handle, -1)
                win32api.CloseHandle(handle)
                break


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(CeleryService)
