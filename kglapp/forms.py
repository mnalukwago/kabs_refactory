from django import forms
from .models import Procurement
from .models import Sale
from .models import CreditSale
from .models import Supplier
from .models import Produce
from .models import Branch
from .models import Receipt
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class ProcurementForm(forms.ModelForm):
    class Meta:
        model = Procurement
        fields = '__all__'

        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),}

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'

class CreditSaleForm(forms.ModelForm):
    class Meta:
        model = CreditSale
        fields = '__all__'  
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "dispatch_date": forms.DateInput(attrs={"type": "date"}),}

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
        
class ProduceForm(forms.ModelForm):
    class Meta:
        model = Produce
        fields = '__all__'

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = '__all__'

class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = '__all__'
        widgets = {
            'receipt_date': forms.DateInput(attrs={'type': 'date'})}


