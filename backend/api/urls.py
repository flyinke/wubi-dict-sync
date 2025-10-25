from django.urls import path
from .views import (
    RegisterView, LoginView, 
    WubiDictPullView, WubiDictPushView, WubiDictCheckBackupExistView,
    WubiCategoryListView, WubiCategoryCreateView, WubiCategoryUpdateView, WubiCategoryDestroyView,
    WubiWordListView, WubiWordCreateView, WubiWordUpdateView, WubiWordDestroyView
)

urlpatterns = [
    path('user/register', RegisterView.as_view(), name='register'),
    path('user/login', LoginView.as_view(), name='login'),

    path('wubi/dict/pull', WubiDictPullView.as_view(), name='wubi-dict-pull'),
    path('wubi/dict/push', WubiDictPushView.as_view(), name='wubi-dict-push'),
    path('wubi/dict/check-backup-exist', WubiDictCheckBackupExistView.as_view(), name='wubi-dict-check-backup-exist'),

    path('wubi/category/list', WubiCategoryListView.as_view(), name='wubi-category-list'),
    path('wubi/category/add', WubiCategoryCreateView.as_view(), name='wubi-category-add'),
    path('wubi/category/modify/<int:pk>', WubiCategoryUpdateView.as_view(), name='wubi-category-modify'),
    path('wubi/category/delete/<int:pk>', WubiCategoryDestroyView.as_view(), name='wubi-category-delete'),

    path('wubi/word/list', WubiWordListView.as_view(), name='wubi-word-list'),
    path('wubi/word/add', WubiWordCreateView.as_view(), name='wubi-word-add'),
    path('wubi/word/modify/<int:pk>', WubiWordUpdateView.as_view(), name='wubi-word-modify'),
    path('wubi/word/delete/<int:pk>', WubiWordDestroyView.as_view(), name='wubi-word-delete'),
]
