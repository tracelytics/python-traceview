""" Tracelytics instrumentation API for Python.

Copyright (C) 2012 by Tracelytics, Inc.
All rights reserved.
"""

# defines no-op classes for platforms we don't support building the c extension on
class Metadata(object):
    def __init__(self, _=None):
        pass

    @staticmethod
    def fromString(_):
        return Metadata()

    def createEvent(self):
        return Event()

    @staticmethod
    def makeRandom():
        return Metadata()

    def copy(self):
        return self

    def isValid(self):
        return False

    def toString(self):
        return ''

class Context(object):
    @staticmethod
    def init():
        pass

    @staticmethod
    def get():
        return Metadata()

    @staticmethod
    def set(_):
        pass

    @staticmethod
    def fromString(_):
        return Context()

    @staticmethod
    def copy():
        return Context()

    @staticmethod
    def clear():
        pass

    @staticmethod
    def isValid():
        return False

    @staticmethod
    def toString():
        return ''

    @staticmethod
    def createEvent():
        return Event()

    @staticmethod
    def startTrace(_=None):
        return Event()


class Event(object):
    def __init__(self, _=None, __=None):
        pass

    def addInfo(self, _, __):
        pass

    def addEdge(self, _):
        pass

    def addEdgeStr(self, _):
        pass

    def getMetadata(self):
        return Metadata()

    def metadataString(self):
        return ''

    @staticmethod
    def startTrace(_=None):
        return Event()

class UdpReporter(object):
    def __init__(self, _, __=None):
        pass

    def sendReport(self, _, __=None):
        pass
