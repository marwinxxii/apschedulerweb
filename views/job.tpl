<h1>Job #{{job_id}} {{job.name}}</h1>
Func: {{job.func}}<br>
Trigger: {{job.trigger}}<br>
Jobstore: {{jobstore}}<br>
Runs:
<ul>
  <li>Total: {{job.runs}}</li>
  <li>Failed: {{job.fails}}</li>
</ul>
%if log:
<h2>Log of failed runs:</h2>
<table border=1>
  <thead>
    <th class=run_time>schedule run time</th>
    <th class=exception>exception</th>
    <th class=traceback>traceback</th>
  </thead>
  <tbody>
%import traceback
%for entry in log:
<tr>
  <td>{{entry.scheduled_run_time}}</td>
  <td>{{entry.exception}}</td>
  <td>
    %for line in traceback.format_tb(entry.traceback):
    {{line}}<br>
    %end
  </td>
</tr>
%end
</tbody>
</table>
%end
%rebase base title='Job #%i info' % job_id
