from django.urls import path, include

urlpatterns = [
    path('v1/', include('company.api.v1.urls'))
]
