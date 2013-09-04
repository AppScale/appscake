""" Thread classes for running the AppScale tools for different types of 
  deployments.
"""
import base64
import logging
import os
import sys
import threading

#  Since AppScake doesn't run the tools on the main thread, use a fake
#  implementation of the signal class.
import fake_signal
sys.modules['signal'] = __import__('fake_signal').FakeSignal

sys.path.append(os.path.join(os.path.dirname(__file__),"../appscale-tools/lib"))
from appscale_tools import AppScaleTools
from custom_exceptions import BadConfigurationException
import parse_args

from cStringIO import StringIO 

# Cluster deployment type. Examples include VirtualBox and KVM.
CLUSTER = "cluster"

# Cloud deployment type. Examples include EC2 and Eucalyptus.
CLOUD = "cloud"

class AppScaleDown(threading.Thread):
  """ Runs terminate instances thread on a currently running AppScale 
  deployment. 
  """

  # Expected number of lines of output from doing appscale-terminate-instances
  # with verbose on.
  EXPECTED_NUM_LINES = 5

  # Initialization state of the AppScaleDown thread. 
  # States are used internally by this class to keep track of where 
  # we are in the process of running appscale-terminate-instances. States are 
  # shared with the web front end in JSON format for the user to know the 
  # current stage of the tools.
  INIT_STATE = "init"

  # When appscale-terminate-instances is currently running.
  TERMINATING_STATE = "terminating"
  
  # When appscale-terminate-instances has successfully terminated.
  TERMINATED_STATE = "terminated"

  # When there was an error when trying to terminate instances.
  ERROR_STATE = "error"

  def __init__(self, deployment_type, keyname, ec2_access=None, 
    ec2_secret=None, ec2_url=None):
    """ A constructor setting up the required arguments for running
    appscale-terminate-instances. Named arguments are for cloud
    deployments.
    
    Args:
      deployment_type: A str, either cloud or cluster deployment.
      keyname: A str, the keyname referencing the deployment to terminate.
      ec2_access: A str, the EC2/Euca access key.
      ec2_secret: A str, the EC2/Euca secret key.
      ec2_url: A str, a URL pointing to where the EC2/Euca cloud is located. 
        (required for Euca).
    """
    threading.Thread.__init__(self)

    self.state = self.INIT_STATE
    self.deployment_type = deployment_type
    self.keyname = keyname
    self.ec2_access = ec2_access
    self.ec2_secret = ec2_secret
    self.ec2_url = ec2_url
    self.err_message = ""
    self.std_out_capture = StringIO()
    self.std_err_capture = StringIO()

  def run(self):
    """ Checks the current state of the thread and terminates AppScale. """
    logging.debug("AppScaleDown thread has started.")
    if self.state != self.INIT_STATE:
      logging.error("Bad state to start terminating instances: {0}.". \
        format(self.state))
    elif not self.appscale_down():
      logging.error("Unable to shut down AppScale.")
    else:
      logging.info("AppScale deployment was successfully terminated.") 
    logging.debug("Thread has stopped.")

  def appscale_down(self):
    """ Terminates a currently running deployment of AppScale. Calls on the 
    AppScale tools by building an argument list, which varies based on 
    the deployment type.
   
    Returns:
      True on success, False otherwise. 
    """
    logging.debug("Starting AppScale down.")
    self.state = self.TERMINATING_STATE

    # We capture the stdout and stderr of the tools and use it to calculate
    # the percentage towards completion.
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = self.std_out_capture
    sys.stderr = self.std_err_capture

    terminate_args = ['--keyname', self.keyname, "--verbose"]

    if self.deployment_type == CLOUD:
      terminate_args.extend(["--EC2_SECRET_KEY", self.ec2_secret,
      "--EC2_ACCESS_KEY", self.ec2_access,
      "--EC2_URL", self.ec2_url])
    try: 
      logging.info("Starting terminate instances.")

      options = parse_args.ParseArgs(terminate_args, 
        "appscale-terminate-instances").args
      AppScaleTools.terminate_instances(options)
      self.state = self.TERMINATED_STATE

      logging.info("AppScale terminate instances successfully ran!")
    except BadConfigurationException as bad_config:
      self.state = self.ERROR_STATE
      logging.exception(bad_config)
      self.err_message = "Bad configuration. Unable to terminate AppScale. " \
        "{0}".format(bad_config)
    except Exception as exception:
      self.state = self.ERROR_STATE
      logging.exception(exception)
      self.err_message = "Exception when terminating: {0}".format(exception)
    finally:
      sys.stdout = old_stdout
      sys.stderr = old_stderr

    return self.state == self.TERMINATED_STATE

  def get_status(self):
    """ Gets the status of the current thread by parsing the output of 
    appscale-terminate-instances. It sets the status and the completion 
    percentage of the command in a dictionary returned to the caller.
  
    Returns:
      A dictionary of the current status of this thread of 
      appscale-terminate-instances.
    """
    status_dict = {'status': self.state, 'percent': 0}
    if self.state == self.INIT_STATE:
      pass
    elif self.state == self.TERMINATING_STATE:
      status_dict['percent'] = self.get_completion_percentage()
    elif self.state == self.TERMINATED_STATE:
      status_dict['percent'] = 100
    else:
      status_dict['error_message'] = "Unknown state"
    return status_dict

  def get_completion_percentage(self):
    """ Gets an estimated percentage of how close to finished we are based
    on the number of lines output by appscale-terminate-instances.
    
    Returns:
      An int, an estimated percentage up to 100.
    """
    logging.debug("Captured tools output thus far: {0}". \
      format(self.std_out_capture.getvalue()))

    count = self.std_out_capture.getvalue().count('\n')
    if count >= self.EXPECTED_NUM_LINES:
      count = self.EXPECTED_NUM_LINES - 1

    percentage = int((float(count)/float(self.EXPECTED_NUM_LINES)) * 100)
    return percentage


