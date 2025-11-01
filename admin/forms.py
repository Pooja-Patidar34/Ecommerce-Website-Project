from django import forms
from products.models import Category,Product
from accounts.models import Role

class CategoryForm(forms.ModelForm):
          class Meta:
                  model=Category
                  fields=['name']

class ProductForm(forms.ModelForm):
         class Meta:
                 model=Product
                 fields=['category','name','description','price','stock','image']


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['rname']

    def clean_rname(self):
        rname = self.cleaned_data['rname']
        if Role.objects.filter(rname__iexact=rname).exists():
            raise forms.ValidationError("")
        return rname