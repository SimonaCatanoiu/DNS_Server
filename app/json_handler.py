import json

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
        "Logfile_path": form_data.get('logfile_path', ''),
        "Logfile_limit_size": form_data.get('logfile_limit_size', ''),
        "Logfile_severity": form_data.get('logfile_severity', ''),
    }

    if log_json_data["Logfile_path"] == '':
        return {"error": "Logfile_path must be non-empty"},None
    if log_json_data["Logfile_limit_size"] == '':
        return {"error": "Logfile_path must be non-empty"},None
    
    return json_data,log_json_data

def extract_list_values(form_data, prefix):
    values = []
    for key, value in form_data.items():
        if key.startswith(f'{prefix}-') and value:
            values.append(value)    
    return values