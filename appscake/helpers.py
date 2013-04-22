""" Helper functions for AppsCake. """
import uuid

def generate_keyname():
  """ Generates a random keyname to use for an AppScale deployment. 
  
  Returns:
    A string which is the name of the AppScale key.
  """
  return str(uuid.uuid1())
