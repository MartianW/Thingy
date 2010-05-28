class ThingyError(Exception):
    "raised whenever something happens that thingy can't handle."
    
class Manual_Action(Exception):
    "raised for actions that have no handler"
    
class Thingy(object):
    pass #TODO
