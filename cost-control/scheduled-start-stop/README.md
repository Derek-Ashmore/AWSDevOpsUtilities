# Automated Instance StartUp / Shutdown

## Purpose
This lambda automatically starts and shuts down instances on a scheduled basis. This is useful for
Non-production environments where instances are not needed 24x7x365. Usually, developers are asked to 
"remember" to shut down instances at the end of the day to save costs; manual methods like that 
are unreliable.

## Methodology
**Start/Stop schedule is recorded by tags.** 
| Tag Name | Tag Required | Tax Value Syntax |
| --- |:---:| ---:|
| Scheduled-StartTime | Y | HH:MM - Hours are in 24-hour format (e.g 2pm is 14:00). All time is UTC. |
| Scheduled-StopTime | Y | HH:MM - Hours are in 24-hour format (e.g 4pm is 16:00). All time is UTC. |
| Scheduled-StartStop-Days | N | M,T,W,R,F assumed. First letter of the day except that R=Thursday and U=Sunday. Days are comma-delimited. |

This lambda will examine all isntances within the account and act according to tags. A separate tag enforcement lambda is planned
that will provide notifications for instances with specified tags.

This lambda should be scheduled every minute.

