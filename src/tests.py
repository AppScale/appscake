import os
import sys
import unittest
from flexmock import flexmock


sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import appscale_tools_thread

sys.path.append(os.path.join(os.path.dirname(__file__), "../appscale-tools/lib"))
from appscale_tools import AppScaleTools
from custom_exceptions import BadConfigurationException
import parse_args


class FakeIOString():
  def __init__(self):
    pass
  def getvalue(self):
    return "\n\n\n"

class TestAppScaleDown(unittest.TestCase):
  def test_constructor(self):
    appscale_down = appscale_tools_thread.\
      AppScaleDown("cloud", "keyname")
    self.assertEquals(appscale_tools_thread.AppScaleDown.TERMINATING_STATE,
      appscale_down.state)

  def test_run(self):
    appscale_thread = appscale_tools_thread.AppScaleDown("cloud", "keyname")
    flexmock(appscale_thread).should_receive("appscale_down").\
      and_return(True).once()
    appscale_thread.run()
  
  def test_appscale_down(self):
    appscale_thread = appscale_tools_thread.\
      AppScaleDown("cluster", "keyname")

    fake_args = flexmock(name="FakeArgs").should_receive("args").and_return()
    flexmock(parse_args).should_receive("ParseArgs").and_return(fake_args)
    appscale_tools = flexmock(AppScaleTools)
    appscale_tools.should_receive("terminate_instances").and_return().once()

    self.assertEquals(True, appscale_thread.appscale_down())

    appscale_tools.should_receive("terminate_instances").and_raise(
      BadConfigurationException).once()
    self.assertEquals(False, appscale_thread.appscale_down())

    appscale_tools.should_receive("terminate_instances").and_raise(
      Exception).once()
    self.assertEquals(False, appscale_thread.appscale_down())

  def test_get_status(self):
    appscale_thread = appscale_tools_thread.AppScaleDown("cloud", "keyname")
    percent = 10
    flexmock(appscale_thread).should_receive("get_completion_percentage").\
      and_return(percent).once()
    self.assertEquals({'status':'terminating', 'percent':percent}, appscale_thread.get_status())
   
  def test_completion_percentage(self):
    appscale_thread = appscale_tools_thread.AppScaleDown("cloud", "keyname")
    appscale_thread.std_out_capture = FakeIOString()
    self.assertEquals(60, appscale_thread.get_completion_percentage())

