""" Form creation class for deployment options in AppScale. """
from django import forms
from django.core.validators import validate_email


# Infrastructures to choose from for cloud deployments.
INFRAS=[
  ('ec2', 'Amazon EC2'),
  ('euca', 'Eucaylptus')]

# Deployment options.
DEPLOYS=[('cluster','Cluster'),
         ('cloud','Cloud')]

#Deployment type: simple or advanced
DEPLOY_TYPE=[
  ('simple', 'Simple'),
  ('advanced', 'Advanced')
]

# Different instance sizes for the user to pick from.
MACHINE=[
  ('m1.small', 'm1.small'),
  ('m1.medium', 'm1.medium'),
  ('m1.large', 'm1.large'),
  ('m1.xlarge', 'm1.xlarge')]

class CommonFields(forms.Form):
  """ A form object for the user to deploy AppScale. """
  cloud = forms.ChoiceField(choices=DEPLOYS, required = True, label = False,
    widget=forms.RadioSelect(attrs={ 'value': '', 'onclick': 
    'checkTransType(this.value)', 'type': 'radio', 'name': '', 'data-required': 
    'true', 'class': 'required', }))

  instance_type = forms.ChoiceField(choices=MACHINE,
                                    widget=forms.Select(attrs={
     'class': 'dk_fix' }))

  key = forms.CharField(label=("EC2/Eucalyptus Key"), required=True, 
    widget=forms.TextInput(attrs={ 'data-required': 'true', 'class': 'required' }))

  secret = forms.CharField(label=("EC2/Eucalyptus Secret"), required=True, 
    widget=forms.TextInput(attrs={ 'data-required': 'true', 'class': 'required' }))

  infrastructure = forms.ChoiceField(choices=INFRAS,
                                    widget=forms.Select(attrs={
    'id':
    'infrastructure', 'class': 'dk_fix' }))

  min = forms.IntegerField(max_value=100,min_value=1,
    widget=forms.TextInput(attrs={ 'data-required': 'true', 'value': '1', 
    'class': 'required' }))

  max = forms.IntegerField(max_value=100,min_value=1,
    widget=forms.TextInput(attrs={'value': '1', }))

  cloud = forms.CharField(widget = forms.HiddenInput(attrs={
    'readonly':'cloud'}))

  cluster = forms.CharField(widget = forms.HiddenInput(attrs={
    'readonly':'cluster'}))

  admin_email = forms.EmailField(validators=[validate_email], max_length=40,
    required=True, widget=forms.TextInput(attrs={'id':'email', 
    'data-type':'email', 'name':"email", 'data-trigger':"change", 
    'data-required':"true"}))

  admin_pass = forms.CharField(widget=forms.PasswordInput(render_value=False,
    attrs={'id':'admin_pass', 'name':"admin_pass", 'class': 'required parsley-validate',
    'data-minlength': '6', 'data-required':"true"}), label="AppScale Admin Password", 
    min_length=6, required=True, )

  root_pass = forms.CharField(widget=forms.PasswordInput(render_value=False,
    attrs={'id':'root_pass', 'name':"root_pass", 'class': 'required parsley-validate',
    'data-minlength': '6', 'data-required':"true"}), label="Virtual Machine Root Password", 
    min_length=6, required=True, )

  pass_confirm = forms.CharField(widget=forms.PasswordInput(render_value=False,
    attrs={'id':'pass_confirm', 'class': 'required parsley-validate', 'data-equalto': 
    '#admin_pass', 'name':'pass_confirm', 'data-minlength': '6', 
    'data-required':"true"}), label="Confirm Password", min_length=6)

  cloud_admin_pass = forms.CharField(widget=forms.PasswordInput(render_value=False,
    attrs={'id':'cloud_admin_pass',
    'name':"admin_pass",
    'class': 'required parsley-validate',
    'data-minlength': '6',
    'data-required':"true"}),
    label="AppScale Admin Password", min_length=6)

  cloud_pass_confirm = forms.CharField(widget=forms.PasswordInput(render_value=False,
    attrs={'id':'cloud_pass_confirm',
    'data-equalto': '#cloud_admin_pass',
    'name':'pass_confirm',
    'data-minlength': '6',
    'data-required':"true"}),
    label="Confirm Password", min_length=6)

  keyname = forms.CharField(min_length=4, max_length=24, required=True,
    widget=forms.TextInput(attrs={'id':'keyname', 'name':"keyname",
    'data-trigger':"change", 'data-required':"true"}))

  ips_yaml = forms.CharField(label=("ips.yaml"), max_length=120,
    widget=forms.Textarea(attrs={'id':'ips_yaml', 'name':"ips",'data-trigger':"change",
    'data-required':"true", 'class': 'required' }), required=True)

  ec2_euca_url = forms.CharField(label='Eucalyptus URL',
                             max_length=120,
                             )

  deployment_type = forms.ChoiceField(label='Select Deployment Type',
                                      initial={'advanced': 'Advanced'},
                                      choices=DEPLOY_TYPE,
                                      widget=forms.Select(attrs={
                                        'placeholder': 'Select Deployment',
                                        'id': 'select-required',
                                        'data-required': 'true',
                                      }))

  machine = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
    'data-required': 'true',
  }))

