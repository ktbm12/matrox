from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from .models import Appartement, ContactMessage, Settings
from .forms import AppartementForm, SettingsForm


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class AdminLoginView(LoginView):
    template_name = 'dashboard/login.html'
    redirect_authenticated_user = True


class AdminDashboardView(LoginRequiredMixin, SuperuserRequiredMixin, TemplateView):
    template_name = 'dashboard/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_appartements'] = Appartement.objects.count()
        context['total_messages'] = ContactMessage.objects.count()
        context['recent_messages'] = ContactMessage.objects.order_by('-created')[:5]
        context['featured_appartements'] = Appartement.objects.filter(is_featured=True)[:5]
        context['revenue_simulated'] = "1,425,800 FCFA" 
        return context


# --- CMS APPARTEMENTS ---

class DashboardAppartementListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    model = Appartement
    template_name = 'dashboard/appartement_list.html'
    ordering = '-created'


class DashboardAppartementCreateView(LoginRequiredMixin, SuperuserRequiredMixin, SuccessMessageMixin, CreateView):
    model = Appartement
    form_class = AppartementForm
    template_name = 'dashboard/appartement_form.html'
    success_url = reverse_lazy('dashboard_appartement_list')
    success_message = "La résidence %(name)s a été créée avec succès !"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Nouvelle Résidence"
        return context


class DashboardAppartementUpdateView(LoginRequiredMixin, SuperuserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Appartement
    form_class = AppartementForm
    template_name = 'dashboard/appartement_form.html'
    success_url = reverse_lazy('dashboard_appartement_list')
    success_message = "La résidence %(name)s a été mise à jour."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modifier la Résidence"
        return context


# --- CMS MESSAGES ---

class DashboardMessageListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    model = ContactMessage
    template_name = 'dashboard/message_list.html'
    ordering = '-created'


# --- CMS SETTINGS ---

class DashboardSettingsView(LoginRequiredMixin, SuperuserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Settings
    form_class = SettingsForm
    template_name = 'dashboard/settings_form.html'
    success_url = reverse_lazy('admin_dashboard')
    success_message = "Les paramètres du site ont été mis à jour."

    def get_object(self, queryset=None):
        obj, created = Settings.objects.get_or_create(id=Settings.objects.first().id if Settings.objects.exists() else None)
        return obj


def home(request):
    appartements = Appartement.objects.filter(is_featured=True).order_by('-created')[:3]
    if not appartements:
        appartements = Appartement.objects.order_by('-created')[:3]
    return render(request, "home.html", {'appartements': appartements})


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


def service(request):
    return render(request, "service.html")


def liste(request):
    return render(request, "liste.html")


def detail(request):
    return render(request, "detail.html")