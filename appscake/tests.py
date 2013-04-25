import os
import sys
import unittest
from flexmock import flexmock


sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from appscake import appscale_tools_thread

sys.path.append(os.path.join(os.path.dirname(__file__), "../appscale-tools/lib"))
from appscale_tools import AppScaleTools
import parse_args

class TestCreateInstances(unittest.TestCase):
  def test_constructor(self):
    tools_runner = appscale_tools_thread.\
      ToolsRunner("cloud", "keyname", "a@a.com", "aaaaaa")
    self.assertEquals(appscale_tools_thread.ToolsRunner.INIT_STATE,
      tools_runner.state)

  def test_run(self):
    tools_runner = appscale_tools_thread.\
      ToolsRunner("cloud", "keyname", "a@a.com", "aaaaaa")
    tools_runner = flexmock(tools_runner)
    tools_runner.deployment_type = appscale_tools_thread.ToolsRunner.CLOUD
    tools_runner.placement = appscale_tools_thread.ToolsRunner.SIMPLE
    tools_runner.should_receive("run_simple_cloud_deploy").once()
    tools_runner.should_receive("run_cluster_deploy").never()
    tools_runner.should_receive("run_advance_cloud_deploy").never()
    tools_runner.run()

    tools_runner.should_receive("run_simple_cloud_deploy").never()
    tools_runner.should_receive("run_advance_cloud_deploy").once()
    tools_runner.should_receive("run_cluster_deploy").never()
    tools_runner.placement = appscale_tools_thread.ToolsRunner.ADVANCE
    tools_runner.run()
    
    tools_runner.should_receive("run_simple_cloud_deploy").never()
    tools_runner.should_receive("run_advance_cloud_deploy").never()
    tools_runner.should_receive("run_cluster_deploy").once()
    tools_runner.deployment_type = appscale_tools_thread.ToolsRunner.CLUSTER
    tools_runner.run()

  def test_run_cluster_deploy(self):
    tools_runner = appscale_tools_thread.\
      ToolsRunner("cloud", "keyname", "a@a.com", "aaaaaa")
    tools_runner = flexmock(tools_runner)
    tools_runner.should_receive("run_appscale").once()
    tools_runner.run_cluster_deploy()

  def test_run_advance_cloud_deploy(self):
    tools_runner = appscale_tools_thread.\
      ToolsRunner("cloud", "keyname", "a@a.com", "aaaaaa")
    tools_runner = flexmock(tools_runner)
    tools_runner.should_receive("run_appscale").once()
    tools_runner.run_advance_cloud_deploy()

  def test_run_simple_cloud_deploy(self):
    tools_runner = appscale_tools_thread.\
      ToolsRunner("cloud", "keyname", "a@a.com", "aaaaaa")
    tools_runner = flexmock(tools_runner)
    tools_runner.should_receive("run_appscale").once()
    tools_runner.run_simple_cloud_deploy()

  def test_run_appscale(self):
    tools_runner = appscale_tools_thread.\
      ToolsRunner("cloud", "keyname", "a@a.com", "aaaaaa")
    appscale_tools = flexmock(AppScaleTools)
    fake_args = flexmock(name="FakeArgs").should_receive("args").and_return()
    flexmock(parse_args).should_receive("ParseArgs").and_return(fake_args)
    appscale_tools.should_receive("run_instances").and_return().once()
    tools_runner.run_appscale()

    appscale_tools.should_receive("run_instances").and_raise(SystemExit).once()
    tools_runner.run_appscale()
    self.assertEquals(appscale_tools_thread.ToolsRunner.ERROR_STATE, tools_runner.state)

  class FakeStringIO():
    def __init__(self):
      pass
    def getvalue(self):
      return '\n\n\n'
   
  def test_get_completition_percentage(self):
    tools_runner = appscale_tools_thread.\
      ToolsRunner("cloud", "keyname", "a@a.com", "aaaaaa")
    tools_runner.std_out_capture = self.FakeStringIO()
    self.assertEquals(int(3/tools_runner.EXPECTED_NUM_LINES), 
      tools_runner.get_completion_percentage())

  def test_get_status(self):
    tools_runner = appscale_tools_thread.\
      ToolsRunner("cloud", "keyname", "a@a.com", "aaaaaa")
    self.assertEquals(tools_runner.INIT_STATE, tools_runner.get_status()['status'])
    tools_runner.state = tools_runner.ERROR_STATE
    self.assertEquals(tools_runner.ERROR_STATE, tools_runner.get_status()['status'])
    tools_runner.state = tools_runner.COMPLETE_STATE
    self.assertEquals(tools_runner.COMPLETE_STATE, tools_runner.get_status()['status'])
    tools_runner.state = None
    self.assertEquals("Unknown state", tools_runner.get_status()['error_message'])
    
if __name__ == "__main__":
  unittest.main()
