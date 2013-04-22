""" Views for different pages. """
import logging

from appscake import helpers
from appscake import create_instances
from appscake.forms import CommonFields
from appscake.forms import Cluster
 
from django.contrib import  messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.utils import simplejson


# When deploying on virtual machines without IaaS support.
CLUSTER_DEPLOY = "cluster"

# When deploying on IaaS.
CLOUD_DEPLOY = "cloud"

# A global variable to store all threads running the tools.
ALL_THREADS = {}

# Strategies for cloud deployments.
SIMPLE_DEPLOYMENT = "simple"
ADVANCE_DEPLOYMENT = "advance"

def home(request):
  return render(request, 'base/home.html', {'form': CommonFields(),})

def about(request):
  return render(request, 'base/about.html')

def get_status(request):
  """ Returns a json string of the status of the tools being run. """
  post = request.POST.copy()
  identifier = None
  if 'tools_id' in post:
    identifier = post['tools_id']
  else:
    message = { 'error': True, 'error_message': 
      "Bad JSON request (missing tools_id identifier)."}
    return HttpResponse(simplejson.dumps(message))  

  if identifier not in ALL_THREADS[post['tools_id']]:
    message = {'error': True, 'error_message': 
      "Unknown identifier give {0}.".form(identifier)}

  message = ALL_THREADS[identifier].get_status()
  return HttpResponse(simplejson.dumps(message))  

def start(request):
  """ This is the page a user submits a request to start AppScale. """
  if request.method == 'POST':
    form = CommonFields(data=request.POST)

    tools_runner = None

    email = form['admin_email']
    password = form['admin_pass']
    keyname = helpers.generate_keyname()
    logging.info(str(form))
    cloud_type = form['cloud']
    if cloud_type == CLOUD_DEPLOY:
      infras = form['infrastructure'] 
      deployment_type = form['deployment_type']
      machine = form['machine']
      if deployment_type == ADVANCE_DEPLOYMENT:
        ips_yaml = form['ips_yaml']
        tools_runner = ToolsRunner(cloud_type,
                                   keyname,
                                   email,
                                   password,
                                   placement=ADVANCE_DEPLOYMENT,
                                   machine=machine,
                                   instance_type=instance_type,
                                   ips_yaml=ips_yaml)
      elif deployment_type == SIMPLE_DEPLOYMENT:
        min_nodes = form['min']
        max_nodes = form['max']
        tools_runner = ToolsRunner(cloud_type,
                                   keyname,
                                   email,
                                   password,
                                   placement=SIMPLE_DEPLOYMENT,
                                   machine=machine,
                                   instance_type=instance_type,
                                   min_nodes=min_nodes,
                                   max_nodes=max_nodes)
    elif cloud_type == CLUSTER_DEPLOY:
      ips_yaml = form['ips_yaml']
      tools_runner = ToolsRunner(cloud_type,
                                 keyname,
                                 email,
                                 password,
                                 ips_yaml=ips_yaml)
    tools_runner.start()
    ALL_THREADS[tools_runner.identifier] = tools_runner
  else:
    return  render(request, 'base/start.html')
