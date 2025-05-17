from datetime import datetime, timedelta
from django.utils import timezone
from home.models import Category, Detail, HoaDon, Like, Product, ProductImage, ProductSize
from django.db.models import Sum, Count
from accounts.models import CustomUser

def get_top_selling_products():
    # Query để lấy 10 sản phẩm bán chạy nhất và thêm hình ảnh đầu tiên của sản phẩm
    top_selling_products = (
        Detail.objects
        .values('product__pro_id', 'product__title')  # Lấy ID và tên sản phẩm
        .annotate(total_sold=Sum('quantity'))  # Tổng số lượng bán của từng sản phẩm
        .order_by('-total_sold')[:10]  # Sắp xếp giảm dần và lấy 10 sản phẩm đầu tiên
    )

    # Lấy hình ảnh đầu tiên của mỗi sản phẩm
    for product in top_selling_products:
        product_image = ProductImage.objects.filter(product_id=product['product__pro_id']).first()
        product['image_pro'] = product_image.image if product_image else None  # Thêm hình ảnh đầu tiên

    print(top_selling_products)
    return top_selling_products

def get_10_new_products():
    # Lấy 10 sản phẩm mới nhất (dựa vào thời gian tạo) theo thứ tự giảm dần
    new_products = Product.objects.order_by('-created_at')[:10]

    # Lấy giá tiền của sản phẩm đầu tiên nếu có
    for product in new_products:
        # Lấy sản phẩm size đầu tiên (nếu có)
        first_size = ProductSize.objects.filter(product=product).first()
        if first_size:
            product.first_price = first_size.price
        else:
            product.first_price = product.original_price  # Nếu không có size, lấy giá gốc

    return new_products

def get_trending_products():
    # Lấy các sản phẩm phổ biến từ tất cả các hóa đơn, mỗi sản phẩm chỉ tính 1 lần xuất hiện
    top_products = (
        Detail.objects
        .values('product__pro_id', 'product__title', 'product__image_pro')
        .annotate(
            count=Count('product__pro_id', distinct=True),  # Đếm số lần xuất hiện của mỗi sản phẩm
            customer_count=Count('hoaDon__user', distinct=True)  # Đếm số khách hàng đã mua sản phẩm
        )
        .order_by('-count')  # Sắp xếp theo số lần xuất hiện, sản phẩm phổ biến nhất lên đầu
    )[:10]  # Lấy top 10 sản phẩm

    # Thêm hình ảnh đầu tiên của mỗi sản phẩm
    for product in top_products:
        product_image = ProductImage.objects.filter(product_id=product['product__pro_id']).first()
        product['image_pro'] = product_image.image if product_image else None  # Thêm hình ảnh đầu tiên

    return top_products
# GỢI Ý CHO KHÁCH HÀNG ĐÃ LOGIN
def get_user_recommended_products(user):
    # Lấy các sản phẩm mà người dùng đã mua trong các hóa đơn, tính tổng số lượng mua mỗi sản phẩm
    purchased_products = (
        Detail.objects
        .filter(hoaDon__user=user)  # Lọc theo hóa đơn của người dùng
        .values('product__pro_id', 'product__title')  # Lấy thông tin sản phẩm
        .annotate(total_quantity=Sum('quantity'))  # Tính tổng số lượng đã mua của mỗi sản phẩm
        .order_by('-total_quantity')  # Sắp xếp theo tổng số lượng mua (sản phẩm bán chạy nhất lên đầu)
    )

    # Thêm hình ảnh đầu tiên của mỗi sản phẩm
    for product in purchased_products:
        product_image = ProductImage.objects.filter(product_id=product['product__pro_id']).first()
        product['image_pro'] = product_image.image if product_image else None

    # Lấy 10 sản phẩm bán chạy nhất
    top_10_products = purchased_products[:10]

    return top_10_products

def get_liked_products_recommendations(user):
    # Lấy các sản phẩm mà người dùng đã like
    liked_products = (
        Like.objects
        .filter(user=user)
        .values('product__pro_id', 'product__category__cate_id')  # Chỉ lấy ID sản phẩm và danh mục
    )

    recommended_products = []

    # Nếu người dùng đã like ít nhất 1 sản phẩm
    if liked_products:
        # Lấy danh sách các danh mục mà người dùng đã like
        liked_categories = set(prod['product__category__cate_id'] for prod in liked_products)
        # Lấy danh sách các sản phẩm mà người dùng đã like (để loại trừ)
        liked_product_ids = set(prod['product__pro_id'] for prod in liked_products)

        # Lấy các sản phẩm trong cùng danh mục, ngoại trừ sản phẩm đã like
        recommended_products_queryset = Product.objects.filter(category__cate_id__in=liked_categories).exclude(
            pro_id__in=liked_product_ids
        )

        # Chuẩn bị danh sách sản phẩm với hình ảnh
        recommended_products = []
        for product in recommended_products_queryset[:10]:  # Lấy tối đa 5 sản phẩm
            image = ProductImage.objects.filter(product=product).first()
            recommended_products.append({
                'id': product.pro_id,
                'title': product.title,
                'image': image.image if image else None,
                'category': product.category.name,
            })

    return recommended_products

## TÍNH DASHBOARD USER
from decimal import Decimal
from bson.decimal128 import Decimal128
from django.db.models import Sum

