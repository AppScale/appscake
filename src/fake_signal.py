class FakeSignal():
  """
  FakeSignal implements the methods of the signal class that 
  AppScale uses in the AppControllerClient class. The reason we
  have a FakeSignal class is because signal can only run on the
  main thread, and AppsCake does not run the AppScale tools on 
  the main thread.  
  """  
  
  # Class variable that AppScale uses, needs to be mocked out. 
  SIGALRM = 1
 

  @staticmethod
  def alarm(arg1):
    pass
  

  @staticmethod
  def signal(arg1, arg2):
    pass
