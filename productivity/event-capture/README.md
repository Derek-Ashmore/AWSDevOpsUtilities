# Event Capture

## Purpose
This lambda merely reports trigger event content. It's a productivity tool to allow developers
to see the content of a lambda trigger json so they can develop additional lambdas 
to do more useful things.

## Installation

* Create a role for the lambda containing the privileges in this [policy](awsPolicy.json). 
* Create this lambda from the console.
    * Platform = Python 2.7
    * Copy/paste source code:  [eventCapture.py](eventCapture.py)
    * Handler method:  lambda_function.eventCaptureHandler
* If you plan to use a global schedule (recommended), set environment variables listed in the configuration section
* Schedule the lambda using a cron expression (e.g. every day, week, etc.)

## Configuration
* None

## Future Plans
* None

