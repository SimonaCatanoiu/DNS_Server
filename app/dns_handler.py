from jinja2 import Template,Environment, FileSystemLoader
from json_handler import *
import os,signal,subprocess

name_reverse=''

def extract_numbers_before_in_addr(name):
    in_addr_index = name.find("in-addr")
    substring_before_in_addr = name[:in_addr_index]
    parsed_numbers = substring_before_in_addr.split(".")
    parsed_numbers.pop()
    try:
        parsed_list = [int(part) for part in parsed_numbers]
    except:
        return 0
    return len(parsed_list) 

def zip_lists(a, b): 
    return zip(a, b)

def reverse_ip_part(ip):
    global name_reverse
    num = extract_numbers_before_in_addr(name_reverse)
    reverse_ip_num=4-num
    if(reverse_ip_num<0):
        return ''
    reverse_ip = '.'.join(ip.split('.')[-reverse_ip_num:][::-1])
    return reverse_ip

def write_file(data,path):
    with open(path, 'w') as file:
        file.write(data)

def create_template(json_path, template_name,dns_file_path):
    json_data = read_file_json(json_path)
    env = Environment(loader=FileSystemLoader('dns_data/templates'))
    env.filters['zip_lists'] = zip_lists
    env.filters['reverse_ip_part'] = reverse_ip_part
    template = env.get_template(template_name)
    rendered_config = template.render(json_data)
    write_file(rendered_config,dns_file_path)
    bind9_pid_command = "pgrep named"  # Adjust this command based on your system
    bind9_pid = subprocess.check_output(bind9_pid_command, shell=True).decode('utf-8').strip()
    # Send the SIGHUP signal to the BIND9 process
    if bind9_pid:
        os.kill(int(bind9_pid), signal.SIGHUP)

def create_named_conf():
    create_template("dns_data/json/named.conf.json", "named.conf.j2","/etc/bind/named.conf")

def create_conf_options():
    create_template("dns_data/json/named.conf.options.json", "named.conf.options.j2","/etc/bind/named.conf.options")

def create_conf_local():
    create_template("dns_data/json/zones.json", "named.conf.local.j2","/etc/bind/named.conf.local")

def create_zone_file(zone_id):
    global name_reverse
    json_path = "dns_data/json/zones.json"
    data = read_file_json(json_path)
    my_zone = [zone for zone in data["zones"] if zone["Id"] == zone_id]
    zone_path=my_zone[0]["Json_data_path"]
    zone_type=my_zone[0]["Type"]
    if(zone_type=="normal"):
        create_template(zone_path,"zone.conf.j2",my_zone[0]["Path"])
    else:
        name_reverse=my_zone[0]["Name"]
        create_template(zone_path,"reverse.conf.j2",my_zone[0]["Path"])
