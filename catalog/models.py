from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import default_storage

class Jutsu(models.Model):

    class Elements(models.TextChoices):

        FIRE = 'fire', _('Fogo')
        WATER = 'water', _('Água') 
        WIND = 'wind', _('Vento')
        EARTH = 'earth', _('Terra')
        LIGHTNING = 'lightning', _('Raio')
        ILLUSION = 'illusion', _('Genjutsu')
        YIN = 'yin', _('Yin')
        YANG = 'yang', _('Yang')
        YIN_YANG = 'yin-yang', _('Yin-Yang')
        OTHER = 'other', _('Outro')

    class Types(models.TextChoices):

        OFFENSIVE = 'offensive', _('Ofensivo')
        DEFENSIVE = 'defensive', _('Defensivo')
        SUPPORT = 'support', _('Suporte')
        SUPPLEMENTARY = 'supplementary', _('Suplementar')

    class Ranks(models.TextChoices):
        E = 'E', _('Rank E')
        D = 'D', _('Rank D') 
        C = 'C', _('Rank C')
        B = 'B', _('Rank B')
        A = 'A', _('Rank A')
        S = 'S', _('Rank S')
        SS = 'SS', _('Rank S+')

    name = models.CharField(
        max_length=100, 
        unique=True,  
        help_text="O nome único do jutsu."
    )
    
    description = models.TextField(
        help_text="Uma descrição detalhada do jutsu, seus efeitos e como é executado."
    )
    
    element_type = models.CharField(
        max_length=20,
        choices=Elements.choices,
        default=Elements.OTHER,
        help_text="O elemento de chakra principal do jutsu."
    )
    
    jutsu_type = models.CharField(
        max_length=20,
        choices=Types.choices, 
        default=Types.SUPPLEMENTARY,
        help_text="A classificação funcional do jutsu."
    )
    
    rank = models.CharField(
        max_length=2,
        choices=Ranks.choices,
        default=Ranks.C,
        help_text="A classificação de dificuldade do jutsu."
    )
    
    image = models.ImageField(
        upload_to='jutsu_images/',
        null=True,
        blank=True,
        help_text="Uma imagem representativa do jutsu."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Data e hora em que o jutsu foi registrado no catálogo."
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Data e hora da última atualização do registro."
    )

    class Meta:
        verbose_name = "Jutsu"
        verbose_name_plural = "Jutsus"
        ordering = ['name'] 

    def __str__(self):
        return f"{self.name} ({self.get_element_type_display()})"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('jutsu-detail', kwargs={'pk': self.pk})
    
    def delete(self, *args, **kwargs):
        if self.image and default_storage.exists(self.image.name):
            default_storage.delete(self.image.name)
        super().delete(*args, **kwargs)