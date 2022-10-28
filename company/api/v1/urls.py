from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'persons', views.PersonViewSet, basename='Person')
router.register(r'departments', views.DepartmentViewSet, basename='Department')
urlpatterns = router.urls
