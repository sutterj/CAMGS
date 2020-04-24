from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('create/', views.CompositionCreateView.as_view(), name='create'),
    path('compositions/', views.CompositionListView.as_view(),
         name='compositions'),
    path('edit/<slug:slug>/', views.CompositionEditView.as_view(),
         name='edit'),
    path('enrty/<composition>/',
         views.NoteCreateView.as_view(), name='entry'),
]
