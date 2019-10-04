import pynetbox
import jinja2
from jinja2 import Environment
from jinja2 import FileSystemLoader

def unique_list(l):
    x = []
    for a in l:
        if a not in x:
            x.append(a)
    return x

nb = pynetbox.api(
    'http://192.168.111.50',
    token='8f0c6b37619e23dd6223e4df3efc76bb1cd18da4')

connections = nb.dcim.interface_connections.filter(device='sg-esg02-mgt01')
device_names = []
for connection in connections:
    device_names.append(connection.interface_a.device.name)
    device_names.append(connection.interface_b.device.name)
device_names = unique_list(device_names)

j2_env = Environment(loader=FileSystemLoader('templates'),
                        trim_blocks=True)

template = j2_env.get_template('template.j2')
rendered_template = template.render(devices=device_names, interfaces=connections)
