from django import forms

class newAgentForm(forms.Form):
    hostname = forms.CharField(label='Hostname:', max_length=100, min_length=1, required=True)
    version = forms.IntegerField(label='Versión SNMP:', max_value=3, min_value=1, required=True)
    puerto = forms.CharField(label='Puerto:', max_length=4, min_length=1, required=True)
    grupo = forms.CharField(label='Grupo:', max_length=100, min_length=1, required=True)
# Display as_table or as_p