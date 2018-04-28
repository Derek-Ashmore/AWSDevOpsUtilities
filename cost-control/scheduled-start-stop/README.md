# Automated Instance StartUp / Shutdown

## Purpose
This lambda automatically starts and shuts down instances on a scheduled basis. This is useful for
Non-production environments where instances are not needed 24x7x365. Usually, developers are asked to 
"remember" to shut down instances at the end of the day to save costs; manual methods like that 
are unreliable.

## Installation

* Create a role for the lambda containing the privileges in this [policy](awsPolicy.json). 
* Create this lambda from the console.
    * Platform = Python 2.7
    * Copy/paste source code:  [instanceStartStopLambda.py](instanceStartStopLambda.py)
    * Handler method:  lambda_function.startStopHandler
* If you plan to use a global schedule (recommended), set environment variables listed in the configuration sectioon
* Schedule the lambda using a cron expression (e.g. every minute, five minutes, etc.)

Note:  You may need to adjust the timeout from the default if you've many instances to manage.

## Configuration
**Global Start/Stop schedule is recorded by environment variable settings.** 

| Environment Variable Name | Value Required | Value Syntax |
| --- |:---:| ---:|
| Scheduled_StartTime | N | HH:MM - Hours are in 24-hour format (e.g 2pm is 14:00). All time is UTC. |
| Scheduled_StopTime | N | HH:MM - Hours are in 24-hour format (e.g 4pm is 16:00). All time is UTC. |
| Scheduled_StartStop_Days | N | M,T,W,R,F assumed. First letter of the day except that R=Thursday and U=Sunday. Days are comma-delimited. |

**Individual Start/Stop schedule is recorded by instance tags.** 

| Tag Name | Tag Required | Tag Value Syntax |
| --- |:---:| ---:|
| Scheduled_StartTime | Y | HH:MM - Hours are in 24-hour format (e.g 2pm is 14:00). All time is UTC. |
| Scheduled_StopTime | Y | HH:MM - Hours are in 24-hour format (e.g 4pm is 16:00). All time is UTC. |
| Scheduled_StartStop_Days | N | M,T,W,R,F assumed. First letter of the day except that R=Thursday and U=Sunday. Days are comma-delimited. |

This lambda will examine all instances within the account and act according to tags. A separate tag enforcement lambda is planned
that will provide notifications for instances with specified tags.

This lambda should be scheduled every minute.

## Future Plans
* Add ability to specify the time zone used.

