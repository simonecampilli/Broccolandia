from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import UserDataViewSet
from .views import UserDataCreate, UserOwnDataView, UserDetailView
from .views import UserDataCreateAPIView

router = DefaultRouter()
router.register(r'userdata', UserDataViewSet)


urlpatterns = [

    path('',views.map,name='map'),
    path('import-data/', views.import_user_data, name='import_user_data'),
    path('', include(router.urls)),
    #path('create/', UserDataCreate.as_view(), name='create-userdata'),
    path('mydata/', UserOwnDataView.as_view(), name='my-data'),
    path('user/details/', UserDetailView.as_view(), name='user-details'),
    path('user/details/', UserDetailView.as_view(), name='user-details'),
    path('api/userdata/', UserDataCreateAPIView.as_view(), name='create_userdata'),
    path('detect/', views.detection_view, name='detect'),
    path('dettaglio/<int:id>/', views.dettaglio, name='dettaglio'),


]