import json
import re

def read_file_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_file_json(file_path, new_data):
    with open(file_path, 'w') as file:
        json.dump(new_data, file, indent=2)

def check_empty_string_in_list(lst):
    for item in lst:
        if item == '':
            return True
    return False

def extract_list_values(form_data, prefix):
    values = []
    for key, value in form_data.items():
        if key.startswith(f'{prefix}-') and value:
            values.append(value)    
    return values

def generate_json_dns_info(form_data):
    #Check if allowed_recursion and forwarders are empty
    allowed_recursion = extract_list_values(form_data, 'allowed_recursion')
    forwarders = extract_list_values(form_data, 'forwarders')

    # Create JSON data for dns info
    json_data = {
        "Type": form_data.get('type', ''),
        "IP": form_data.get('ip', ''),
        "Recursion": form_data.get('recursion', ''),
        "Allowed_recursion": allowed_recursion,
        "Forwarders": forwarders,
    }

    log_json_data = {
        "Logfile_default_path": form_data.get('logfile_path', ''),
        "Logfile_default_limit_size": form_data.get('logfile_limit_size', ''),
        "Logfile_default_severity": form_data.get('logfile_severity', ''),
        "Logfile_query_path": form_data.get('logfile_path2', ''),
        "Logfile_query_limit_size": form_data.get('logfile_limit_size2', ''),
        "Logfile_query_severity": form_data.get('logfile_severity2', ''),
    }

    if log_json_data["Logfile_default_path"] == '':
        return {"error": "Logfile_default_path must be non-empty"},None
    if log_json_data["Logfile_default_limit_size"] == '':
        return {"error": "Logfile_default_limit_size must be non-empty"},None
    if log_json_data["Logfile_query_path"] == '':
        return {"error": "Logfile_query_path must be non-empty"},None
    if log_json_data["Logfile_query_limit_size"] == '':
        return {"error": "Logfile_query_limit_size must be non-empty"},None
    
    return json_data,log_json_data

def generate_json_zone_details(form_data,zone_id):
    domains = extract_list_values(form_data, 'domains')
    ns = extract_list_values(form_data, 'ns')
    a_name = extract_list_values(form_data, 'a_name')
    a_asoc = extract_list_values(form_data, 'a_asoc')
    mx_name = extract_list_values(form_data, 'mx_name')
    mx_asoc = extract_list_values(form_data, 'mx_asoc')
    
    allow_query = extract_list_values(form_data, 'allow_query')
    name = form_data.get('name', '')
    path = form_data.get('path', '')

    #Verifica sa fie de aceeasi dimensiune a_name cu a_asoc, mx_name cu mx_asoc
    if len(a_name) != len(a_asoc):
        return {"error": "Lengths of 'a_name' and 'a_asoc' do not match."},None
    elif len(mx_name) != len(mx_asoc):
        return {"error": "Lengths of 'mx_name' and 'mx_asoc' do not match."},None

    #Verifica sa nu fie empty ns, domains, name si path
    if len(ns) == 0:
        return {"error": "NS must be non-empty"},None
    if len(domains)==0:
       return {"error": "Domains must be non-empty"},None
    if name=='':
        return {"error": "Name must be non-empty"},None
    if path=='':
        return {"error": "Path must be non-empty"},None

    json_path = "dns_data/json/zones.json"
    data = read_file_json(json_path)
    my_zone = [zone for zone in data["zones"] if zone["Id"] == zone_id].pop(0)

    zone_data_json = my_zone['Json_data_path']
    zone_data = read_file_json(zone_data_json)

    serial = zone_data["Serial"]
    serial+=1

    #update my zone with allow_query,name and path and put back in data
    my_zone["Allow_query"] = allow_query
    my_zone["Name"] = name
    my_zone["Path"] = path

    data["zones"][zone_id-1] = my_zone
   
    json_data = {
        "Serial": serial,
        "domains": domains,
        "NS": ns,
        "A_name": a_name,
        "A_asoc": a_asoc,
        "MX_name": mx_name,
        "MX_asoc": mx_asoc,
    }

    write_file_json(json_path,data)
    write_file_json("./dns_data/json/zones/db."+my_zone["Name"]+".json",json_data)

    return data,None

def generate_json_new_zone(form_data):
    name = form_data.get('name', '')
    path = form_data.get('path', '')
    domains = extract_list_values(form_data, 'domains')
    ns = extract_list_values(form_data, 'ns')
    a_name = extract_list_values(form_data, 'a_name')
    a_asoc = extract_list_values(form_data, 'a_asoc')
    mx_name = extract_list_values(form_data, 'mx_name')
    mx_asoc = extract_list_values(form_data, 'mx_asoc')
    allow_query = extract_list_values(form_data, 'allow_query')

    #Verifica sa nu fie empty ns, domains, name si path
    if len(name)==0:
        return {"error": "Name must be non-empty"},None
    if len(path)==0:
        return {"error": "Path must be non-empty"},None
    if len(ns) == 0:
        return {"error": "NS must be non-empty"},None
    if len(domains)==0:
       return {"error": "Domains must be non-empty"},None
    
    #Verifica sa fie de aceeasi dimensiune a_name cu a_asoc, mx_name cu mx_asoc
    if len(a_name) != len(a_asoc):
        return {"error": "Lengths of 'a_name' and 'a_asoc' do not match."},None
    elif len(mx_name) != len(mx_asoc):
        return {"error": "Lengths of 'mx_name' and 'mx_asoc' do not match."},None


    json_path = "dns_data/json/zones.json"
    data = read_file_json(json_path)
    num_zones = len(data.get("zones", []))
 
    new_zone = {
        "Id": num_zones+1,
        "Type": "normal",
        "Name": name,
        "Path": path,
        "Allow_query": allow_query,
        "Json_data_path": f"./dns_data/json/zones/db.{name}.json"
    }

    serial=2
    json_data = {
        "Serial": serial,
        "domains": domains,
        "NS": ns,
        "A_name": a_name,
        "A_asoc": a_asoc,
        "MX_name": mx_name,
        "MX_asoc": mx_asoc,
    }

    data.setdefault("zones", []).append(new_zone)
    write_file_json(json_path,data)
    write_file_json("./dns_data/json/zones/db."+name+".json",json_data)

    return data,num_zones+1

