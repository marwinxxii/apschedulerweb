<table id=jobs>
  <tr>
    <th class=id>ID</th>
    <th class=job>Job</th>
    <th class=trigger>Trigger</th>
    <th class=args>Args, kwargs</th>
    <th class=runs>Total runs/failed</th>
    <th class=action>Action</th>
  </tr>
  %i = 0
  %for job, jobstore in jobs:
  <tr>
    <td><a href="/job/{{i}}">{{i}}</a></td>
    <td>{{job.name}}</td>
    <td>{{job.trigger}}</td>
    <td>
    %empty = False
    %if job.args:
    args={{job.args}}
    %else:
    %empty=True
    %end
    %if job.kwargs:
    kwargs={{job.kwargs}}
    %else:
    %empty=True
    %end
    %if empty:
      &nbsp;
    %end
    </td>
    <td>{{job.runs}}/{{job.fails}}</td>
    <td>
      %if job.stopped:
      <a href="/job/{{i}}/start">Start</a>
      %else:
      <a href="/job/{{i}}/stop">Stop</a>
      %end
    </td>
  </tr>
  %i+=1
  %end
</table>
%rebase base title='APScheduler web interface'
