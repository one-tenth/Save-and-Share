from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.decorators import login_required

def index(request):
    if not request.user.is_authenticated:
        # 用戶未登入，重定向到登入頁面
        return redirect('login')

    # 用戶已登入，查詢數據
    records = Record.objects.filter(member=request.user)
    return render(request, 'index.html', {'records': records})


def register(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']


            # 創建用戶
            user = User.objects.create_user(username=username, email=email, password=password,phone=phone)
            user.save()

            messages.success(request, "註冊成功！")
            return redirect('index')
        else:
            return render(request, 'accounts/register.html', {'form': form})

    # GET 請求
    form = PhoneForm()
    return render(request, 'accounts/register.html', {'form': form})



from django.contrib.auth import authenticate, login, logout

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')

    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    return redirect('index')
#---------------------------------------------------------------
# #record
# @login_required  # 確保只有登入用戶才能訪問此視圖
# def record_input(request):
#     if request.method == 'POST': 
#         # 處理 POST 請求的邏輯
#         pass
#     return render(request, 'record_input.html')
#---------------------------------------------------------------
#record
@login_required  # 確保只有登入用戶才能訪問此視圖
def record_input(request):  
    if request.method == 'POST':
        record_form = RecordForm(request.POST)
        if record_form.is_valid():
            record = record_form.save(commit=False)  # 先保存但不提交
            record.member = request.user  # 設置當前用戶為該交易的會員
            record.save()  # 提交並保存交易記錄
            return redirect('index')  # 提交後重定向回首頁

    else:
        record_form = RecordForm()

    categories = Category.objects.all()  # 確保載入所有分類
    category_form = CategoryForm()

    records = Record.objects.filter(member=request.user)

    return render(request, 'record_input.html', {
        'record_form': record_form,
        'category_form': category_form,
        'categories': categories,
        'records': records,  
    })


#管理分類
def category_management(request):
    categories = Category.objects.all()  # 確保獲取所有分類
    
    category_form = CategoryForm()

    for category in categories:
        print(category.category_ids)

    return render(request, 'category_management.html', {
        'categories': categories,
        'category_form': category_form,
    })

#---------------------------------------------------------------
#相機
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.files.base import ContentFile
import base64
import re

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        image_data = request.POST.get('image')  # 取得 Base64 圖片數據
        
        if not image_data:
            return render(request, 'front.html', {'error': '請提供有效的圖片'})

        try:
            # 移除 base64 前綴，例如 "data:image/png;base64,"
            image_data = re.sub('^data:image/.+;base64,', '', image_data)
            image_bytes = base64.b64decode(image_data)  # 轉換回二進位格式

            # 轉換成 OpenCV 可讀格式
            image_array = np.frombuffer(image_bytes, dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            
            # 轉換為灰階影像提高辨識率
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            decoded_objects = decode(gray_image)

            if not decoded_objects:
                return render(request, 'front.html', {'error': '無法識別 QR Code'})

            # 解析 QR Code 資料
            raw_results = [obj.data.decode('utf-8') for obj in decoded_objects]
            filtered_results = [process_qr_data(data) for data in raw_results]

            return render(request, 'front.html', {'message': '解析成功', 'data': filtered_results})

        except Exception as e:
            return render(request, 'front.html', {'error': f'圖片處理錯誤: {str(e)}'})

    return render(request, 'front.html')

def process_qr_data(qr_text):
    """
    處理 QR Code 內容：
    - 以 ":" 分割字串
    - 只保留第 0 個元素的前 17 個字元
    - 取第 5 個之後的元素
    - 回傳新的字串
    """
    parts = qr_text.split(':')
    
    if len(parts) > 0:
        first_part = parts[0][:16]  # 取前 17 個字
    else:
        first_part = ""

    filtered_parts = [first_part] + parts[5:] if len(parts) > 5 else [first_part]
    return ':'.join(filtered_parts)