def is_valid_reverse_dns_zone(name):
    pattern = re.compile(r'^(\d+\.)+in-addr\.arpa$')
    return bool(pattern.match(name))

def generate_json_reverse_zone(form_data,zone_id):
    domains = extract_list_values(form_data, 'domains')
    ns = extract_list_values(form_data, 'ns')
    allow_query = extract_list_values(form_data, 'allow_query')
    name = form_data.get('name', '')
    path = form_data.get('path', '')
    ptr_name = extract_list_values(form_data, 'ptr_name')
    ptr_ip = extract_list_values(form_data, 'ptr_ip')
    
    #Verifica sa nu fie empty ns, domains, name si path
    if len(ns) == 0:
        return {"error": "NS must be non-empty"},None
    if len(domains)==0:
       return {"error": "Domains must be non-empty"},None
    if name=='':
        return {"error": "Name must be non-empty"},None
    if path=='':
        return {"error": "Path must be non-empty"},None

    #Verifica sa fie de aceeasi dimensiune PTR_Record si PTR_IP
    if len(ptr_name) != len(ptr_ip):
        return {"error": "Lengths of 'Ptr Records' and 'Ptr Ip' do not match."},None

    #Verifica sa existe digits.in-addr.arpa.zone in nume
    if not is_valid_reverse_dns_zone(name):
        return {"error": f"The reverse DNS zone name '{name}' is not valid."},None

    json_path = "dns_data/json/zones.json"
    data = read_file_json(json_path)
    my_zone = [zone for zone in data["zones"] if zone["Id"] == zone_id].pop(0)

    zone_data_json = my_zone['Json_data_path']
    zone_data = read_file_json(zone_data_json)

    serial = zone_data["Serial"]
    serial+=1

    #update my zone with allow_query,name and path and put back in data
    my_zone["Allow_query"] = allow_query
    my_zone["Name"] = name
    my_zone["Path"] = path
    data["zones"][zone_id-1] = my_zone
   
    json_data = {
        "Serial": serial,
        "domains": domains,
        "NS": ns,
        "PTR_Record": ptr_name,
        "PTR_IP": ptr_ip,
    }

    write_file_json(json_path,data)
    write_file_json("./dns_data/json/zones/"+my_zone["Name"]+".zone.json",json_data)

    return data,None

def generate_json_new_reverse_zone(form_data):
    domains = extract_list_values(form_data, 'domains')
    ns = extract_list_values(form_data, 'ns')
    allow_query = extract_list_values(form_data, 'allow_query')
    name = form_data.get('name', '')
    path = form_data.get('path', '')
    ptr_name = extract_list_values(form_data, 'ptr_name')
    ptr_ip = extract_list_values(form_data, 'ptr_ip')

    #Verifica sa nu fie empty ns, domains, name si path
    if len(name)==0:
        return {"error": "Name must be non-empty"},None
    if len(path)==0:
        return {"error": "Path must be non-empty"},None
    if len(ns) == 0:
        return {"error": "NS must be non-empty"},None
    if len(domains)==0:
       return {"error": "Domains must be non-empty"},None
    
    #Verifica sa fie de aceeasi dimensiune PTR_Record si PTR_IP
    if len(ptr_name) != len(ptr_ip):
        return {"error": "Lengths of 'Ptr Records' and 'Ptr Ip' do not match."},None

    #Verifica sa existe digits.in-addr.arpa.zone in nume
    if not is_valid_reverse_dns_zone(name):
        return {"error": f"The reverse DNS zone name '{name}' is not valid."},None
    
    json_path = "dns_data/json/zones.json"
    data = read_file_json(json_path)
    num_zones = len(data.get("zones", []))
 
    new_zone = {
        "Id": num_zones+1,
        "Type": "reverse",
        "Name": name,
        "Path": path,
        "Allow_query": allow_query,
        "Json_data_path": f"./dns_data/json/zones/{name}.zone.json"
    }

    serial=2
    json_data = {
        "Serial": serial,
        "domains": domains,
        "NS": ns,
        "PTR_Record": ptr_name,
        "PTR_IP": ptr_ip,
    }

    data.setdefault("zones", []).append(new_zone)
    write_file_json(json_path,data)
    write_file_json("./dns_data/json/zones/"+name+".zone.json",json_data)

    return data,num_zones+1