class AppScaleUp(threading.Thread):
  """ Runs the AppScale tools command appscale-run-instances to start a new 
  AppScale deployment. 
  """

  # When appscale-run-instances is initializing.
  # States are used internally by this class to keep track of where 
  # we are in the process of running appscale-run-instances. States are 
  # shared with the web front end in JSON format for the user to know the 
  # current stage of the tools.
  INIT_STATE = "initializing"
 
  # When appscale-run-instances in currently running.
  RUNNING_STATE = "running"
 
  # When appscale-run-instances has successfully completed.
  COMPLETE_STATE = "complete"

  # When appscale-run-instances ended in an error state.
  ERROR_STATE = "error"
 
  # Automatic layout of roles in AppScale. User supplies the minimum and 
  # maximum number of nodes.
  SIMPLE = "simple"

  # Manual layout of roles in AppScale. User manually specifies what roles
  # go on which nodes in an ips.yaml configuration.
  ADVANCED = "advanced"

  # Expected number of lines of output from doing appscale-run-instances.
  EXPECTED_NUM_LINES = 17

  # Contents of the line which contains the status link from the tools output.
  STATUS_LINK_LINE = "View status information about your AppScale deployment at"

  # The default location URL for EC2.
  EC2_URL_DEFAULT = "https://ec2.us-east-1.amazonaws.com"

  def __init__(self, deployment_type, keyname, admin_email, admin_pass, 
    root_pass=None, placement=None, infrastructure=None, min_nodes=None, 
    max_nodes=None, machine=None, instance_type=None, ips_yaml=None, 
    ec2_secret=None, ec2_access=None, ec2_url=None):
    """ A constructor setting up the required arguments for running
    appscale-run-instances. 
    
    Args:
      deployment_type: A str, the deployment type of either cloud or cluster.
      keyname: A str representing the keyname used for an AppScale deployment.
      admin_email: A str, email for the administrator.
      admin_pass: A str, password for the administrator.
      root_pass: A str, the root password of the appscale image.
      placement: A str, of either automatic placement or manual.
      infrastructure: A str, the IaaS we're deploying on ('ec2' or 'euca').
      max_nodes: An int, the maximum number of nodes AppScale can run.
      min_nodes: An int, the minimum number of nodes AppScale can run.
      machine: A str representing the emi or ami identifier of the cloud image 
        to use.
      instance_type: A str, the instance size to use when starting up VMs.
      ips_yaml: A str, of the contents of the ips.yaml file.
      ec2_secret: A str, the EC2 secret key for EC2 and Euca.
      ec2_access: A str, the EC2 access key for EC2 and Euca.
      ec2_url: A str, the EC2 URL location for EC2 and Euca.
    """
    threading.Thread.__init__(self)

    logging.basicConfig(format='%(asctime)s %(levelname)s %(filename)s:' \
      '%(lineno)s %(message)s ', level=logging.INFO)

    self.keyname = keyname
    self.admin_email = admin_email
    self.admin_pass = admin_pass
    self.deployment_type = deployment_type # cloud or cluster
    self.placement = placement # simple or advance
    self.max_nodes = max_nodes
    self.machine = machine
    self.infrastructure = infrastructure
    self.instance_type = instance_type
    self.ec2_secret = ec2_secret
    self.ec2_access = ec2_access

    self.ec2_url = ec2_url
    if not ec2_url:
      self.ec2_url = self.EC2_URL_DEFAULT

    self.ips_yaml = ips_yaml
    self.ips_yaml_b64 = None
    if ips_yaml:
      self.ips_yaml_b64 = base64.b64encode(str(ips_yaml))

    self.std_out_capture = StringIO()
    self.std_err_capture = StringIO()
    self.state = self.INIT_STATE
    self.err_message = "" 
    self.args = ['--table', 'cassandra']
    self.args.extend(["--admin_user", self.admin_email,
                      "--admin_pass", self.admin_pass,
                      "--keyname", self.keyname])
    self.link = None
    self.root_pass = root_pass

    logging.debug("Initial arguments: {0}".format(self.args))
 
  def run(self):
    """ Checks the current state of an AppScale deployment and starts a 
    deployment if in the correct state. 
    """
    if self.state != self.INIT_STATE:
      logging.error("Bad state to start a new thread for AppScaleUp.")
    elif not self.appscale_up():
      logging.error("Unable to start AppScale.")
    else:
      logging.info("AppScale was successfully deployed!")
    logging.debug("Thread has stopped.")

  def appscale_up(self): 
    """ Starts up an AppScale deployment. Checks the type of deployment
    and placement strategy and calls on the correct initialization 
    procedure.

    Returns:
      True on success, False otherwise.
    Raises:
      NotImplementedError: If there is an unknown placement or deployment.
    """
    self.state = self.RUNNING_STATE

    if self.deployment_type == CLOUD:
      if self.placement == self.SIMPLE:
        return self.run_simple_cloud_deploy()
      elif self.placement == self.ADVANCED:
        return self.run_advance_cloud_deploy()
      else:
        raise NotImplementedError("Unknown placement of {0}". \
          format(self.placement))
    elif self.deployment_type == CLUSTER:
      return self.run_cluster_deploy()
    else:
      raise NotImplementedError("Unknown deployment of {0}".format(
        self.deployment_type)) 

  def run_add_keypair(self):
    """ Sets up the add keypair arguments and attempts to add the
    keyname generated.

    Returns:
      True on success, False otherwise.
    """
    self.state = self.INIT_STATE
    add_keypair_args = ['--keyname', self.keyname, '--ips_layout', 
      self.ips_yaml_b64, "--root_password", self.root_pass, "--auto"]
    options = parse_args.ParseArgs(add_keypair_args, "appscale-add-keypair"). \
      args
    try:
      AppScaleTools.add_keypair(options)
      logging.info("AppScale add key pair was successful")
    except BadConfigurationException as bad_config:
      self.state = self.ERROR_STATE
      logging.error(str(bad_config))
      self.err_message = "Bad configuration. Unable to set up keypairs."
      return False
    except Exception as exception:
      self.state = self.ERROR_STATE
      logging.exception(exception)
      self.err_message = "Exception when running add key pair: {0}". \
        format(exception)
      return False
    return True

  def run_cluster_deploy(self):
    """ Sets up deployment arguments of a cluster start up.
  
    Returns:
      True on success, False otherwise.
    """
    self.args.extend(["--ips_layout", self.ips_yaml_b64])
    if self.run_add_keypair():
      return self.run_appscale()
    else:
      return False

  def run_advance_cloud_deploy(self):
    """ Sets up deployment arguments of an advance cloud layout and 
    starts up AppScale.
  
    Returns:
      True on success, False otherwise.
    """
    self.args.extend(["--infrastructure", str(self.infrastructure), 
                      "--machine", self.machine,  
                      "--ips_layout", self.ips_yaml_b64,
                      "--group", self.keyname,
                      "--EC2_SECRET_KEY", self.ec2_secret,
                      "--EC2_ACCESS_KEY", self.ec2_access,
                      "--EC2_URL", self.ec2_url])
    return self.run_appscale()

  def run_simple_cloud_deploy(self):
    """ Sets up deployment arguments of a simple cloud layout and 
    starts up AppScale.
  
    Returns:
      True on success, False otherwise.
    """
    self.args.extend(["--infrastructure", str(self.infrastructure),
                      "--machine", self.machine,  
                      "--max", self.max_nodes,
                      "--group", self.keyname,
                      "--EC2_SECRET_KEY", self.ec2_secret,
                      "--EC2_ACCESS_KEY", self.ec2_access,
                      "--EC2_URL", self.ec2_url])
    return self.run_appscale()

  def run_appscale(self):
    """ Executes the appscale tools with deployment specific arguments.

    Returns:
      True on success, False otherwise.
    """
    logging.info("Tools arguments: {0}".format(str(self.args)))

    self.state = self.RUNNING_STATE
    old_stdout = sys.stdout
    old_stderr = sys.stderr

    try:
      options = parse_args.ParseArgs(self.args, "appscale-run-instances").args
      sys.stdout = self.std_out_capture
      sys.stderr = self.std_err_capture

      AppScaleTools.run_instances(options)
      logging.info("AppScale run instances was successful!")
      self.state = self.COMPLETE_STATE 
      self.set_status_link()
    except BadConfigurationException as bad_config:
      self.state = self.ERROR_STATE
      logging.exception(bad_config)
      self.err_message = "Bad configuration. {0}".format(bad_config)
    except Exception as exception:
      self.state = self.ERROR_STATE
      logging.exception(exception)
      self.err_message = "Exception--{0}".format(exception)
    except SystemExit as sys_exit:
      self.state = self.ERROR_STATE
      logging.error(str(sys_exit))
      self.err_message = str("Error with given arguments caused system exit.")
    finally:
      sys.stdout = old_stdout
      sys.stderr = old_stderr
 
    return self.state == self.COMPLETE_STATE

  def set_status_link(self):
    """ Parses the output of the tools and sets the status link. """
    lines = self.std_out_capture.getvalue().split('\n')
    for line in lines:
      if self.STATUS_LINK_LINE in line:
        self.link = line.split(' ')[-1]
        self.link = self.link.split('status')[0]
        logging.info("AppScale status link: {0}".format(self.link))
        return
  
  def get_completion_percentage(self):
    """ Gets an estimated percentage of how close to finished we are based
    on the number of lines output by appscale-run-instances.
    
    Returns:
      An int, an estimated percentage up to 100.
    """
    logging.debug("Captured tools output thus far: {0}". \
      format(self.std_out_capture.getvalue()))

    count = self.std_out_capture.getvalue().count('\n')
    if count >= self.EXPECTED_NUM_LINES:
      count = self.EXPECTED_NUM_LINES - 1

    percentage = int((float(count)/float(self.EXPECTED_NUM_LINES)) * 100)
    return percentage

  def get_status(self):
    """ Sees what the current status of an AppScale deployment is.
  
    Returns:
      A dictionary of the current status of this thread of 
      appscale-run-instances. Includes the state of the tools and 
      additional information depending on the current state.
    """
    status_dict = {'status': self.state, 'percent': 0}
    if self.state == self.INIT_STATE:
      pass
    elif self.state == self.ERROR_STATE:
      status_dict['error_message'] = self.err_message
    elif self.state == self.RUNNING_STATE:
      status_dict['percent'] = self.get_completion_percentage()
    elif self.state == self.COMPLETE_STATE:
      status_dict['percent'] = 100 
      status_dict['link'] = self.link
    else:
      status_dict['error_message'] = "Unknown state"
    return status_dict
