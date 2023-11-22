from django import forms

class Add_To_CardForm(forms.Form) :

    quantity = forms.IntegerField(min_value=1,max_value=9,label='Quantity ')

class CouponForm(forms.Form) :

    coupon_code = forms.CharField(max_length=30,label='Coupon ',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your coupon for discount'}))