from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    """Form for creating and editing items"""
    
    class Meta:
        model = Item
        fields = [
            'title', 'description', 'category', 'size', 'condition',
            'tags', 'point_value', 'is_available'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'e.g., Vintage Denim Jacket'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your item in detail...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select form-select-lg',
            }),
            'size': forms.Select(attrs={
                'class': 'form-select form-select-lg',
            }),
            'condition': forms.Select(attrs={
                'class': 'form-select form-select-lg',
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'e.g., summer, casual'
            }),
            'point_value': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter point value'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make required fields have asterisk in label
        for field_name, field in self.fields.items():
            if field.required:
                field.label = f"{field.label} *"
