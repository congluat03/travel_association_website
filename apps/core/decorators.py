from django.shortcuts import redirect
from apps.members.models import TaiKhoan
def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        # Kiểm tra xem người dùng đã đăng nhập chưa (kiểm tra user_id trong session)
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('custom_login')

        # Truy vấn người dùng từ bảng TaiKhoan
        try:
            user = TaiKhoan.objects.get(MA_TK=user_id)
        except TaiKhoan.DoesNotExist:
            # Nếu không tìm thấy người dùng trong bảng TaiKhoan, chuyển hướng đến trang đăng nhập
            return redirect('custom_login')

        # Gắn thông tin người dùng vào request để dễ dàng sử dụng trong view
        request.user_info = user
        
        # Tiếp tục gọi hàm view gốc
        return view_func(request, *args, **kwargs)
    
    return wrapper

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('vai_tro') != 'admin':
            return redirect('custom_login')
        return view_func(request, *args, **kwargs)
    return wrapper