class TestAppScaleUp(unittest.TestCase):
  def test_constructor(self):
    appscale_up = appscale_tools_thread.\
      AppScaleUp("cloud", "keyname", "a@a.com", "aaaaaa")
    self.assertEquals(appscale_tools_thread.AppScaleUp.INIT_STATE,
      appscale_up.state)

  def test_run(self):
    appscale_up = appscale_tools_thread.\
      AppScaleUp("cloud", "keyname", "a@a.com", "aaaaaa")
    flexmock(appscale_up).should_receive("appscale_up").and_return(True).\
      once()
    appscale_up.run()

  def test_appscale_up(self):
    appscale = appscale_tools_thread.\
      AppScaleUp("cloud", "keyname", "a@a.com", "aaaaaa")
    flexmock(appscale).should_receive("run_simple_cloud_deploy").and_return(True).\
      once()
    appscale.placement = appscale.SIMPLE
    self.assertEquals(True, appscale.appscale_up())

    appscale.placement = appscale.ADVANCE
    flexmock(appscale).should_receive("run_simple_cloud_deploy").and_return(True).\
      never()
    flexmock(appscale).should_receive("run_advance_cloud_deploy").and_return(True).\
      once()
    self.assertEquals(True, appscale.appscale_up())
 
    appscale.placement = "some_unknown_state" 
    self.assertRaises(NotImplementedError, appscale.appscale_up)
 
    appscale.deployment_type = appscale_tools_thread.CLUSTER
    appscale.placement = "test dont care"
    flexmock(appscale).should_receive("run_advance_cloud_deploy").and_return(True).\
      never()
    flexmock(appscale).should_receive("run_cluster_deploy").and_return(True).\
      once()
    self.assertEquals(True, appscale.appscale_up()) 

    appscale.deployment_type = "some crazy deployment"
    flexmock(appscale).should_receive("run_cluster_deploy").and_return(True).\
      never()
    self.assertRaises(NotImplementedError, appscale.appscale_up)

  def test_run_addkeypair(self):
    appscale = appscale_tools_thread.\
      AppScaleUp("cloud", "keyname", "a@a.com", "aaaaaa")
    class Args():
      def __init__(self):
        self.args = None
    flexmock(parse_args).should_receive("ParseArgs").and_return(Args()).once()
    flexmock(AppScaleTools).should_receive("add_keypair").once()
    self.assertEquals(True, appscale.run_add_keypair())

    flexmock(parse_args).should_receive("ParseArgs").and_return(Args()).once()
    flexmock(AppScaleTools).should_receive("add_keypair").\
      and_raise(BadConfigurationException).once()
    self.assertEquals(False, appscale.run_add_keypair())

    flexmock(parse_args).should_receive("ParseArgs").and_return(Args()).once()
    flexmock(AppScaleTools).should_receive("add_keypair").\
      and_raise(Exception).once()
    self.assertEquals(False, appscale.run_add_keypair())
  
  def test_run_cluster_deploy(self):
    appscale = appscale_tools_thread.\
      AppScaleUp("cloud", "keyname", "a@a.com", "aaaaaa")
    flexmock(appscale).should_receive("run_add_keypair").and_return(True).once()
    flexmock(appscale).should_receive("run_appscale").and_return(True).once()
    self.assertEquals(True, appscale.run_cluster_deploy())
    
    flexmock(appscale).should_receive("run_add_keypair").and_return(False).once()
    flexmock(appscale).should_receive("run_appscale").and_return(True).never()
    self.assertEquals(False, appscale.run_cluster_deploy())

    flexmock(appscale).should_receive("run_add_keypair").and_return(True).once()
    flexmock(appscale).should_receive("run_appscale").and_return(False).once()
    self.assertEquals(False, appscale.run_cluster_deploy())

  def test_run_advance_cloud_deploy(self):
    appscale = appscale_tools_thread.\
      AppScaleUp("cloud", "keyname", "a@a.com", "aaaaaa")
    flexmock(appscale).should_receive("run_appscale").and_return(True).once()
    self.assertEquals(True, appscale.run_advance_cloud_deploy())

  def test_run_simple_cloud_deploy(self):
    appscale = appscale_tools_thread.\
      AppScaleUp("cloud", "keyname", "a@a.com", "aaaaaa")
    flexmock(appscale).should_receive("run_appscale").and_return(True).once()
    self.assertEquals(True, appscale.run_simple_cloud_deploy())

  def test_run_appscale(self):
    appscale = appscale_tools_thread.\
      AppScaleUp("cloud", "keyname", "a@a.com", "aaaaaa")
    class Args():
      def __init__(self):
        self.args = None
    flexmock(appscale).should_receive("set_status_link").once()
    flexmock(parse_args).should_receive("ParseArgs").and_return(Args())
    flexmock(AppScaleTools).should_receive("run_instances").once()
    self.assertEquals(True, appscale.run_appscale())

    flexmock(AppScaleTools).should_receive("run_instances").and_raise(
      BadConfigurationException).once()
    flexmock(appscale).should_receive("set_status_link").never()
    self.assertEquals(False, appscale.run_appscale())
    
    flexmock(AppScaleTools).should_receive("run_instances").and_raise(
      Exception).once()
    flexmock(appscale).should_receive("set_status_link").never()
    self.assertEquals(False, appscale.run_appscale())
      
    flexmock(AppScaleTools).should_receive("run_instances").and_raise(
      SystemExit).once()
    flexmock(appscale).should_receive("set_status_link").never()
    self.assertEquals(False, appscale.run_appscale())

  def test_get_status(self):
    appscale = appscale_tools_thread.\
      AppScaleUp("cloud", "keyname", "a@a.com", "aaaaaa")
    self.assertEquals({'status': 'initializing', 'percent': 0}, appscale.get_status())

    appscale.state = appscale.ERROR_STATE
    self.assertEquals({'status': 'error', 'error_message' : "", 'percent': 0}, appscale.get_status())

    appscale.state = appscale.RUNNING_STATE
    flexmock(appscale).should_receive("get_completion_percentage").and_return(10)
    self.assertEquals({'status': 'running', 'percent': 10}, appscale.get_status())

    appscale.state = appscale.COMPLETE_STATE
    self.assertEquals({'status': 'complete', 'link': None, 'percent': 100}, appscale.get_status())
  
    
if __name__ == "__main__":
  unittest.main()
