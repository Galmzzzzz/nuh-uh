from .models import ShippingAddress
from django.forms import ModelForm

class ShippingAddress_Form(ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city']
