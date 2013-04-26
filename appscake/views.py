""" Views for different pages. """
import logging

from appscake import helpers
from appscake import appscale_tools_thread
from appscake.forms import CommonFields
 
from django.contrib import  messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseServerError
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.utils import simplejson

# When deploying on virtual machines without IaaS support.
CLUSTER_DEPLOY = "cluster"

# When deploying on IaaS.
CLOUD_DEPLOY = "cloud"

# A global variable to store all threads deploying AppScale.
DEPLOYMENT_THREADS = {}

# A global variable to store all threads terminating AppScale.
TERMINATING_THREADS = {}

# Placement stategies for cloud deployments.
SIMPLE_DEPLOYMENT = "simple"
ADVANCE_DEPLOYMENT = "advanced"

def terminate(request):
  """ A request to the terminate page which goes and looks up a currently 
      running deployment and terminates that deployment.
  
  Args:
    request: A Django web request.
  Returns:
    A rendered version of terminate.html with the keyname passed into the 
    javascript.
  """
  get = request.GET.copy()
  if 'keyname' not in get:
    return HttpResponseServerError("Did not receive the keyname of the "\
      "instances to terminate")
  keyname = get['keyname']
  if keyname not in DEPLOYMENT_THREADS:
    return HttpResponseServerError("Unknown keyname of the "\
      "instances to terminate")
  appscale_up_thread = DEPLOYMENT_THREADS[keyname]
  terminate_thread = appscale_tools_thread.AppScaleDown(
    appscale_up_thread.deployment_type, keyname,
    ec2_access=appscale_up_thread.ec2_access, 
    ec2_secret=appscale_up_thread.ec2_secret,
    ec2_url=appscale_up_thread.ec2_url)
  TERMINATING_THREADS[keyname] = terminate_thread
  logging.debug("Starting terminate thread.")
  terminate_thread.start()
  logging.debug("Thread started.")
  return render(request, 'base/terminate.html', {'keyname': keyname})

def home(request):
  """ Render the home page which takes in input from the user to start 
      AppScale. 

  Args:
    request: A Django web request.
  Returns:
    A rendered version of home.html with form fields.
  """
  return render(request, 'base/home.html', {'form': CommonFields()})

def about(request):
  """ Render the about page that tells users about AppsCake. 

  Args:
    request: A Django web request.
  Returns:  
    A rendered version of about.html. 
  """
  return render(request, 'base/about.html')

def get_deployment_status(request):
  """ Returns a json string of the status of the tools being run.

  Args:
    request: A Django web request.
  """
  get = request.GET.copy()
  identifier = None
  if 'keyname' in get:
    identifier = get['keyname']
  else:
    message = {'status': 'error', 'error_message': 
      "Bad JSON request (missing keyname)."}
    return HttpResponse(simplejson.dumps(message))  

  logging.debug("Running keyname {0}".format(DEPLOYMENT_THREADS.keys()))

  if identifier not in DEPLOYMENT_THREADS:
    message = {'status': 'error', 'error_message': 
      "Unknown keyname given {0}.".format(identifier)}
  else:
    message = DEPLOYMENT_THREADS[identifier].get_status()

  return HttpResponse(simplejson.dumps(message))  

def get_termination_status(request):
  """ Returns a json string of the status of the tools being run. """
  get = request.GET.copy()
  identifier = None
  if 'keyname' in get:
    identifier = get['keyname']
  else:
    message = {'status': 'error', 'error_message': 
      "Bad JSON request (missing keyname)."}
    return HttpResponse(simplejson.dumps(message))  

  if identifier not in TERMINATING_THREADS:
    message = {'status': 'error', 'error_message': 
      "Unknown keyname given {0}.".format(identifier)}
  else:
    message = TERMINATING_THREADS[identifier].get_status()

  return HttpResponse(simplejson.dumps(message))  


def start(request):
  """ This is the page a user submits a request to start AppScale. """
  if request.method == 'POST':
    form = CommonFields(data=request.POST)
    appscale_up_thread = None
    email = form['admin_email'].value()
    password = form['admin_pass'].value() or form['cloud_admin_pass'].value()
    assert password != None
    keyname = helpers.generate_keyname()
   
    cloud_type = None
    if 'cluster' in request.POST:
      cloud_type = CLUSTER_DEPLOY
    elif 'cloud' in request.POST:
      cloud_type = CLOUD_DEPLOY

    if cloud_type == CLOUD_DEPLOY:
      infras = form['infrastructure'].value()
      deployment_type = form['deployment_type'].value()
      instance_type = form['instance_type'].value()
      machine = form['machine'].value()
      instance_type = form['instance_type'].value()
      access_key = form['key'].value()
      secret_key = form['secret'].value()
      ec2_url = form['ec2_euca_url'].value()
      if not ec2_url:
        ec2_url = None

      if deployment_type == ADVANCE_DEPLOYMENT:
        ips_yaml = form['ips_yaml'].value()
        appscale_up_thread = appscale_tools_thread.AppScaleUp(cloud_type,
                                   keyname,
                                   email,
                                   password,
                                   placement=ADVANCE_DEPLOYMENT,
                                   machine=machine,
                                   instance_type=instance_type,
                                   infrastructure=infras,
                                   ips_yaml=ips_yaml,
                                   ec2_access=access_key,
                                   ec2_secret=secret_key,
                                   ec2_url=ec2_url)
      elif deployment_type == SIMPLE_DEPLOYMENT:
        min_nodes = form['min'].value()
        max_nodes = form['max'].value()
        appscale_up_thread = appscale_tools_thread.AppScaleUp(cloud_type,
                                   keyname,
                                   email,
                                   password,
                                   placement=SIMPLE_DEPLOYMENT,
                                   machine=machine,
                                   instance_type=instance_type,
                                   infrastructure=infras,
                                   min_nodes=min_nodes,
                                   max_nodes=max_nodes,
                                   ec2_access=access_key,
                                   ec2_secret=secret_key,
                                   ec2_url=ec2_url)
      else:
        return HttpResponseServerError("Unable to get the deployment strategy")
    elif cloud_type == CLUSTER_DEPLOY:
      ips_yaml = form['ips_yaml'].value()
      root_password = form['root_pass'].value()
      appscale_up_thread = appscale_tools_thread.AppScaleUp(cloud_type, 
                                   keyname,  
                                   email,
                                   password,
                                   ips_yaml=ips_yaml,
                                   root_pass=root_password)
    else:
      return HttpResponseServerError(
        "Unable to figure out the type of cloud deployment")  

    appscale_up_thread.start()
    identifier = appscale_up_thread.keyname
    DEPLOYMENT_THREADS[identifier] = appscale_up_thread
    return render(request, 'base/start.html', {'keyname': identifier})
  else:
    return HttpResponseServerError("404 Page not found")
