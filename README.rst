===============
APScheduler-Web
===============

`apscheduler <https://bitbucket.org/agronholm/apscheduler>`_ + `bottle <https://github.com/defnull/bottle>`_ = apschedulerweb

This is a web interface for Advanced Python Scheduler. It provides
functionality for managing jobs added to scheduler, such as:
  - Stopping/starting jobs
  - Viewing logs of failed runs

Requirements
============

Python 2.7+, bottle, apscheduler

Usage
=====

The only thing you need to do is pass ``Scheduler`` object and config
options to ``start`` function of ``apschedulerweb`` module.
::
    from apschedulerweb import start
    from apscheduler.scheduler import Scheduler

    s = Scheduler()
    def printer(s):
    	print(s)
    
    s.add_interval_job(printer, args=['hello'], seconds=5)
    start(s, users={'user':'pass'})

Also you can write configuration file and run directly apschedulerweb module.
``example.json``::
    
    {
      "web": {
        "users": {
          "user": "pass"
        },
        "user": "alex",
        "pid_file": "example.pid",
        "max_log_entries": 5,
        "max_auth_tries": 3
      },
      "bottle": {
        "host": "localhost",
        "port": 8080
      },
      "jobs": [
        {
          "file": "example.py",
          "func": "printer",
	  "trigger": "interval",
          "args": ["hello"],
          "seconds": 5
        }
      ]
    }
    
``example.py``::
    
    def printer(s):
        print(s)

and then run ``python -m apschedulerweb --conf=example.json``
