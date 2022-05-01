from django.urls import path
from django.views.decorators.cache import never_cache
from . import views

urlpatterns = [
    path('', never_cache(views.YoutubeSearchJSON), name='youtube-json'),
    path('youtube/', views.YoutubeAdvancedSearchJSON, name='youtube-advanced-json'),
    path('youtube/comments/', views.YoutubeCommentsSearchJSON, name='youtube-comments-json'),
    path('youtube/details/', views.YoutubeVideoDetailJSON, name='youtube-detail'),
    path('youtube/src/', views.YoutubeGetVideoSRC, name='youtube-src'),
    path('youtube/captions/', views.YoutubeGetVideoTrack, name='youtube-caption'),
    path('google/', views.GoogleSearchAPI, name='google'),
    path('twitter/', views.TwitterSearchJSON, name='twitter-search'),
    path('tweet/', views.TwitterDetailJSON, name='twitter-detail'),
    path('url/', views.URLJSON, name='url-json'),
    path('cache/', views.CacheBuster, name='cache-buster')
]
