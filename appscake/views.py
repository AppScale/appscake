""" Views for different pages. """
import logging

from appscake import helpers
from appscake import create_instances
from appscake.forms import CommonFields
from appscake.forms import Cluster
 
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

# A global variable to store all threads running the tools.
ALL_THREADS = {}

# Placement stategies for cloud deployments.
SIMPLE_DEPLOYMENT = "simple"
ADVANCE_DEPLOYMENT = "advance"

def home(request):
  return render(request, 'base/home.html', {'form': CommonFields(),})

def about(request):
  return render(request, 'base/about.html')

def get_status(request):
  """ Returns a json string of the status of the tools being run. """
  logging.error("Get status")
  get = request.GET.copy()
  identifier = None
  if 'keyname' in get:
    identifier = get['keyname']
  else:
    message = { 'error': True, 'error_message': 
      "Bad JSON request (missing keyname)."}
    return HttpResponse(simplejson.dumps(message))  

  if identifier not in ALL_THREADS:
    message = {'error': True, 'error_message': 
      "Unknown keyname give {0}.".form(identifier)}

  message = ALL_THREADS[identifier].get_status()
  return HttpResponse(simplejson.dumps(message))  

def start(request):
  """ This is the page a user submits a request to start AppScale. """
  if request.method == 'POST':
    form = CommonFields(data=request.POST)
    tools_runner = None
    email = form['admin_email'].value()
    password = form['admin_pass'].value()
    keyname = helpers.generate_keyname()
   
    cloud_type = None
    if 'cluster' in request.POST:
      cloud_type = CLUSTER_DEPLOY
    elif 'cloud' in request.POST:
      cloud_type = CLOUD_DEPLOY

    if cloud_type == CLOUD_DEPLOY:
      infras = form['infrastructure'].value()
      deployment_type = form['deployment_type'].value()
      machine = form['machine'].value()
      if deployment_type == ADVANCE_DEPLOYMENT:
        ips_yaml = form['ips_yaml'].value()
        tools_runner = create_instances.ToolsRunner(cloud_type,
                                   keyname,
                                   email,
                                   password,
                                   placement=ADVANCE_DEPLOYMENT,
                                   machine=machine,
                                   instance_type=instance_type,
                                   ips_yaml=ips_yaml)
      elif deployment_type == SIMPLE_DEPLOYMENT:
        min_nodes = form['min'].value()
        max_nodes = form['max'].value()
        tools_runner = create_instances.ToolsRunner(cloud_type,
                                   keyname,
                                   email,
                                   password,
                                   placement=SIMPLE_DEPLOYMENT,
                                   machine=machine,
                                   instance_type=instance_type,
                                   min_nodes=min_nodes,
                                   max_nodes=max_nodes)
      else:
        logging.error(str(form))
        return HttpServerErrorResponse("Unable to get the deployment strategy")
    elif cloud_type == CLUSTER_DEPLOY:
      ips_yaml = form['ips_yaml'].value()
      tools_runner = create_instances.ToolsRunner(cloud_type,
                                 keyname,
                                 email,
                                 password,
                                 ips_yaml=ips_yaml)
    else:
      logging.error(str(form))
      return HttpResponseServerError("Unable to figure out the type of cloud deployment")  
    tools_runner.start()
    identifier = tools_runner.keyname
    ALL_THREADS[identifier] = tools_runner
    return render(request, 'base/start.html', {'keyname': identifier})
  else:
    logging.error(str(form))
    return HttpServerErrorResponse("404 Page not found")
