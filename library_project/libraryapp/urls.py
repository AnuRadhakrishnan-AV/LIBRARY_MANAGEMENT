
from django.contrib import admin
from django.urls import path
from libraryapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.FrontpageView.as_view(), name='front_page'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('user_signup/', views.UserSignupView.as_view(), name='user_signup'),
    path('librarian_signup/', views.LibrarianSignupView.as_view(), name='librarian_signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('user_dashboard/', views.UserDashboardView.as_view(), name='user_dashboard'),
    path('librarian_dashboard/', views.LibrarianDashboardView.as_view(), name='librarian_dashboard'),
    path('admin_dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('approve_librarian/<int:pk>/',views. ApproveLibrarianView.as_view(), name='approve_librarian'),
    path('reject_librarian/<int:pk>/',views. RejectLibrarianView.as_view(), name='reject_librarian'),
    path('delete_approved_library/<int:pk>/',views. DeleteApprovedLibraryView.as_view(), name='delete_approved_library'),
    path('add_book/',views. AddBookView.as_view(), name='add_book'),
    path('edit_book/<int:pk>/',views. EditBookView.as_view(), name='edit_book'),
    path('delete_book/<int:pk>/',views. DeleteBookView.as_view(), name='delete_book'),
    path('library/<int:pk>/',views. LibraryDetailView.as_view(), name='library_detail'),
    path('book/<int:pk>/',views.BookingPageView.as_view(), name='booking_page'),
    path('profile/',views.UserProfileView.as_view(), name='user_profile'),


    
   
   
   


  
    

    
   


    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


   
























