"""
test_tagEnforcer.py

Unit tests for tagEnforcerLambda.

Usage:  pytest
"""

import tagEnforcerLambda

tags=['fu','bar']
tagDict={'Name':'testMe'}

def test_checkTags():
    tagEnforcerLambda.violationList = []
    tagEnforcerLambda.checkTags(tagDict, tags, 'testType', 'testName', 'testId')
    assert len(tagEnforcerLambda.violationList) == 2
    assert tagEnforcerLambda.violationList[0]['missingTag'] == 'fu'
    assert tagEnforcerLambda.violationList[1]['missingTag'] == 'bar'
    print (tagEnforcerLambda.violationList)
    
def test_tagEnforcement():
    tagEnforcerLambda.violationList = []
    tagEnforcerLambda.tagEnforcement(tags, '')
    assert len(tagEnforcerLambda.violationList) > 0
    print (tagEnforcerLambda.violationList)