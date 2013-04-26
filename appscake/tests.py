import os
import sys
import unittest
from flexmock import flexmock


sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from appscake import appscale_tools_thread

sys.path.append(os.path.join(os.path.dirname(__file__), "../appscale-tools/lib"))
from appscale_tools import AppScaleTools
from custom_exceptions import BadConfigurationException
import parse_args

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
    flexmock(appscale_thread).should_receive("stdout_capture.getvalue.count").\
      and_return(appscale_thread.EXPECTED_NUM_LINES).once()
    self.assertEquals(94, appscale_thread.get_completition_percentage())
      
if __name__ == "__main__":
  unittest.main()
