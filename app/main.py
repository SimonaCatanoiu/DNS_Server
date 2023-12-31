from flask import Flask,render_template, request, redirect, url_for
from json_handler import read_file_json, write_file_json, generate_json_dns_info,generate_json_zone_details
from forms import DNSInfoForm , DnsZoneDetails
app = Flask(__name__)
app.config['SECRET_KEY'] = "proiect_retele"

@app.route("/", methods=['GET', 'POST'])
def home():
    json_path = "dns_data/json/named.conf.options.json"
    json_path_logs = "dns_data/json/named.conf.json"
    form = DNSInfoForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        new_data = request.form.to_dict()
        result1, result2 = generate_json_dns_info(new_data)
        if 'error' in result1:
            return render_template('error.html', error=result1, target_page_url=url_for('home'), target_page_name="Home")
        
        write_file_json(json_path,result1)
        write_file_json(json_path_logs,result2)
        return redirect(url_for('home'))
    
    dns_info = read_file_json(json_path)
    log_info = read_file_json(json_path_logs)
    form.set_defaults(dns_info,log_info)
    return render_template('home.html',form=form)

@app.route("/logs")
def logs():
    json_path_logs = "dns_data/json/named.conf.json"
    logs_data = read_file_json(json_path_logs)
    return render_template('logs.html',log_paths=logs_data)

@app.route("/get_logs")
def get_logs():
    file_path = request.args.get('file_path', '')
    try:
        with open(file_path, 'r') as log_file:
            lines = log_file.readlines()
            last_30_lines = ''.join(lines[-30:])
            return last_30_lines
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return str(e)
    
@app.route("/zones/<int:page>")
@app.route("/zones", defaults={'page': 1})
def zones(page):
    json_path = "dns_data/json/zones.json"
    data = read_file_json(json_path)
    normal_zones = [zone for zone in data["zones"] if zone["Type"] == "normal"]
    return render_template('zones.html',zones=normal_zones,page=page)

@app.route("/zone_details/<int:zone_id>")
def zone_details(zone_id):
    json_path = "dns_data/json/zones.json"
    data = read_file_json(json_path)
    my_zone = [zone for zone in data["zones"] if zone["Id"] == zone_id].pop(0)
    zone_data_json = my_zone['Json_data_path']
    zone_data = read_file_json(zone_data_json)

    form = DnsZoneDetails()
    form.set_defaults(my_zone,zone_data)
    return render_template('zone_details.html',zone=my_zone,form=form)

@app.route("/submit_zone_details/<int:zone_id>", methods=['POST'])
def submit_zone_details(zone_id):
    if request.method == 'POST':
        new_data = request.form.to_dict()
        result1 = generate_json_zone_details(new_data,zone_id)
        if 'error' in result1:
            return render_template('error.html', error=result1, target_page_url=url_for('home'), target_page_name="Home")
        
        return redirect(url_for('zones', page=1))

@app.route("/delete_zone/<int:zone_id>")
def delete_zone(zone_id):
    return f"Delete for Zone ID: {zone_id}"
    
@app.route("/add_zone")
def add_zone():
    return render_template('add_zone.html') 

@app.route("/reverse_zones")
def reverse_zones():
    return render_template('reverse_zones.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)