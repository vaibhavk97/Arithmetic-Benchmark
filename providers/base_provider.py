from abc import ABC

class Model(ABC):
  def __init__(self, name):
    self.name = name
  
  def predict(self, message):
    raise NotImplementedError
  
  