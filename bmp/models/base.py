
class BaseModel(object):

    def __init__(self,submit):
        for k, v in submit.items():
            setattr(self, k, v)
            

