from wtforms_alchemy import ModelForm

from models import GuestBook


class GuestBookForm(ModelForm):
    class Meta:
        model = GuestBook
