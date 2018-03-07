from django import forms
from lists.models import Item

EMPTY_ITEM_ERROR = "You can't have an empty list item"

class ItemForm(forms.models.ModelForm):

    class Meta:
        model = Item
        fields = ('text',)
        widgets={
            'text': forms.fields.TextInput(attrs={
                    'placeholder': 'Enter a to-do item',
                    'class': 'form-control input-lg',
            }),
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR }
        }

    def save(self, for_list): #custom save function to save item to a specific list
        self.instance.list = for_list
        return super().save()

class ItemFormManual(forms.Form):
    item_text = forms.CharField(
            widget=forms.fields.TextInput(attrs={
                    'placeholder': 'Enter a to-do item',
                    'class': 'form-control input-lg',
                }),
        )
