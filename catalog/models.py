from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import default_storage

class Jutsu(models.Model):
    """
    Modelo que representa um Jutsu no universo de Naruto.
    
    Este é nosso "pergaminho mestre" - define exatamente
    o que cada jutsu deve conter e como deve se comportar.
    """
    
    # Classes internas para choices - uma abordagem moderna e clean
    class Elements(models.TextChoices):
        """
        Elementos de chakra disponíveis.
        
        TextChoices é uma funcionalidade moderna do Django que:
        1. Agrupa logicamente as opções
        2. Permite acesso por notação de ponto (ex: Elements.FIRE)
        3. Gera automaticamente labels legíveis
        """
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
        """
        Tipos funcionais de jutsu.
        """
        OFFENSIVE = 'offensive', _('Ofensivo')
        DEFENSIVE = 'defensive', _('Defensivo')
        SUPPORT = 'support', _('Suporte')
        SUPPLEMENTARY = 'supplementary', _('Suplementar')

    class Ranks(models.TextChoices):
        """
        Classificação de dificuldade dos jutsus.
        """
        E = 'E', _('Rank E')
        D = 'D', _('Rank D') 
        C = 'C', _('Rank C')
        B = 'B', _('Rank B')
        A = 'A', _('Rank A')
        S = 'S', _('Rank S')
        SS = 'SS', _('Rank S+')

    # Campos do modelo - como os "atributos" de cada jutsu
    name = models.CharField(
        max_length=100, 
        unique=True,  # Evita jutsus duplicados - como um índice único nos arquivos ninja
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
    
    # Campo automático - Django cria e gerencia automaticamente
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Data e hora em que o jutsu foi registrado no catálogo."
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Data e hora da última atualização do registro."
    )

    class Meta:
        """
        Metadados do modelo - configurações extras.
        """
        verbose_name = "Jutsu"
        verbose_name_plural = "Jutsus"
        ordering = ['name']  # Ordena alfabeticamente por padrão

    def __str__(self):
        """
        Representação em string do objeto.
        
        Este método é CRUCIAL - é como o jutsu vai aparecer
        no admin do Django e em qualquer lugar que precise
        de uma representação textual.
        """
        return f"{self.name} ({self.get_element_type_display()})"
    
    def get_absolute_url(self):
        """
        Retorna a URL canônica para este jutsu.
        
        Útil para links diretos e SEO. Implementaremos isso
        quando criarmos nossas URLs.
        """
        from django.urls import reverse
        return reverse('jutsu-detail', kwargs={'pk': self.pk})
    
    def delete(self, *args, **kwargs):
        """
        Sobrescreve o método delete para remover a imagem quando o jutsu for excluído.
        Isso evita 'arquivos órfãos' no sistema de arquivos.
        """
        # Se houver uma imagem, delete-a
        if self.image and default_storage.exists(self.image.name):
            default_storage.delete(self.image.name)
        
        # Continue com a exclusão normal
        super().delete(*args, **kwargs)