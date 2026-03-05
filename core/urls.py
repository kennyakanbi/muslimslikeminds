from django.urls import path
from . import views 


app_name = "core"  # important for namespacing

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("community/", views.community, name="community"),
    path("teachings/", views.teachings, name="teachings"),
    path("teachings/<int:id>/", views.teaching_detail, name="teaching_detail"),  # <-- add this
    path('events/', views.events, name='events'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path("media/", views.media, name="media"),
    path("media/<slug:slug>/", views.media_detail, name="media_detail"),
    path('media/', views.media_list, name='media_list'),
    path("serve-humanity/", views.serve_humanity, name="serve_humanity"),
    path("contact/", views.contact, name="contact"),
]
