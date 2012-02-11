import signal
import sys

from apscheduler.scheduler import Scheduler
from apscheduler.events import EVENT_JOB_ERROR
import bottle

from bottle.ext.basicauth import BasicAuthPlugin

webapp = {
    }
bottle_config = {
    'host': 'localhost',
    'port': 8080
}
web_config = {
    'users': None, # dict with usernames as keys and passwords as values
    'max_auth_tries': 3, # maximum number of tries before user will be banned
    'max_log_entries': 10 # maximum number of entries saved in log for each job
}

def kill_handler(signum, frame):
    if 'sched' in webapp and webapp['sched'].running:
        webapp['sched'].shutdown()
        sys.exit(0) # stopping server

def parse_config(config, default):
    if config is None:
        config = dict(default)
    else:
        for key, value in default.items():
            if key not in config:
                config[key] = value
    return config

def error_listener(event):
    event.job.fails += 1
    i = 0
    for job, jobstore in webapp['jobs']:
        if job is event.job:
            job_id = i
            break
        i += 1
    log = webapp['logs'].setdefault(job_id, [])
    if len(log) == webapp['max_log_entries']:
        del log[0]
    log.append(event)

def start(sched, bottle_conf=None, **web_conf):
    '''Start scheduler and its web interface.
    :param sched: a Scheduler object.
    :param bottle_conf: dict with configuration passed to bottle.run
    :param **web_conf: params passed to web application
    '''
    global webapp
    bottle_conf = parse_config(bottle_conf, bottle_config)
    webapp = parse_config(web_conf, web_config)
    webapp['sched'] = sched
    for job, jobstore in sched._pending_jobs:
        job.fails = 0
        job.stopped = False
    webapp['jobs'] = list(sched._pending_jobs)
    webapp['logs'] = {}
    sched.add_listener(error_listener, mask=EVENT_JOB_ERROR)
    sched.start()
    if webapp['users'] is not None:
        bottle.install(BasicAuthPlugin(webapp['users'],
                       max_auth_tries=webapp['max_auth_tries']))
    signal.signal(signal.SIGTERM, kill_handler)
    bottle.run(**bottle_conf)
    sched.shutdown()

@bottle.route('/')
def list_jobs():
    return bottle.template('list', jobs=webapp['jobs'])

@bottle.route('/job/<job_id:int>')
def show_job(job_id):
    if job_id >= len(webapp['jobs']) or job_id < 0:
        bottle.abort(text='Incorrect job id', code=400)
    job, jobstore = webapp['jobs'][job_id]
    if job_id in webapp['logs']:
        log = list(webapp['logs'][job_id])
        log.reverse()
    else:
        log = None
    return bottle.template('job', job=job, job_id=job_id,
                           jobstore=jobstore, log=log)

@bottle.route('/job/<job_id:int>/<action>')
def startstop_job(job_id, action):
    if job_id >= len(webapp['jobs']) or job_id < 0:
        bottle.abort(text='Incorrect job id', code=400)
    job, jobstore = webapp['jobs'][job_id]
    sched = webapp['sched']
    if action == 'stop':
        if job.stopped:
            bottle.abort(text='Job is already stopped', code=400)
        sched.unschedule_job(job)
        job.runs = 0
        job.fails = 0
        job.stopped = True
    elif action == 'start':
        if not job.stopped:
            bottle.abort(text='Job is already started', code=400)
        job = sched.add_job(job.trigger, job.func, job.args, job.kwargs,
                            jobstore, name=job.name,
                            max_runs=job.max_runs,
                            max_instances=job.max_instances)
        #TODO should be assigned before job start?
        job.fails = 0
        job.stopped = False
        webapp['jobs'][job_id] = (job, jobstore)
    else:
        bottle.abort(text='Unknown action', code=400)
    #bottle.redirect('/job/%i' % job_id)
    bottle.redirect('/')

@bottle.error
def show_error(error):
    return template('error', error=error)

@bottle.route('/static/<filename:path>', skip='basicauth')
def static(filename):
    return bottle.static_file(filename, root='static')
