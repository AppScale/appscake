require 'rubygems'
require 'test/unit'
require 'flexmock/test_unit'

$:.unshift File.join(File.dirname(__FILE__), "..", "lib")
require 'appscake_utils'

class TestInputValidation < Test::Unit::TestCase

  def test_validate_appscale_credentials
    status, result = validate_appscale_credentials('bwayne', 'batman', 'batman')
    assert status
    assert_equal result, ''

    status, result = validate_appscale_credentials(nil, 'batman', 'batman')
    assert !status
    assert result.include?('username')

    status, result = validate_appscale_credentials('bwayne', nil, 'batman')
    assert !status
    assert result.include?('password')

    status, result = validate_appscale_credentials('bwayne', 'batman', nil)
    assert !status
    assert result.include?('password')

    status, result = validate_appscale_credentials('bwayne', 'batman', 'robin')
    assert !status

    status, result = validate_appscale_credentials('bwayne', 'robin', 'robin')
    assert !status
  end

  def test_validate_yaml
    yaml1 = <<EOS
---
:controller: 192.168.1.2
:servers:
- 192.168.1.3
- 192.168.1.4
- 192.168.1.5
EOS
    status, result = validate_yaml(yaml1)
    assert status

    yaml2 = <<EOS
:master: 192.168.1.2
:appengine:
- 192.168.1.3
- 192.168.1.4
:database:
- 192.168.1.5
EOS
    status, result = validate_yaml(yaml2)
    assert status

    yaml3 = <<EOS
---
:servers:
- 192.168.1.3
- 192.168.1.4
- 192.168.1.5
EOS
    status, result = validate_yaml(yaml3)
    assert !status
    assert result.include?("login") and result.include?("shadow") and
        result.include?("zookeeper")

    yaml4 = <<EOS
---
:controller: 192.168.1.2
EOS
    status, result = validate_yaml(yaml4)
    assert !status
    assert result.include?("appengine")

    status, result = validate_yaml(nil)
    assert !status
    status, result = validate_yaml("")
    assert !status
  end

  def test_validate_ec2_cluster_settings
    status, result = validate_ec2_cluster_settings("1", "1", "ami-123456")
    assert status

    status, result = validate_ec2_cluster_settings(nil, "1", "ami-123456")
    assert !status
    status, result = validate_ec2_cluster_settings("", "1", "ami-123456")
    assert !status
    status, result = validate_ec2_cluster_settings("1", nil, "ami-123456")
    assert !status
    status, result = validate_ec2_cluster_settings("1", "", "ami-123456")
    assert !status
    status, result = validate_ec2_cluster_settings("1", "1", nil)
    assert !status
    status, result = validate_ec2_cluster_settings("1", "1", "")
    assert !status
    status, result = validate_ec2_cluster_settings("0", "1", "ami-123456")
    assert !status
    status, result = validate_ec2_cluster_settings("1", "0", "ami-123456")
    assert !status
    status, result = validate_ec2_cluster_settings("5", "4", "ami-123456")
    assert !status
    status, result = validate_ec2_cluster_settings("-1", "1", "ami-123456")
    assert !status
    status, result = validate_ec2_cluster_settings("1", "-1", "ami-123456")
    assert !status
    status, result = validate_ec2_cluster_settings("a", "b", "ami-123456")
    assert !status
  end

  def test_validate_ec2_credentials
    status, result = validate_ec2_credentials("", "batcowl", "batmobile", "gotham-city")
    assert !status
    status, result = validate_ec2_credentials(nil, "batcowl", "batmobile", "gotham-city")
    assert !status
    status, result = validate_ec2_credentials("bwayne", "", "batmobile", "gotham-city")
    assert !status
    status, result = validate_ec2_credentials("bwayne", nil, "batmobile", "gotham-city")
    assert !status
    status, result = validate_ec2_credentials("bwayne", "batcowl", "", "gotham-city")
    assert !status
    status, result = validate_ec2_credentials("bwayne", "batcowl", nil, "gotham-city")
    assert !status
    status, result = validate_ec2_credentials("bwayne", "batcowl", "batmobile", "")
    assert !status
    status, result = validate_ec2_credentials("bwayne", "batcowl", "batmobile", nil)
    assert !status
  end

  def test_validate_ec2_certificate_uploads
    status, result = validate_ec2_certificate_uploads("", "dummy", "dummy")
    assert !status
    status, result = validate_ec2_certificate_uploads(nil, "dummy", "dummy")
    assert !status
    status, result = validate_ec2_certificate_uploads("bwayne", nil, "dummy")
    assert !status
    status, result = validate_ec2_certificate_uploads("bwayne", "dummy", nil)
    assert !status
  end

  def test_redirect_standard_io
    timestamp = 12345678
    redirect_standard_io(timestamp) {
      do_stuff
    }
    log = File.join(File.expand_path(File.dirname(__FILE__)), "..",
                    "logs", "deploy-#{timestamp}.log")
    file = File.new(log, "r")
    counter = 0
    while (line = file.gets)
      assert_equal("Doing stuff", line.chomp)
      counter += 1
    end
    file.close

    assert_equal(1, counter)

    File.delete(log)
  end

  def test_deploy_on_virtual_cluster
    flexmock(AppScaleTools).should_receive(:add_keypair).and_return {
      puts "Generating keys"
    }
    flexmock(AppScaleTools).should_receive(:run_instances).and_return do
      5.times do |i|
        puts "Deploying..."
        sleep(1)
      end
    end

    params = { :keyname => "appscale" }
    result = deploy_on_virtual_cluster(params, {}, {})
    assert result[0]

    output = `kill -0 #{result[2]}`
    assert output.length == 0
    assert locked?

    puts "Waiting 10 seconds for the mock deployment tasks to complete"
    sleep(10)

    assert !locked?
    log = File.join(File.expand_path(File.dirname(__FILE__)), "..",
                    "logs", "deploy-#{result[1]}.log")
    assert File.exist?(log)
    File.delete(log)
  end

  def do_stuff
    puts "Doing stuff"
  end

end