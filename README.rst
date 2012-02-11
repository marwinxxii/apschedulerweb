===============
APScheduler-Web
===============

`apscheduler <https://bitbucket.org/agronholm/apscheduler>`_ + `bottle <https://github.com/defnull/bottle>`_ = apschedulerweb

This is a web interface for Advanced Python Scheduler. It provides
functionality for managing jobs added to scheduler, such as:
  - Stopping/starting jobs
  - Viewing logs of failed runs

Usage
=====

The only thing you need to do is pass ``Scheduler`` object and config
options to ``start`` function of ``apschedulerweb`` module.
::
    from apschedulerweb import start
    from apscheduler.scheduler import Scheduler

    s=Scheduler()
    def printer(s):
    	print(s)
    
    s.add_interval_job(printer, args=['hello'], seconds=5)
    start(s, users={'user':'pass'})
