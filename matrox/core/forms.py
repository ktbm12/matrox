from django import forms
from .models import Appartement, Settings, ContactMessage, AppartementImage

class PremiumFormMixin:
    """Mixin pour appliquer les styles Elite Professional aux formulaires."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            common_classes = 'w-full px-8 py-5 bg-white border border-stone-200 rounded-[1.5rem] focus:ring-4 focus:ring-primary/10 focus:border-primary transition-all duration-300 font-medium text-stone-900 placeholder:text-stone-300 shadow-sm'
            
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'w-6 h-6 rounded-lg border-stone-300 text-primary focus:ring-primary/20'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': common_classes + ' min-h-[180px] resize-none',
                    'placeholder': f"Saisissez le {field.label.lower()} ici..."
                })
            elif isinstance(field.widget, (forms.ClearableFileInput, forms.FileInput)):
                 field.widget.attrs.update({'class': 'block w-full text-sm text-stone-500 file:mr-4 file:py-3 file:px-6 file:rounded-xl file:border-0 file:text-[11px] file:font-black file:uppercase file:tracking-widest file:bg-matrox-dark file:text-white hover:file:bg-primary transition-all cursor-pointer'})
            else:
                field.widget.attrs.update({
                    'class': common_classes,
                    'placeholder': field.label
                })

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput(attrs={'multiple': True}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)] if data else []
        return result

class AppartementForm(PremiumFormMixin, forms.ModelForm):
    gallery_images = MultipleFileField(
        required=False,
        label="Images Galerie"
    )

    class Meta:
        model = Appartement
        fields = [
            'name', 'location', 'neighborhood', 'description', 
            'price_per_night', 'bedrooms', 'bathrooms', 'max_guests', 
            'main_image', 'is_featured', 'status'
        ]

class SettingsForm(PremiumFormMixin, forms.ModelForm):
    class Meta:
        model = Settings
        fields = [
            'site_name', 'logo_text_main', 'logo_text_sub', 
            'contact_email', 'contact_phone', 'office_address',
            'facebook_url', 'instagram_url', 'whatsapp_number', 'status'
        ]

class AppartementImageForm(PremiumFormMixin, forms.ModelForm):
    class Meta:
        model = AppartementImage
        fields = ['image', 'alt_text', 'order', 'status']
