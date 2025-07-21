from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q, Count  # Para buscas complexas e agregações
from .models import Jutsu
from django.contrib.auth.mixins import LoginRequiredMixin  # Importa o mixin para controle de acesso
from .forms import JutsuForm

class JutsuListView(ListView):
    """
    View para listar todos os jutsus com funcionalidades de busca e filtro.
    
    ListView é perfeita para "mostrar uma lista de coisas" - o Django
    já sabe como paginar, como passar os dados para o template, etc.
    """
    model = Jutsu
    template_name = 'catalog/jutsu_list.html' 
    context_object_name = 'jutsus'  # Nome que usaremos no template
    paginate_by = 12  # Quantos jutsus por página
    
    def get_queryset(self):
        """
        Personaliza quais jutsus serão mostrados.
        
        Este método é chamado automaticamente pelo ListView.
        Aqui podemos adicionar filtros, buscas, ordenação, etc.
        """
        queryset = super().get_queryset() # A ordenação já está no model Meta
        
        # Implementar busca por nome ou descrição
        search_query = self.request.GET.get('search')
        if search_query:
            # O objeto Q permite construir queries complexas. Aqui, usamos o operador OR (|).
            # 'icontains' significa 'case-insensitive contains' (contém, ignorando maiúsculas/minúsculas)
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        # Implementar filtro por elemento
        element_filter = self.request.GET.get('element')
        if element_filter:
            queryset = queryset.filter(element_type=element_filter)
            
        # Implementar filtro por tipo
        type_filter = self.request.GET.get('type')
        if type_filter:
            queryset = queryset.filter(jutsu_type=type_filter)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        """
        Adiciona dados extras ao contexto do template.
        
        Além da lista de jutsus, vamos passar as opções de filtro
        para construir nossos dropdowns dinamicamente.
        """
        context = super().get_context_data(**kwargs)
        
        # Adicionar opções de filtro ao contexto
        context['element_choices'] = Jutsu.Elements.choices
        context['type_choices'] = Jutsu.Types.choices
        
        # Manter os filtros atuais para o template saber qual está ativo
        context['current_search'] = self.request.GET.get('search', '')
        context['current_element'] = self.request.GET.get('element', '')
        context['current_type'] = self.request.GET.get('type', '')
        
        return context

class JutsuDetailView(DetailView):
    """
    View para mostrar os detalhes completos de um jutsu específico.
    
    DetailView é perfeita para "mostrar uma coisa específica".
    Ela automaticamente pega o objeto baseado no ID (pk) da URL.
    """
    model = Jutsu
    template_name = 'catalog/jutsu_detail.html'
    context_object_name = 'jutsu'

class JutsuCreateView(LoginRequiredMixin, CreateView):
    """
    View para criar um novo jutsu. Exige que o usuário esteja logado.
    
    CreateView já sabe como:
    - Mostrar um formulário (GET request)
    - Processar o formulário submetido (POST request)  
    - Validar os dados
    - Salvar no banco de dados
    - Redirecionar após sucesso
    """
    model = Jutsu
    form_class = JutsuForm  # Use o formulário personalizado
    template_name = 'catalog/jutsu_form.html'
    success_url = reverse_lazy('jutsu-list')
    
    def get_context_data(self, **kwargs):
        """Adiciona informações extras para o template."""
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Adicionar Novo Jutsu ao Catálogo'
        context['submit_text'] = 'Registrar Jutsu'
        return context

class JutsuUpdateView(LoginRequiredMixin, UpdateView):
    """
    View para editar um jutsu existente. Exige que o usuário esteja logado.
    
    Muito similar ao CreateView, mas trabalha com um objeto existente que ela
    busca automaticamente usando o ID (pk) da URL.
    """
    model = Jutsu
    form_class = JutsuForm  # Use o formulário personalizado
    template_name = 'catalog/jutsu_form.html'
    success_url = reverse_lazy('jutsu-list')
    
    def get_context_data(self, **kwargs):
        """Adiciona o título e o texto do botão ao contexto."""
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Editar Pergaminho: {self.object.name}'
        context['submit_text'] = 'Atualizar Jutsu'
        return context

class JutsuDeleteView(LoginRequiredMixin, DeleteView):
    """
    View para excluir um jutsu. Exige que o usuário esteja logado.
    
    DeleteView mostra uma página de confirmação (GET request) e exclui
    o objeto ao receber um POST request. Uma medida de segurança para
    evitar exclusões acidentais.
    """
    model = Jutsu
    template_name = 'catalog/jutsu_confirm_delete.html'
    context_object_name = 'jutsu'
    success_url = reverse_lazy('jutsu-list')
    
class DashboardView(TemplateView):
    """
    View para exibir estatísticas sobre os jutsus cadastrados.
    
    Esta view demonstra como usar agregação em Django para criar
    estatísticas e visualizações de dados.
    """
    template_name = 'catalog/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estatísticas básicas
        context['total_jutsus'] = Jutsu.objects.count()
        context['total_elements'] = Jutsu.objects.values('element_type').distinct().count()
        
        # Distribuição por elemento
        elements_data = Jutsu.objects.values('element_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Formatar para gráficos JavaScript
        context['elements_labels'] = [item['element_type'] for item in elements_data]
        context['elements_data'] = [item['count'] for item in elements_data]
        
        # Distribuição por tipo
        types_data = Jutsu.objects.values('jutsu_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        context['types_labels'] = [item['jutsu_type'] for item in types_data]
        context['types_data'] = [item['count'] for item in types_data]
        
        # Distribuição por rank
        ranks_data = Jutsu.objects.values('rank').annotate(
            count=Count('id')
        ).order_by('rank')
        
        context['ranks_labels'] = [item['rank'] for item in ranks_data]
        context['ranks_data'] = [item['count'] for item in ranks_data]
        
        # Jutsus mais recentes
        context['recent_jutsus'] = Jutsu.objects.order_by('-created_at')[:5]
        
        return context