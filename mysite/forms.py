from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import *
User = get_user_model()

class PhoneForm(forms.Form):
    username = forms.CharField(
        max_length=150,  # 通常用戶名可以更長
        required=True,
        label="用戶名",
        error_messages={
            'required': '寶寶你沒打名字喔~'
        }
    )
    email = forms.EmailField(
        max_length=254,  # 電子郵件的標準長度限制
        required=True,
        label="電子郵件"
    )
    password = forms.CharField(
        max_length=128,  # Django 默認的密碼最大長度
        widget=forms.PasswordInput,  # 使用密碼輸入類型
        required=True,
        label="密碼"
    )
    confirm_password = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput,
        required=False,
        label="確認密碼"
    )
    phone = forms.CharField(
        max_length=12,
        validators=[
            RegexValidator(
                regex = r'^09\d{2}-\d{3}-\d{3}$',
                message="親親您輸入錯了，請輸入有效的台灣電話號碼 "
            )
        ],
        required=True,
        label="電話號碼"
    )


    # 自定義驗證用戶名是否存在
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("用戶名已存在。")
        return username

    # 自定義驗證電話號碼是否存在
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if User.objects.filter(phone=phone).exists():  # 假設電話號碼存儲在 `Profile` 模型中
            raise ValidationError("電話號碼已存在。")
        return phone
    def clean(self):
        """
        自定義驗證方法，用於檢查密碼是否一致。
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("密碼和確認密碼不一致，請重新輸入。")
        return cleaned_data
    

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['member', 'transaction_type', 'category', 'describe', 'price', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})  # 使用內建的HTML5日期選擇控件
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']  # 使用者輸入類別名稱
