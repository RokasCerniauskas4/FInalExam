from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register_user, name='register'),
    path('login', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('add_category', views.add_category, name='add_category'),
    path('show_categories_and_notes/', views.show_categories_and_notes, name='show_categories_and_notes'),
    path('show_categories_and_notes/<int:category_id>/', views.show_categories_and_notes, name='show_categories_and_notes'),
    path('add_note', views.add_note, name='add_note'),
    path('delete_note/<int:note_id>/', views.delete_note, name='delete_note'),
    path('update_note<int:note_id>', views.update_note, name='update_note'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)