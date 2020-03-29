
from jinja2 import Template, Environment, FileSystemLoader
import time
import datetime


env = Environment(loader=FileSystemLoader("dist"))

while True:
    template = env.get_template("template.html")
    now = datetime.datetime.now()
    datestring = "{0:%Y-%m-%d %H:%M:%S} (JST)".format(now)
    with open("dist/index.html", "w") as f:
        f.write(template.render(tstamp=datestring))
    time.sleep(3)
