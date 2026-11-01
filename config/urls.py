from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Импортируем функцию напрямую, без приставки views
from catalog.views import add_product

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('catalog.urls')),
    # Используем просто имя функции add_product
    path('add-product/', add_product, name='add_product'),
]

# ЭТО ВАЖНО: Раздача медиа-файлов (картинок) только в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
