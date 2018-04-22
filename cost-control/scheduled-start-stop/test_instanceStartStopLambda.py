"""
test_instanceStartStopLambda.py

Unit tests for instanceStartStopLambda.

Usage:  pytest
"""

import instanceStartStopLambda
import datetime
import json

currentDateTime = datetime.datetime(year=2018, month=4, day=22, hour=22, minute=0) 

def test_int2Weekday():
    assert instanceStartStopLambda.int2Weekday(0) == 'M'
    assert instanceStartStopLambda.int2Weekday(1) == 'T'
    assert instanceStartStopLambda.int2Weekday(2) == 'W'
    assert instanceStartStopLambda.int2Weekday(3) == 'R'
    assert instanceStartStopLambda.int2Weekday(4) == 'F'
    assert instanceStartStopLambda.int2Weekday(5) == 'S'
    assert instanceStartStopLambda.int2Weekday(6) == 'U'
    
def test_matchesDaySpec(): 
    assert not instanceStartStopLambda.matchesDaySpec(currentDateTime, 'M,T,W,R,F')
    assert instanceStartStopLambda.matchesDaySpec(currentDateTime, 'M,T,W,R,F,U')
    assert instanceStartStopLambda.matchesDaySpec(currentDateTime, 'M,U ,T,W,R,F')
    
def test_matchesTimeSpec(): 
    assert not instanceStartStopLambda.matchesTimeSpec(currentDateTime, '22:05')
    assert not instanceStartStopLambda.matchesTimeSpec(currentDateTime, '21:00')
    assert instanceStartStopLambda.matchesTimeSpec(currentDateTime, '22:00')
    
def test_datetimeMatches(): 
    assert not instanceStartStopLambda.datetimeMatches(currentDateTime, '22:05', 'M,T,W,R,F')
    assert not instanceStartStopLambda.datetimeMatches(currentDateTime, '22:00', 'M,T,W,R,F')
    assert not instanceStartStopLambda.datetimeMatches(currentDateTime, '22:05', 'M,T,W,R,F,U')
    assert instanceStartStopLambda.datetimeMatches(currentDateTime, '22:00', 'M,T,W,R,F,U')
    
def test_findAllEc2Instances(): 
    instanceList = instanceStartStopLambda.findAllEc2Instances()
    print("instanceList = {}").format(instanceList[0])
    assert False