from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired

class DNSInfoForm(FlaskForm):
    type = StringField('Type', render_kw={'readonly': True})
    ip = StringField('IP', render_kw={'readonly': True})
    recursion = SelectField('Recursion', choices=[('yes', 'Yes'), ('no', 'No')], validators=[DataRequired()])
    allowed_recursion = FieldList(StringField('Allowed Recursion'), min_entries=1)
    forwarders = FieldList(StringField('Forwarders'), min_entries=1)
    logfile_path = StringField('Default Logfile Path')
    logfile_limit_size = StringField('Default Logfile Limit Size')
    logfile_severity = SelectField('Default Logfile Severity', choices=[('info', 'Info'), ('warning', 'Warning'),('err', 'Error'),('alert', 'Alert')], validators=[DataRequired()])
    logfile_path2 = StringField('Query Logfile Path')
    logfile_limit_size2 = StringField('Query Logfile Limit Size')
    logfile_severity2 = SelectField('Query Logfile Severity', choices=[('info', 'Info'), ('warning', 'Warning'),('err', 'Error'),('alert', 'Alert')], validators=[DataRequired()])
    submit = SubmitField('Submit')

    def set_defaults(self, dns_info,log_info):
        self.type.default = dns_info.get("Type")
        self.ip.default = dns_info.get("IP")
        self.recursion.default = dns_info.get("Recursion")
        self.allowed_recursion.default = dns_info.get("Allowed_recursion")
        self.forwarders.default = dns_info.get("Forwarders")
        
        self.logfile_path.default = log_info.get("Logfile_default_path")
        self.logfile_limit_size.default = log_info.get("Logfile_default_limit_size")
        self.logfile_severity.default = log_info.get("Logfile_default_severity")
        self.logfile_path2.default = log_info.get("Logfile_query_path")
        self.logfile_limit_size2.default = log_info.get("Logfile_query_limit_size")
        self.logfile_severity2.default = log_info.get("Logfile_query_severity")

        self.process()


class DnsZoneDetails(FlaskForm):
    type = StringField('Type',render_kw={'readonly': True})
    name = StringField('Name')
    path = StringField('Path')
    allow_query = FieldList(StringField('Allow Query'))

    domains = FieldList(StringField('Domains'))
    ns = FieldList(StringField('NS'))
    a_name = FieldList(StringField('A Name'))
    a_asoc = FieldList(StringField('A Association'))
    mx_name = FieldList(StringField('MX Name'))
    mx_asoc = FieldList(StringField('MX Association'))
    submit = SubmitField('Submit')

    def set_defaults(self,zone_info,zone_data):
        self.type.default = zone_info.get("Type")
        self.name.default = zone_info.get("Name")
        self.path.default = zone_info.get("Path")
        self.allow_query.default = zone_info.get("Allow_query")

        self.domains.default = zone_data.get("domains")
        self.ns.default = zone_data.get("NS")
        self.a_name.default = zone_data.get("A_name")
        self.a_asoc.default = zone_data.get("A_asoc")
        self.mx_name.default = zone_data.get("MX_name")
        self.mx_asoc.default = zone_data.get("MX_asoc")
        
        self.process()

class AddNewZoneForm(FlaskForm):
    type = SelectField('Type', choices=[('normal', 'Normal'), ('reverse', 'Reverse')], render_kw={'readonly': True})   
    name = StringField('Name')
    path = StringField('Path')
    allow_query = FieldList(StringField('Allow Query'))
    domains = FieldList(StringField('Domains'))
    ns = FieldList(StringField('NS'))
    a_name = FieldList(StringField('A Name'))
    a_asoc = FieldList(StringField('A Association'))
    mx_name = FieldList(StringField('MX Name'))
    mx_asoc = FieldList(StringField('MX Association'))
    submit = SubmitField('Submit')

    def set_defaults(self):
        self.process()

class ReverseZondeDetails(FlaskForm):
    type = StringField('Type',render_kw={'readonly': True})
    name = StringField('Name')
    path = StringField('Path')
    allow_query = FieldList(StringField('Allow Query'))

    domains = FieldList(StringField('Domains'))
    ns = FieldList(StringField('NS'))
    ptr_name = FieldList(StringField('PTR Record'))
    ptr_ip = FieldList(StringField('PTR Ip'))
    submit = SubmitField('Submit')

    def set_defaults(self,zone_info,zone_data):
        self.type.default = zone_info.get("Type")
        self.name.default = zone_info.get("Name")
        self.path.default = zone_info.get("Path")
        self.allow_query.default = zone_info.get("Allow_query")

        self.domains.default = zone_data.get("domains")
        self.ns.default = zone_data.get("NS")
        self.ptr_name.default = zone_data.get('PTR_Record')
        self.ptr_ip.default = zone_data.get('PTR_IP')
        self.process()

class AddNewReverseZoneForm(FlaskForm):
    type = StringField('Type',render_kw={'readonly': True})
    name = StringField('Name')
    path = StringField('Path')
    allow_query = FieldList(StringField('Allow Query'))
    domains = FieldList(StringField('Domains'))
    ns = FieldList(StringField('NS'))
    ptr_name = FieldList(StringField('PTR Record'))
    ptr_ip = FieldList(StringField('PTR Ip'))
    submit = SubmitField('Submit')
    
    def set_defaults(self):
        self.type.default="reverse"
        self.process()