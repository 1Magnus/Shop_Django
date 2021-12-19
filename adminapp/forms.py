from django import forms
from authapp.models import ShopUser
from authapp.forms import ShopUsersEditForm

class ShopUserAdminEditForm(ShopUsersEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'

