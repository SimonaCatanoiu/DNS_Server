from jinja2 import Template,Environment, FileSystemLoader
from json_handler import *

def create_named_conf():
    json_data = read_file_json("dns_data/json/named.conf.json")
    env = Environment(loader=FileSystemLoader('dns_data/templates'))
    template = env.get_template('named.conf.j2')
    rendered_config = template.render(json_data)
    print(rendered_config)

def create_conf_options():
    json_data = read_file_json("dns_data/json/named.conf.options.json")
    env = Environment(loader=FileSystemLoader('dns_data/templates'))
    template = env.get_template('named.conf.options.j2')
    rendered_config = template.render(json_data)
    print(rendered_config)

def create_conf_local():
    json_data = read_file_json("dns_data/json/zones.json")
    env = Environment(loader=FileSystemLoader('dns_data/templates'))
    template = env.get_template('named.conf.local.j2')
    rendered_config = template.render(json_data)
    print(rendered_config)