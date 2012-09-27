#!/usr/bin/ruby
# Author: Hiranya Jayathilaka (hiranya@cs.ucsb.edu)
# AppsCake web interface for deploying and launching AppScale clouds
# AppsCake = Makes deploying AppScale a 'piece of cake'

require 'rubygems'
require 'sinatra/base'
require 'webrick'
require 'webrick/https'
require 'openssl'

CURRENT_DIR = File.expand_path(File.dirname(__FILE__))

$:.unshift CURRENT_DIR
require 'appscake_utils'

puts "\nAppsCake - Makes deploying AppScale a 'piece of cake'!\n\n"

class AppsCake < Sinatra::Base
  get '/' do
    erb :index
  end

  post '/virtual.do' do
    if locked?
      return report_error("Server Busy", "AppsCake is currently busy deploying a cloud." +
          " Please try again later.")
    end

    status, yaml_result, yaml = validate_yaml(params[:ips])
    if !status
      return report_error("IP Configuration Error", yaml_result)
    end

    status,acc_result = validate_appscale_credentials(params[:virtual_user],
                                                      params[:virtual_pass], params[:virtual_pass2])
    if !status
      return report_error("AppScale Administrator Account Configuration Error", acc_result)
    end

    status,ssh_result = validate_ssh_credentials(params[:virtual_keyname], params[:root_password], yaml)
    if !status
      return report_error("AppScale SSH Configuration Error", ssh_result)
    end

    add_key_options = {
        'ips' => yaml,
        'keyname' => params[:virtual_keyname],
        'auto' => true,
        'root_password' => params[:root_password]
    }

    app_name = nil
    file_location = nil
    if !params[:target_app].nil? and params[:target_app] != '_none_'
      puts params[:target_app]
      app_name = params[:target_app]
      file_location = File.join(File.dirname(__FILE__), "repository", params[:target_app])
    end

    run_instances_options = {
        'ips' => yaml,
        'keyname' => params[:virtual_keyname],
        'file_location' => file_location,
        'appname' => app_name,
        'appengine' => 1,
        'autoscale' => true,
        'separate' => false,
        'confirm' => false,
        'table' => 'cassandra',
        'infrastructure' => nil,
        'admin_user' => params[:virtual_user],
        'admin_pass' => params[:virtual_pass]
    }

    deploy_on_virtual_cluster(params, add_key_options, run_instances_options, yaml_result)
  end

  post '/iaas_ec2.do' do
    status, result = validate_ec2_cluster_settings(params[:min], params[:max], params[:ami])
    if !status
      return report_error("Cluster Configuration Error", result)
    end

    status, result = validate_ec2_credentials(params[:username], params[:access_key],
                                              params[:secret_key], params[:region])
    if !status
      return report_error("EC2 Security Configuration Error", result)
    end

    status, result = validate_ec2_certificate_uploads(params[:username], params[:private_key],
                                                      params[:cert])
    if !status
      return report_error("EC2 Security Configuration Error", result)
    end
    cert_timestamp = result

    status,acc_result = validate_appscale_credentials(params[:ec2_user],
                                                      params[:ec2_pass], params[:ec2_pass2])
    if !status
      return report_error("AppScale Administrator Account Configuration Error", acc_result)
    end

    app_name = nil
    file_location = nil
    if !params[:target_app].nil? and params[:target_app] != '_none_'
      app_name = params[:target_app]
      file_location = File.join(File.dirname(__FILE__), "repository", params[:target_app])
    end

    run_instances_options = {
        'keyname' => params[:ec2_keyname],
        'group' => params[:ec2_keyname],
        'file_location' => file_location,
        'appname' => app_name,
        'appengine' => 1,
        'autoscale' => true,
        'separate' => false,
        'confirm' => false,
        'table' => 'cassandra',
        'infrastructure' => 'ec2',
        'min_images' => params[:min].to_i,
        'max_images' => params[:max].to_i,
        'instance_type' => params[:instance_type],
        'machine' => params[:ami],
        'admin_user' => params[:ec2_user],
        'admin_pass' => params[:ec2_pass],
    }
    deploy_on_ec2(params, run_instances_options, cert_timestamp)
  end

  get '/view_logs' do
    timestamp = params[:ts]
    if timestamp.nil? or timestamp.length == 0
      return report_error("Invalid URL Request", "No timestamp information found in the request")
    end
    @timestamp = timestamp
    erb :view_log
  end
end

webrick_options = {
    :Port               => 8443,
    :Logger             => WEBrick::Log::new($stderr, WEBrick::Log::INFO),
    :DocumentRoot       => "/ruby/htdocs",
    :SSLEnable          => true,
    :SSLVerifyClient    => OpenSSL::SSL::VERIFY_NONE,
    :SSLCertificate     => OpenSSL::X509::Certificate.new(
        File.open(File.join(CURRENT_DIR, "certificates", "cert-appscake.pem")).read),
    :SSLPrivateKey      => OpenSSL::PKey::RSA.new(
        File.open(File.join(CURRENT_DIR, "certificates", "pk-appscake.pem")).read),
    :SSLCertName        => [["CN", WEBrick::Utils::getservername]],
    :app                => AppsCake,
    :server             => 'webrick'
}

Rack::Server.start webrick_options

at_exit do
  puts "Terminating AppsCake..."
end


