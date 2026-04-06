from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('service/', views.service, name='service'),
    path('liste/', views.liste, name='liste'),
    path('appartement/<slug:slug>/', views.detail, name='detail'),
    
    # Administration Custom
    path('admin-auth/login/', views.AdminLoginView.as_view(), name='admin_login'),
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    
    # CMS Appartements
    path('admin-dashboard/appartements/', views.DashboardAppartementListView.as_view(), name='dashboard_appartement_list'),
    path('admin-dashboard/appartements/add/', views.DashboardAppartementCreateView.as_view(), name='dashboard_appartement_add'),
    path('admin-dashboard/appartements/<uuid:pk>/edit/', views.DashboardAppartementUpdateView.as_view(), name='dashboard_appartement_edit'),
    
    # CMS Messages
    path('admin-dashboard/messages/', views.DashboardMessageListView.as_view(), name='dashboard_message_list'),
    
    # CMS Settings
    path('admin-dashboard/settings/', views.DashboardSettingsView.as_view(), name='dashboard_settings'),
    
    # CMS Testimonials
    path('admin-dashboard/testimonials/', views.DashboardTestimonialListView.as_view(), name='dashboard_testimonial_list'),
    path('admin-dashboard/testimonials/add/', views.DashboardTestimonialCreateView.as_view(), name='dashboard_testimonial_add'),
    path('admin-dashboard/testimonials/<uuid:pk>/edit/', views.DashboardTestimonialUpdateView.as_view(), name='dashboard_testimonial_edit'),
    path('admin-dashboard/testimonials/<uuid:pk>/delete/', views.DashboardTestimonialDeleteView.as_view(), name='dashboard_testimonial_delete'),
]