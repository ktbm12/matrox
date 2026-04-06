import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django_extensions.db.models import ActivatorModel
from model_utils.models import TimeStampedModel


class SentinelBaseModel(TimeStampedModel, ActivatorModel):
    """
    Modèle abstrait de base pour tous les modèles BTP Sentinel.

    Fournit :
    - Clé primaire UUID
    - Horodatages created / modified (via TimeStampedModel)
    - Statut activer / désactiver (via ActivatorModel)
    - Indicateur de suppression douce
    - Métadonnées JSON flexibles
    - Champ auteur (email, téléphone ou identifiant quelconque)
    """

    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        null=False,
        blank=False,
        editable=False,
    )
    is_deleted = models.BooleanField(_("supprimé"), default=False)
    metadata = models.JSONField(_("métadonnées"), default=dict, null=True, blank=True)
    author = models.CharField(_("auteur"), max_length=255, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ("created",)


class Settings(SentinelBaseModel):
    """
    Paramètres globaux du site MatRox (Singleton).
    """
    site_name = models.CharField(_("Nom du site"), max_length=100, default="MatRox Residence")
    contact_email = models.EmailField(_("Email de contact"), blank=True)
    contact_phone = models.CharField(_("Téléphone de contact"), max_length=50, blank=True)
    office_address = models.TextField(_("Adresse du bureau"), blank=True)
    
    logo_text_main = models.CharField(_("Texte Logo (Principal)"), max_length=50, default="MatRox")
    logo_text_sub = models.CharField(_("Texte Logo (Sous-titre)"), max_length=50, default="Residence")
    
    facebook_url = models.URLField(_("Facebook"), blank=True)
    instagram_url = models.URLField(_("Instagram"), blank=True)
    whatsapp_number = models.CharField(_("WhatsApp"), max_length=50, blank=True)

    class Meta:
        verbose_name = _("Paramètres")
        verbose_name_plural = _("Paramètres")

    def __str__(self):
        return self.site_name


class Appartement(SentinelBaseModel):
    """
    Représente une résidence ou un appartement MatRox.
    """
    LOCATIONS = [
        ('douala', _('Douala')),
        ('yaounde', _('Yaoundé')),
        ('kribi', _('Kribi')),
    ]

    name = models.CharField(_("Nom de l'appartement"), max_length=255)
    slug = models.SlugField(_("URL simplifiée"), unique=True, max_length=255)
    location = models.CharField(_("Localisation"), max_length=50, choices=LOCATIONS)
    neighborhood = models.CharField(_("Quartier"), max_length=100, help_text="Ex: Bastos, Bonapriso")
    
    description = models.TextField(_("Description détaillée"), blank=True)
    price_per_night = models.DecimalField(_("Prix par nuit (FCFA)"), max_digits=12, decimal_places=2)
    
    bedrooms = models.PositiveIntegerField(_("Chambres"), default=1)
    bathrooms = models.PositiveIntegerField(_("Salles de bain"), default=1)
    max_guests = models.PositiveIntegerField(_("Voyageurs max"), default=2)
    
    main_image = models.ImageField(_("Image principale"), upload_to="appartements/", null=True, blank=True)
    is_featured = models.BooleanField(_("Mettre en avant"), default=False)
    
    amenities = models.JSONField(_("Équipements"), default=list, blank=True)
    
    latitude = models.FloatField(_("Latitude"), null=True, blank=True)
    longitude = models.FloatField(_("Longitude"), null=True, blank=True)

    class Meta:
        verbose_name = _("Appartement")
        verbose_name_plural = _("Appartements")
        ordering = ("-created",)

    def __str__(self):
        return f"{self.name} - {self.neighborhood}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            original_slug = self.slug
            counter = 1
            while Appartement.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)


class ContactMessage(SentinelBaseModel):
    """
    Représente un message envoyé via le formulaire de contact.
    """
    full_name = models.CharField(_("Nom complet"), max_length=255)
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Téléphone"), max_length=50, blank=True)
    subject = models.CharField(_("Sujet"), max_length=255)
    message = models.TextField(_("Message"))
    
    is_read = models.BooleanField(_("Lu"), default=False)

    class Meta:
        verbose_name = _("Message de contact")
        verbose_name_plural = _("Messages de contact")
        ordering = ("-created",)

    def __str__(self):
        return f"{self.full_name} - {self.subject}"


class AppartementImage(SentinelBaseModel):
    """
    Images secondaires pour la galerie d'un appartement.
    """
    appartement = models.ForeignKey(Appartement, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(_("Image"), upload_to="appartements/gallery/")
    alt_text = models.CharField(_("Texte alternatif"), max_length=255, blank=True)
    order = models.PositiveIntegerField(_("Ordre d'affichage"), default=0)

    class Meta:
        verbose_name = _("Image d'appartement")
        verbose_name_plural = _("Images d'appartement")
        ordering = ("order", "created")

    def __str__(self):
        return f"Image pour {self.appartement.name}"
