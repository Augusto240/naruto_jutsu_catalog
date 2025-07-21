from django import forms
from .models import Jutsu
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div

class JutsuForm(forms.ModelForm):
    class Meta:
        model = Jutsu
        fields = ['name', 'description', 'element_type', 'jutsu_type', 'rank', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'element_type': forms.Select(attrs={'class': 'form-select'}),
            'jutsu_type': forms.Select(attrs={'class': 'form-select'}),
            'rank': forms.Select(attrs={'class': 'form-select'}),
        }
        help_texts = {
            'name': 'Digite o nome do jutsu (exemplo: Rasengan).',
            'description': 'Descreva o jutsu, seus efeitos e como é executado.',
            'image': 'Opcional: Faça upload de uma imagem representativa do jutsu.'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-3'),
                Column('rank', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('element_type', css_class='form-group col-md-6 mb-3'),
                Column('jutsu_type', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            'description',
            'image',
            Div(
                Submit('submit', 'Salvar', css_class='btn-success'),
                css_class='text-end mt-3'
            )
        )