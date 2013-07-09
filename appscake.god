God.watch do |w|
  w.name = "appscake"
  w.start = "cd /root/appscake && python manage.py runserver `get_my_ip.py`:80"
  w.keepalive
end