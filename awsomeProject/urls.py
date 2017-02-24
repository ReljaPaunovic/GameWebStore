"""awsomeProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
#from awsomeProject.core import views as core_views ###

#TODO: Clean urls, make hierarchy
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name' : 'registration/logout.html'}, name='logout'),
    url(r'^oauth/', include('social.apps.django_app.urls', namespace='social'), name = 'oauth'),  # <--
    url(r'^register/$', views.register, name='register'),
    url(r'^register/([0-9]+)/$', views.activation, name='activation'),
    url(r'^register/success/$', views.register_success),
    url(r'^$', views.home, name='index'),
    url(r'^createGitHubProfile/$', views.createGitHubProfile, name='home'),
    #TODO: Change regex to W (word metacharacter)
    url(r'^game/([0-9a-zA-Z ]+)/$', views.game, name='game'),
    url(r'^game/[0-9a-zA-Z ]+/saveScore/$', views.saveScore, name='saveScore'),
    url(r'^game/[0-9a-zA-Z ]+/saveGame/$', views.saveGame, name='saveGame'),
    url(r'^game/[0-9a-zA-Z ]+/loadGame/$', views.loadGame, name='loadGame'),
    url(r'^game/([0-9a-zA-Z ]+)/buyGame/$', views.buyGame, name='buyGame'),
    url(r'^game/([0-9a-zA-Z ]+)/addComment/$', views.addComment, name='addComment'),
    url(r'^browseGames/$', views.browseGames, name='browseGames'),
	url(r'^about/$', views.about, name='about'),
    url(r'^myProfile/$', views.myProfile, name='myProfile'),
    url(r'^game/([0-9a-zA-Z ]+)/payment/$', views.buyGameResult, name='buyGameResult'),
	#url(r'^test/$', views.test, name='test_cloudinary'),
	url(r'^test/$', views.upload, name='upload'),
	url(r'^myProfile/editProfile/$', views.editProfile, name='editProfile'),
    url(r'^myProfile/manageUploadedGames/$', views.manageUploadedGames, name='manageUploadedGames'),
    url(r'^myProfile/manageUploadedGames/([a-zA-Z0-9 ]+)/$', views.manageGame, name='manageGame'),
    url(r'^registerForAPI/$', views.registerForAPI, name='registerForAPI'),
    url(r'^searchGamesAPI/v1/$', views.searchGamesAPI, name='searchGamesAPI'),
    url(r'^searchHighScoresAPI/v1/$', views.searchHighScoresAPI, name='searchHighScoresAPI'),
    url(r'^searchGameSalesAPI/v1/$', views.searchGameSalesAPI, name='searchGameSalesAPI'),

]
