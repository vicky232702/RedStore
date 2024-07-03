"""
URL configuration for Ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # type: ignore
from django.urls import path # type: ignore
from Eapp import views
from django.conf.urls.static import static # type: ignore # 07/05/24
from django.conf import settings  # type: ignore

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index),
    path('register/',views.register),
     path('login/',views.ulogin),
     path('logout/',views.ulogout),
     path("catfilter/<cv>",views.catfilter),
     path("sortbyprice/<pv>",views.sortbyprice),
     path("filterbyprice/",views.filterbyprice),
     path("pdetails/<rid>/",views.productdetails),
     path("vcart/",views.viewcart),
     path("addtocart/<pid>/",views.addtocart),
     path("updateqty/<x>/<cid>/",views.updatequantity),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  #07/05/24