import jinja2
import socket

my_public_ip = socket.gethostbyname(socket.gethostname())

template_contents = open('/root/appscake/nginx_config').read()
template = jinja2.Template(template_contents)
rendered_template = template.render(my_public_ip=my_public_ip)

with open('/etc/nginx/sites-available/default', 'w') as file_handle:
  file_handle.write(rendered_template)