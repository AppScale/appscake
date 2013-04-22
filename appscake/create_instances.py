""" Methods for running the appscale-run-instances command for different
    types of deployments.
"""
import argparse
import base64
import os
import random
import sys
import threading

sys.path.append(os.path.join(os.path.dirname(__file__),"../appscale-tools/lib"))
from appscale_tools import AppScaleTools

from cStringIO import StringIO 
from parse_args import ParseArgs

class ToolsRunner(threading.Thread):

  # When appscale-run-instances ended in an error state.
  ERROR_STATE = "error"
  
  # When appscale-run-instances in currently running.
  RUNNING_STATE = "running"
 
  # When appscale-run-instances is initializing.
  INIT_STATE = "initializing"

  # When appscale-run-instances has successfully completed.
  COMPLETE_STATE = "complete"

  # Automatic layout of roles in AppScale.
  SIMPLE = "simple"

  # Manual layout of roles in AppScale.
  ADVANCE = "advance"

  # Cluster type deployment.
  CLUSTER = "cluster"

  # Cloud type deployment.
  CLOUD = "cloud"

  # Default args given to the tools.
  DEFAULT_ARGS = ['--table', 'cassandra']

  # Expected number of lines of output from doing appscale-run-instances.
  EXPECTED_NUM_LINES = 17

  def __init__(self, deployment_type, keyname, admin_email, admin_pass, 
    placement=SIMPLE, min_nodes=None, max_nodes=None, machine=None, 
    instance_type=None, ips_yaml=None, ec2_secret=None, ec2_access=None):
    """ Constructor. 
    
    Args:
      deployment_type: A str, the deployment type of either cloud or cluster.
      keyname: A str representing the keyname used for an AppScale
        deployment.
      admin_email: A str, email for the administrator.
      admin_pass: A str, password for the administrator.
      placement: A str, of either automatic placement or manual.
      max_nodes: An int, the maximum number of nodes AppScale can run.
      min_nodes: An int, the minimum number of nodes AppScale can run.
      machine: A str representing the emi or ami identifier of the cloud image 
        to use.
      infrastructure: A str, the infrastructure used (ec2, euca, etc.).
      instance_type: A str, the instance size to use when starting up VMs.
      ips_yaml: A str, of the contents of the ips.yaml file.
      ec2_secret: A str, the EC2 secret key for EC2 and Euca.
      ec2_access: A str, the EC2 access key for EC2 and Euca.
    """
    threading.Thread.__init__(self)
    self.keyname = keyname
    self.admin_email = admin_email
    self.admin_pass = admin_pass
    self.deployment_type = deployment_type #cloud or cluster
    self.placement = placement #simple or advance
    self.min_nodes = min_nodes
    self.max_nodes = max_nodes
    self.machine = machine
    self.infrastructure = infrastructure
    self.instance_type = instance_type
    self.ec2_secret = ec2_secret
    self.ec2_access = ec2_access
    self.ips_yaml = ips_yaml
    self.ips_yaml_b64 = None
    if ips_yaml:
      self.ips_yaml_b64 = base64.b64encode(ips_yaml)

    self.std_in_capture = cStringIO.StringIO()
    self.std_err_capture = cStringIO.StringIO()
    self.status = INIT_STATE
    self.err_message = ""
    self.args = DEFAULT_TOOLS_ARGS
    self.args.extend(["--admin_email", self.admin_email,
                      "--admin_pass", self.admin_pass,
                      "--keyname", self.keyname])
  def run(self):
    """ The initial function called when starting a tools runner thread. """
    self.status = RUNNING_STATE

    if self.deployment_type == CLOUD:
      if self.placement == SIMPLE:
        self.run_simple_cloud_deploy()
      elif self.placement == ADVANCE:
        self.run_advance_cloud_deploy()
      else:
        raise NotImplemented("Unknown placement of {0}".format(self.placement))
    elif self.deployment_type == CLUSTER:
      self.run_cluster_deploy()
    else:
      raise NotImplemented("Unknown deployment of {0}".format(self.deployment_type)) 

  def run_cluster_deploy(self):
    """ Sets up deployment of a cluster and runs the appscale tools. """
    self.args.extend(["--ips_layout", self.ips_yaml_b64])
    self.run_appscale()

  def run_advance_cloud_deploy(self):
    """ Sets up deployment of an advance cloud layout and runs the appscale tools.
    """
    self.args.extend(["--infrastructure", self.infrastructure, 
                      "--machine", self.machine,  
                      "--ips_layout", self.ips_yaml_b64,
                      "--ec2_access", self.ec2_access,
                      "--ec2_secret", self.ec2_secret])
    self.run_appscale()

  def run_simple_cloud_deploy(self):
    """ Sets up deployment of a simple cloud layout and runs the appscale tools. """
    self.args.extend(["--infrastructure", self.infrastructure, 
                      "--machine", self.machine,  
                      "--min", self.min_nodes,
                      "--max", self.max_nodes,
                      "--ec2_access", self.ec2_access,
                      "--ec2_secret", self.ec2_secret])
    self.run_appscale()

  def run_appscale(self):
    """ Exectutes the appscale tools once the configuration has been set. """
    self.status = RUNNING_STATE
    options = ParseArgs(self.args, "appscale-run-instances").args

    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = self.std_out_capture
    sys.stderr = self.std_err_capture

    try:
      AppScaleTools.run_instances(options)
    except Exception as e:
      self.status = ERROR_STATE
      self.err_message = str(e)
    finally:
      sys.stdout = old_stdout
      sys.stderr = old_stderr

  def get_completion_percentage(self):
    """ Gets an estimated percentage of how close to finished we are based
        on the number of lines output by appscale-run-instances.
    
    Returns:
      An int, an estimated percentage up to 100.
    """
    count = self.std_out_capture.getvalue().count('\n')
    if count >= EXPECTED_NUM_LINES:
      count = EXECTED_NUM_LINES - 1
    percentage = int((count/EXPECTED_NUM_LINES) * 100)
    return percentage

  def get_status(self):
    """ Parses the output of appscale-run-instances and sees what the current 
        status of a running command is.
  
    Returns:
      A json string of the current status of this thread of run-instances.
    """
    status_dict['status'] = self.status
    status_dict['percent'] = 0
    if self.status == INIT_STATE:
      pass
    elif self.status == ERROR_STATE:
      status_dict['error_message'] = self.err_message
    elif self.status == RUNNING_STATE:
      status_dict['percent'] = self.get_completion_percentage()
    elif self.status == COMPLETE_STATE:
      status_dict['percent'] = 100 
    else:
      status_dict['error_message'] = "Unknown state"
    return status_dict
