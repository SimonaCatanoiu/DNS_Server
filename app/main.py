from flask import Flask,render_template, request, redirect, url_for
from json_handler import read_file_json, write_file_json, generate_json_dns_info
from forms import DNSInfoForm 
app = Flask(__name__)
app.config['SECRET_KEY'] = "proiect_retele"

@app.route("/", methods=['GET', 'POST'])
def home():
    json_path = "dns_data/json/named.conf.options.json"
    json_path_logs = "dns_data/json/named.conf.json"
    form = DNSInfoForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        new_data = request.form.to_dict()
        print("New Data:", new_data)
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

@app.route("/features")
def features():
    return render_template('features.html')

@app.route("/pricing")
def pricing():
    return render_template('pricing.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)