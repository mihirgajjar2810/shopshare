from django import forms
from .models import Product 

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'description', 'price', 'stock', 'available', 'category', 'image']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'name': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'description': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'image': forms.FileInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input bg-dark text-white border-secondary'}),
            
        }