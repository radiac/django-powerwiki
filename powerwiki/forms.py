from django import forms

from .models import Asset, Page, Wiki


class PageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Inherit markup engine from parent
        if not self.instance.pk and self.initial.get("wiki"):
            self.initial["markup_engine"] = self.initial["wiki"].markup_engine

    class Meta:
        model = Page
        fields = ["wiki", "path", "title", "markup_engine", "content"]
        widgets = {
            "wiki": forms.HiddenInput(),
            "path": forms.HiddenInput(),
            "title": forms.TextInput(
                attrs={"placeholder": "Title", "autocomplete": "off"}
            ),
            "content": forms.Textarea(),
        }


class ImportForm(forms.Form):
    file = forms.FileField(help_text="Zip containing wiki pages")
    wipe = forms.BooleanField(
        required=False,
        initial=False,
        help_text="Wipe the wiki first",
    )


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ["wiki", "name", "file"]
        widgets = {
            "wiki": forms.HiddenInput(),
            "name": forms.HiddenInput(),
        }


class SearchForm(forms.Form):
    q = forms.CharField(
        label="Query",
        widget=forms.TextInput(attrs={"placeholder": "Search"}),
    )
    wikis = forms.ModelMultipleChoiceField(
        queryset=Wiki.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
    )

    def __init__(self, *args, available_wikis=None, **kwargs):
        super().__init__(*args, **kwargs)
        if available_wikis is not None:
            self.fields["wikis"].queryset = available_wikis

    def clean_q(self):
        q = self.cleaned_data["q"]
        q = q.strip()
        return q
