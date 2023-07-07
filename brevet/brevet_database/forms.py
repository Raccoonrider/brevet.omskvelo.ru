import re

from django import forms

from brevet_database.models import Randonneur

result_pattern = re.compile("^(\d{1,2})[^\d]?(\d{2})$")

class ProtocolUploadForm(forms.Form):
    xls = forms.FileField(label="*.xls")


class AddResultForm(forms.Form):
    """ Add result form for manual result calculation (deprecated). Note field types."""
    result = forms.DurationField()
    medal = forms.BooleanField(required=False)

    def __init__(self, data=None, *args, **kwargs):
        """ Allows user to enter time in HH[?]MM format instead of default HH:MM:SS format.
        Any delimiter is valid.
        """
        if data:
            data = data.copy()
            result = data['result'].strip()
            result_match = result_pattern.match(result)
            if result_match:
                data['result'] = result_match.group(1) + ":" + result_match.group(2) + ":00"
        super().__init__(data, *args, **kwargs)


class AddResultTimeForm(forms.Form):
    """ Add result form for automatic result calculation. Note field types."""
    result = forms.TimeField()
    medal = forms.BooleanField(required=False)

    def __init__(self, data=None, *args, **kwargs):
        """ Allows user to enter time in HH[?]MM format instead of default HH:MM:SS format.
        Any delimiter is valid.
        """
        if data:
            data = data.copy()
            result = data['result'].strip()
            result_match = result_pattern.match(result)
            if result_match:
                data['result'] = result_match.group(1) + ":" + result_match.group(2) + ":00"

        super().__init__(data, *args, **kwargs)

class AdminResultForm(forms.ModelForm):
    def __init__(self, data=None, *args, **kwargs):
        if data:
            data = data.copy()
            data['time'] = data['time'].strip()
            if result_pattern.match(data['time']):
                data['time'] += ":00"
        super().__init__(data, *args, **kwargs)

    class Meta:
        model = Randonneur
        exclude = []