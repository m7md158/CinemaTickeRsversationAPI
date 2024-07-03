"""
URL configuration for project project.

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
from django.contrib import admin
from django.urls import path,include
from tickets import views
from django.db import router
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

# special case for 7 way -> viewset
router = DefaultRouter()
router.register('guests',views.viewsets_guest)
router.register('movies',views.viewsets__movie)
router.register('reservations',views.viewsets__resrvation)

urlpatterns = [
    path('admin/', admin.site.urls),

    #1
    path('django/jsonersponse/',views.no_rest_no_model),

    #2
    path('django/jsonersponsefrommodel/', views.no_rest_from_model),

    #3.1  GET POST from rest framework function based view @api_view
    path('rest/fvb/', views.FBV_List),

    #3.2 Get PUT DELETE from rest framework function based view @api_view
    path('rest/fvb/<int:pk>', views.FBV_Pk),

    #4.1 CBV_List GET POST from rest framework function based class @api_view
    path('rest/cbv/', views.CBV_List.as_view()),

    # 4.2 CBV_pk GET PUT DELETE from rest framework function based class @api_view
    path('rest/cbv/<int:pk>', views.CBV_pk.as_view()),

    # 5.1 mixins_list GET POST from rest framework class view mixins
    path('rest/mixins/', views.mixins_list.as_view()),

    # 5.1  GET Put Delete from rest framework class view mixins
    path('rest/mixins/<int:pk>', views.mixins_pk.as_view()),

    # 6.1 GET Post from rest framework class view generics
    path('rest/generics/', views.generics_list.as_view()),

    # 6.2  GET Put Delete from rest framework class view generics
    path('rest/generics/<int:pk>', views.generics_pk.as_view()),

    # 7 viewsets
    path('rest/viewsets/', include(router.urls)),

    # 8 find movies
    path('fbv/findmovies/', views.find_movie),
    
    # 9 new reservation
    path('fbv/create_reservation/', views.new_reservation),

    # 10 rest auth url
    path('api-auth/', include('rest_framework.urls')),

    # 11 Token authentication
    path('api-auth-token', obtain_auth_token),

    # 12 Post pk genercis post_pk
    # path('post/generics/<int:pk>', views.Post.as_view()),
    path('post/generics/<int:pk>', views.Post_pk.as_view()),

    ]


