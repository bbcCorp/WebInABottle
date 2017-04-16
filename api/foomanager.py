import os
import sys

curpath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(curpath, '..')))


# class: FooManager
class FooManager(object):

    def __init__(self):
        pass

    def getInfo(self):
        '''Get a list of information'''
        return ["Function #1", "Function #2", "Function #3"]