def calculate_order_summary(user):
    hoa_don_list = HoaDon.objects.filter(user=user)
    total_spent = 0
    total_discount = 0
    for hd in hoa_don_list:
        # Chuyển Decimal128 sang float hoặc Decimal
        try:
            tong_tien = float(hd.tongTien) if hd.tongTien is not None else 0
        except Exception:
            tong_tien = 0
        total_spent += tong_tien
        try:
            discount = float(hd.discount) if hasattr(hd, 'discount') and hd.discount is not None else 0
        except Exception:
            discount = 0
        total_discount += discount
    return {
        'total_invoices': hoa_don_list.count(),
        'total_spent': total_spent,
        'total_discount': total_discount,
    }


def get_category_products():
    """
    Hàm lấy danh mục và danh sách sản phẩm theo từng danh mục
    """
    categories = Category.objects.prefetch_related('product_set').all()

    category_products = {}
    for category in categories:
        # Lấy tối đa 10 sản phẩm mỗi danh mục
        products = category.product_set.all()[:5]
        # Gắn hình ảnh đầu tiên của mỗi sản phẩm
        products_with_images = []
        for product in products:
            image = ProductImage.objects.filter(product=product).first()
            products_with_images.append({
                'id': product.pro_id,
                'title': product.title,
                'image': image.image if image else None,
                'price': 18.00,  # Giá sản phẩm mẫu, bạn có thể thay đổi thành giá thực tế
            })
        category_products[category.name] = products_with_images

    return category_products

def calculate_month_revenue():
    # Lấy ngày hôm nay
    today = timezone.now().date()

    # Ngày đầu tiên và cuối cùng của tháng
    start_of_month = today.replace(day=1)
    next_month = today.replace(day=28) + timezone.timedelta(days=4)
    end_of_month = next_month.replace(day=1) - timezone.timedelta(days=1)

    # Lọc hóa đơn trong tháng
    hoa_dons_this_month = HoaDon.objects.filter(
        created_at__gte=start_of_month,
        created_at__lte=end_of_month
    ).values_list('tongTien', flat=True)

    # Tính tổng doanh thu thủ công
    total = Decimal('0.00')
    for value in hoa_dons_this_month:
        if isinstance(value, Decimal128):
            total += value.to_decimal()
        elif isinstance(value, Decimal):
            total += value
        elif value is not None:
            total += Decimal(value)

    return total

def calculate_day_revenue():
    # Lấy ngày hôm nay (dạng date)
    today = datetime.today().date()

    # Lấy thời gian bắt đầu của ngày hôm nay (00:00:00)
    start_of_day = datetime.combine(today, datetime.min.time())

    # Lấy thời gian kết thúc của ngày hôm nay (23:59:59.999999)
    end_of_day = datetime.combine(today, datetime.max.time())

    # Lọc các hóa đơn được tạo trong ngày hôm nay
    hoa_dons_today = HoaDon.objects.filter(
        created_at__gte=start_of_day, 
        created_at__lt=end_of_day
    )

    # Tính tổng doanh thu trong ngày hôm nay
    total_revenue_today = hoa_dons_today.aggregate(total_revenue=Sum('tongTien'))['total_revenue'] or 0

    return total_revenue_today

def calculate_daily_products_sold():
    # Lấy thời gian hiện tại
    now = datetime.now()

    # Lấy ngày hôm nay bắt đầu từ 00:00:00
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # Lọc chi tiết sản phẩm đã bán trong ngày hôm nay
    total_products_sold_today = Detail.objects.filter(
        hoaDon__created_at__gte=start_of_day
    ).aggregate(total_sold=Sum('quantity'))['total_sold'] or 0

    return total_products_sold_today

def calculate_monthly_products_sold():
     # Lấy thời gian hiện tại
    now = datetime.now()

    # Tính ngày đầu tháng và cuối tháng
    first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day_of_month = (first_day_of_month.replace(month=now.month + 1 if now.month < 12 else 1, year=now.year + 1 if now.month == 12 else now.year) - timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=999999)

    # Lọc chi tiết sản phẩm đã bán trong tháng này
    total_products_sold = Detail.objects.filter(
        hoaDon__created_at__gte=first_day_of_month,
        hoaDon__created_at__lt=last_day_of_month
    ).aggregate(total_sold=Sum('quantity'))['total_sold'] or 0

    return total_products_sold

def count_registered_users_today():
    now = datetime.now()

    # Lấy thời gian bắt đầu của ngày hôm nay (00:00:00)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # Lọc người dùng đăng ký trong ngày hôm nay
    total_users_today = CustomUser.objects.filter(date_joined__gte=start_of_day).count()

    return total_users_today

def calculate_users_registered_this_month():
    now = datetime.now()
    
    # Lấy ngày đầu tháng (ngày 1 của tháng hiện tại)
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Lọc người dùng đăng ký từ ngày đầu tháng đến nay
    total_users_this_month = CustomUser.objects.filter(date_joined__gte=start_of_month).count()

    return total_users_this_month

def get_monthly_revenue(year):
    start_of_year = datetime(year, 1, 1)
    end_of_year = datetime(year, 12, 31, 23, 59, 59)

    invoices = HoaDon.objects.filter(created_at__gte=start_of_year, created_at__lte=end_of_year)
    revenue = [Decimal('0.00')] * 12

    for invoice in invoices:
        month = invoice.created_at.month
        tong_tien = invoice.tongTien

        if isinstance(tong_tien, Decimal128):
            tong_tien = tong_tien.to_decimal()
        else:
            tong_tien = Decimal(tong_tien)

        revenue[month - 1] += tong_tien

    return revenue

def get_revenue_data_for_chart(year):
    revenue = get_monthly_revenue(year)
    target = [500000] * 12

    # Chuyển Decimal -> float để JSON hóa được
    revenue_float = [float(r) for r in revenue]

    return {
        'labels': [f'Tháng {i+1}' for i in range(12)],
        'revenue': revenue_float,
        'target': target
    }