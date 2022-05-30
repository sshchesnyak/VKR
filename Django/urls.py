"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

import main.views
from Django import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', main.views.main_view),
    path('structure/', main.views.structure_view),
    path('main/lasfileupdate/', main.views.las_file_update),
    path('main/lasrectanle/', main.views.get_las_rectanle),
    path('main/landuse/', main.views.get_land_use),
    path('main/residential/', main.views.get_residential),
    path('main/relaxation/', main.views.get_relaxation),
    path('main/protected/', main.views.get_protected),
    path('main/properties/', main.views.get_properties),
    path('main/roads/', main.views.get_roads),
    path('main/results/', main.views.get_results),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
