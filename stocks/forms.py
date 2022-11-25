from django import forms


class ItemForm(forms.Form):
    #item_id = forms.AutoField(primary_key=True)
    #category = forms.ForeignKey(Category, on_delete=forms.CASCADE, default=1)
    name = forms.CharField(label='Item_name', max_length=50)
    quantity = forms.IntegerField(label='Quantity')
    price = forms.IntegerField(label='Price')
    cost = forms.IntegerField(label='Cost')

