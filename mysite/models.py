# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class Member(AbstractUser):
    # 例如新增手機號碼欄位
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    # OneToOneField 連接到 Member 模型
    member = models.OneToOneField(
        Member,
        on_delete=models.CASCADE,  # 如果 Member 被刪除，Profile 也會被刪除
        related_name='profile'     # Member 反向查詢時的名稱
    )
    bio = models.TextField(blank=True, null=True)  # 簡介

    def __str__(self):
        return f"{self.member.username}'s Profile"
    
class Category(models.Model):
    category_id = models.AutoField(primary_key=True, verbose_name='分類編號')  # 分類編號作為主鍵
    category_name = models.CharField(max_length=100, verbose_name='分類名稱')  # 分類名稱

    def __str__(self):
        return self.category_name  # 回傳分類名稱
    
class Record(models.Model):
    recordNo = models.AutoField(primary_key=True, verbose_name='紀錄編號')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name='會員編號')
    transaction_type = models.CharField(max_length=7,choices=[('income', '收入'), ('expense', '支出')],default='expense',verbose_name='收支')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='商品類別')  # 外鍵指向Category
    describe = models.TextField(verbose_name='說明')
    price = models.PositiveIntegerField(default=0, verbose_name='價格')
    date = models.DateField(verbose_name='日期')

    def __str__(self):
        return str(self.recordNo)