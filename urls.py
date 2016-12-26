from django.conf.urls import *
from maze import views
from django.contrib import admin

from maze.views import make_me_a_maze

urlpatterns = [

	url(r'^admin/', include(admin.site.urls)),
	url(r'^maze/$', views.maze),
	url(r'^make_me_a_maze/$', views.make_me_a_maze),

]