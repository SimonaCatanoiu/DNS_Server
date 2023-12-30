from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired

class DNSInfoForm(FlaskForm):
    type = StringField('Type', render_kw={'readonly': True})
    ip = StringField('IP', render_kw={'readonly': True})
    recursion = SelectField('Recursion', choices=[('yes', 'Yes'), ('no', 'No')], validators=[DataRequired()])
    allowed_recursion = FieldList(StringField('Allowed Recursion'), min_entries=1)
    forwarders = FieldList(StringField('Forwarders'), min_entries=1)
    logfile_path = StringField('Logfile Path')
    logfile_limit_size = StringField('Logfile Limit Size')
    logfile_severity = SelectField('Logfile Severity', choices=[('info', 'Info'), ('warning', 'Warning'),('err', 'Error'),('alert', 'Alert')], validators=[DataRequired()])
    submit = SubmitField('Submit')

    def set_defaults(self, dns_info,log_info):
        self.type.default = dns_info.get("Type")
        self.ip.default = dns_info.get("IP")
        self.recursion.default = dns_info.get("Recursion")
        self.allowed_recursion.default = dns_info.get("Allowed_recursion")
        self.forwarders.default = dns_info.get("Forwarders")
        
        self.logfile_path.default = log_info.get("Logfile_path")
        self.logfile_limit_size.default = log_info.get("Logfile_limit_size")
        self.logfile_severity.default = log_info.get("Logfile_severity")

        self.process()
