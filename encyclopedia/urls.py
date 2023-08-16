from django.urls import path


from . import views



app_name = 'encyclopedia'

urlpatterns = [
    path("index/", views.index, name="index"),
    path("random/", views.random_page, name="random"),
    path('new_entry/<str:title>/',views.new_entry, name="new_entry"),
    path("edit/<str:title>", views.edit_entry,name="edit_entry"),
    path("<str:title>/", views.entry, name="title"),    
    path("index/search", views.search, name="search"),
    path('index/create/', views.create,name="create")
    
    
]
