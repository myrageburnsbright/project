from ast import pattern
from enum import Flag
from django import forms
import re 
class CreateOrderForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    requires_delivery = forms.ChoiceField(choices=[
            ("0",False),
            ("1",True),
        ],)
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(choices=[
            ("0",False),
            ("1",True),
        ],)
    

    # first_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class":"form-control",
    #             "placeholder":"Введите ваше имя"
    #         }
    #     )
    # )

    # last_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class":"form-control",
    #             "placeholder":"Введите вашу фамилию"
    #         }
    #     )
    # )

    # phone_number = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class":"form-control",
    #             "placeholder":"Введите номер телефона"
    #         }
    #     )
    # )

    # requires_delivery = forms.ChoiceField(
    #     widget=forms.RadioSelect(),
    #     choices=[
    #         ("0",False),
    #         ("1",True),
    #     ],
    #     initial=0,
    # )

    # delivery_address = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class":"form-control",
    #             "id":"delivery-address",
    #             "rows":2,
    #             "placeholder":"Введите номер телефона"
    #         }
    #     ),
    #     required=False
    # )

    # payment_on_get = forms.ChoiceField(
    #     widget=forms.RadioSelect(),
    #     choices=[
    #         ("0",False),
    #         ("1",True),
    #     ],
    #     initial="card",
    # )

