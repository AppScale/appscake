God.watch do |w|
  w.name = "appscake"
  w.start = "cd /root/appscake && python manage.py runserver `python get_my_ip.py`:8000"
  w.keepalive
end