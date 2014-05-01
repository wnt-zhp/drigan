from drigan.forms import DriganModelForm
from django import forms
from dynamic_forms.models import DynamicFormField
import json

#CR: Średnio podobają mi się dwie rozłączne mapy, jedna odwzorowuje
#Nazwę pola na typ, a druga na opis.
#Warto byłoby powołać klasę która odpowiada za: przegowywanie nazwy, typu pola
#django oraz tworzenie pola django z DynamicFielda.
types = {
    'IntegerField': forms.IntegerField,
    'CharField': forms.CharField,
    'TextField': forms.CharField,
    'EmailField': forms.EmailField,
    'DateField': forms.DateField,
    'BooleanField': forms.BooleanField,
    'ChoiceField': forms.ChoiceField
}


#CR: Myślę że pierwszym krokiem do rozdzielenia wersji sportowej i harcerskiej
#byłoby releasowanie DynamicFormsów do własnej OSS aplikacji. W tym celu
#warto byłonby pozbyć się powiązań DynamicForms -> Drigan.
#Dziedziczenie tej klasy zaoszczędza nam jedną linijkę kodu,
#myślę że warto byłoby jednak pozbyć się tutaj DriganModelForm
class AddDynamicFormField(DriganModelForm):

    class Meta:
        model = DynamicFormField
        fields = ('name', 'field_type', 'required')


class AddChoices(forms.Form):

    name = forms.CharField(max_length=100)


class BaseDynamicForm(forms.Form):

    def __init__(self, dynamic_form, *args, **kwargs):
        super(BaseDynamicForm, self).__init__(*args, **kwargs)
        dynamic_fields = dynamic_form.fields
        for dynamic_field in dynamic_fields.all():
            field_type = types[dynamic_field.field_type]
            field = field_type()
            field.required = dynamic_field.required
            #CR: To jest słabe --- poprawne renderowanie się powinno być 
            #odpowiedzialnością samego pola a nie formularza.
            #Implementacja tego wymagałaby stworzenia nowej klasy która
            #reprezentuje dynamiczne-pole-w-formularzu
            if dynamic_field.field_type == 'TextField':
                field.widget = forms.Textarea()

            #CR: WArto byłoby napisać jaki typ ma choices (lista. mapa)
            #oraz czym jest pojedyńczy choice, bo z lektury kodu ciężko
            #to stwierdzić.
            if dynamic_field.field_type == 'ChoiceField':
                choices = json.loads(dynamic_field.additional_data['choices'])
                if not dynamic_field.required:
                    blank_choice = '---------'
                    choices.insert(0, blank_choice)
                #CR Nie ładniej byłoby jakoś tak:
                # [(c, c) for c in choices]
                field.choices = [(choices[i], choices[i])
                                 for i in range(0, len(choices))]
            self.fields[dynamic_field.name] = field
