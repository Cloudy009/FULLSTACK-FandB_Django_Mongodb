from django.core.management.base import BaseCommand
from home.models import Category
from datetime import datetime

class Command(BaseCommand):
    help = 'Thêm sẵn 4 danh mục mẫu vào bảng Category với detail mô tả'

    def handle(self, *args, **kwargs):
        categories = [
            {
                'name': 'Combo',
                'created_at': datetime(2025, 5, 10, 15, 52),
                'updated_at': datetime(2025, 5, 10, 15, 52),
                'image_cat': 'https://img.freepik.com/premium-vector/combo-offer-banner-flat-design-template_1197144-14.jpg',
                'detail': 'Danh mục các gói combo ưu đãi, tiết kiệm chi phí.'
            },
            {
                'name': 'Food',
                'created_at': datetime(2025, 5, 10, 15, 47),
                'updated_at': datetime(2025, 5, 10, 15, 57),
                'image_cat': 'https://th.bing.com/th/id/OIP.sYxq2natty23oqbtUS_Z1AHaEo?cb=iwc1&w=626&h=391&rs=1&pid=ImgDetMain',
                'detail': 'Danh mục thực phẩm đa dạng, tươi ngon mỗi ngày.'
            },
            {
                'name': 'Beverage',
                'created_at': datetime(2025, 5, 10, 13, 32),
                'updated_at': datetime(2025, 5, 10, 13, 50),
                'image_cat': 'https://harshdesigns.com/wp-content/uploads/2023/04/Green-Beverage.jpg',
                'detail': 'Thức uống giải khát, dinh dưỡng, phù hợp mọi lứa tuổi.'
            },
            {
                'name': 'cake',
                'created_at': datetime(2025, 5, 6, 15, 19),
                'updated_at': datetime(2025, 5, 10, 13, 28),
                'image_cat': 'https://img.freepik.com/vector-premium/productos-panaderia-diseno-grafico-vector-plato-ilustracion_24640-8247.jpg',
                'detail': 'Bánh ngọt, bánh kem thơm ngon cho mọi dịp lễ.'
            }
        ]

        for cat in categories:
            category, created = Category.objects.update_or_create(
                name=cat['name'],
                defaults={
                    'created_at': cat['created_at'],
                    'updated_at': cat['updated_at'],
                    'image_cat': cat['image_cat'],
                    'detail': cat['detail']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✔ Đã tạo danh mục mới: {category.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠ Đã cập nhật danh mục: {category.name}"))
