import re
from django import forms
from django.core.exceptions import ValidationError


from .models import Url


class LongUrlForm(forms.ModelForm):
    url = forms.CharField(
        label='URL',
        widget=forms.TextInput(attrs={'placeholder': 'The URL you want to transform.'})
    )
    code = forms.CharField(
        required=False,
        label='CODE',
        widget=forms.TextInput(
            attrs={'placeholder': 'The code will be generated by auto if you didn\'t enter.'}
        )
    )

    def clean_url(self):
        url = self.cleaned_data.get('url')
        print('url: ', url)

        regex = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )

        if not regex.search(url):
            raise ValidationError('The url is not valid.')

        return url
        
    class Meta:
        model = Url
        fields = ('url', 'code', 'remark')


class UrlInfoForm(forms.ModelForm):
    url = forms.CharField(label='URL')
    code = forms.CharField(label='CODE')
    remark = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(UrlInfoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['readonly'] = 'readonly'


    class Meta:
        model = Url
        fields = ('url', 'code', 'remark')