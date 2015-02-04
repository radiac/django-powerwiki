from django import forms

from uzewiki.models import Page, Asset


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['wiki', 'slug', 'title', 'content']
        widgets = {
            'wiki': forms.HiddenInput(),
            'slug': forms.HiddenInput(),
            'title': forms.TextInput(attrs={
                'placeholder':  'Title',
                'autocomplete': 'off',
            }),
            'content': forms.Textarea(attrs={'class': 'code'}),
        }


class ImportForm(forms.Form):
    file = forms.FileField(help_text="Zip containing wiki pages")
    wipe = forms.BooleanField(
        required=False, initial=False, help_text="Wipe the wiki first",
    )
