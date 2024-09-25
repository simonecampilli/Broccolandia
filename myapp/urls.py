from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserDataViewSet
from .views import UserDataCreate, UserOwnDataView, UserDetailView
router = DefaultRouter()
router.register(r'userdata', UserDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create/', UserDataCreate.as_view(), name='create-userdata'),
path('mydata/', UserOwnDataView.as_view(), name='my-data'),
path('user/details/', UserDetailView.as_view(), name='user-details'),
path('user/details/', UserDetailView.as_view(), name='user-details'),


]
