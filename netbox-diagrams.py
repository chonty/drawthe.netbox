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

role_y = {'mpls p': 0, 'mpls pe': 1, 'management': 2, 'firewall': 2}
netbox_devices = {}
for d in device_names:
    netbox_d = nb.dcim.devices.get(name=d)
    netbox_devices[d] = {}
    netbox_devices[d]['y'] = role_y[netbox_d.device_role.name]

j2_env = Environment(loader=FileSystemLoader('templates'),
                        trim_blocks=True)

template = j2_env.get_template('template.j2')
rendered_template = template.render(devices=netbox_devices, interfaces=connections)
print(rendered_template)
