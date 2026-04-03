from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Appartement, ContactMessage, Settings, AppartementImage


class AppartementImageInline(admin.TabularInline):
    model = AppartementImage
    extra = 1
    fields = ('image', 'alt_text', 'order', 'status')


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'contact_email', 'contact_phone', 'created', 'status')
    list_editable = ('status',)
    fieldsets = (
        (_('Infos Générales'), {
            'fields': ('site_name', 'status', 'author')
        }),
        (_('Identité Visuelle'), {
            'fields': ('logo_text_main', 'logo_text_sub')
        }),
        (_('Contact & Localisation'), {
            'fields': ('contact_email', 'contact_phone', 'office_address')
        }),
        (_('Réseaux Sociaux'), {
            'fields': ('facebook_url', 'instagram_url', 'whatsapp_number')
        }),
        (_('Avancé'), {
            'classes': ('collapse',),
            'fields': ('metadata', 'is_deleted')
        }),
    )

    def has_add_permission(self, request):
        # Limite à une seule instance de paramètres (Singleton)
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(Appartement)
class AppartementAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'neighborhood', 'price_per_night', 'status', 'is_featured')
    list_filter = ('location', 'status', 'is_featured', 'created')
    search_fields = ('name', 'neighborhood', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('status', 'is_featured')
    
    fieldsets = (
        (_('Informations de base'), {
            'fields': ('name', 'slug', 'location', 'neighborhood', 'status')
        }),
        (_('Détails & Prix'), {
            'fields': ('description', 'price_per_night', 'bedrooms', 'bathrooms', 'max_guests')
        }),
        (_('Médias & Visibilité'), {
            'fields': ('main_image', 'is_featured', 'amenities')
        }),
        (_('Géo-localisation'), {
            'fields': ('latitude', 'longitude')
        }),
        (_('Métadonnées'), {
            'classes': ('collapse',),
            'fields': ('author', 'metadata', 'is_deleted')
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'subject', 'email', 'created', 'is_read')
    list_filter = ('is_read', 'created')
    search_fields = ('full_name', 'email', 'subject', 'message')
    readonly_fields = ('created', 'modified', 'author')
    list_editable = ('is_read',)
    
    fieldsets = (
        (_('Expéditeur'), {
            'fields': ('full_name', 'email', 'phone')
        }),
        (_('Contenu du Message'), {
            'fields': ('subject', 'message', 'is_read')
        }),
        (_('Infos Techniques'), {
            'classes': ('collapse',),
            'fields': ('author', 'metadata', 'is_deleted', 'created', 'modified')
        }),
    )
