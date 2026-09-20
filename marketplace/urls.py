from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Core & Marketplace views
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('browse/', views.browse, name='browse'),
    
    # Item CRUD views
    path('items/new/', views.new_item, name='new_item'),
    path('items/<int:pk>/', views.detail, name='detail'),
    path('items/<int:pk>/edit/', views.edit_item, name='edit_item'),
    path('items/<int:pk>/delete/', views.delete_item, name='delete_item'),

    # Direct Messaging views
    path('inbox/', views.inbox, name='inbox'),
    path('inbox/<int:item_pk>/<int:user_pk>/', views.conversation_detail, name='conversation_detail'),

    # Authentication views (Using Django built-in auth views for login/logout)
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
