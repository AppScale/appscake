import os

print os.popen("curl -L http://metadata/computeMetadata/v1beta1/instance/network-interfaces/0/access-configs/0/external-ip").read()
