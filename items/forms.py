from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    """Form for creating and editing items"""
    
    class Meta:
        model = Item
        fields = ['title', 'description', 'category', 'type', 'brand', 'size', 'condition', 'image']
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
            'type': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'e.g., Jacket, T-shirt, Sneakers'
            }),
            'brand': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'e.g., Nike, Zara, Uniqlo (Optional)'
            }),
            'size': forms.Select(attrs={
                'class': 'form-select form-select-lg',
            }),
            'condition': forms.Select(attrs={
                'class': 'form-select form-select-lg',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control form-control-lg',
                'accept': 'image/*'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make required fields have asterisk in label
        for field_name, field in self.fields.items():
            if field.required:
                field.label = f"{field.label} *"
