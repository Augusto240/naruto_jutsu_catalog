from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q, Count 
from .models import Jutsu
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import JutsuForm

class JutsuListView(ListView):
    model = Jutsu
    template_name = 'catalog/jutsu_list.html' 
    context_object_name = 'jutsus' 
    paginate_by = 12
    def get_queryset(self):
        queryset = super().get_queryset() 

        search_query = self.request.GET.get('search')
        if search_query:           
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )

        element_filter = self.request.GET.get('element')
        if element_filter:
            queryset = queryset.filter(element_type=element_filter)

        type_filter = self.request.GET.get('type')
        if type_filter:
            queryset = queryset.filter(jutsu_type=type_filter)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['element_choices'] = Jutsu.Elements.choices
        context['type_choices'] = Jutsu.Types.choices
        context['current_search'] = self.request.GET.get('search', '')
        context['current_element'] = self.request.GET.get('element', '')
        context['current_type'] = self.request.GET.get('type', '')
        
        return context

class JutsuDetailView(DetailView):
    model = Jutsu
    template_name = 'catalog/jutsu_detail.html'
    context_object_name = 'jutsu'

class JutsuCreateView(LoginRequiredMixin, CreateView):
    model = Jutsu
    form_class = JutsuForm 
    template_name = 'catalog/jutsu_form.html'
    success_url = reverse_lazy('jutsu-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Adicionar Novo Jutsu ao Catálogo'
        context['submit_text'] = 'Registrar Jutsu'
        return context

class JutsuUpdateView(LoginRequiredMixin, UpdateView):
    model = Jutsu
    form_class = JutsuForm
    template_name = 'catalog/jutsu_form.html'
    success_url = reverse_lazy('jutsu-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Editar Pergaminho: {self.object.name}'
        context['submit_text'] = 'Atualizar Jutsu'
        return context

class JutsuDeleteView(LoginRequiredMixin, DeleteView):
    model = Jutsu
    template_name = 'catalog/jutsu_confirm_delete.html'
    context_object_name = 'jutsu'
    success_url = reverse_lazy('jutsu-list')
    
class DashboardView(TemplateView):
    template_name = 'catalog/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_jutsus'] = Jutsu.objects.count()
        context['total_elements'] = Jutsu.objects.values('element_type').distinct().count()
        elements_data = Jutsu.objects.values('element_type').annotate(
            count=Count('id')
        ).order_by('-count')
        context['elements_labels'] = [item['element_type'] for item in elements_data]
        context['elements_data'] = [item['count'] for item in elements_data]
        types_data = Jutsu.objects.values('jutsu_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        context['types_labels'] = [item['jutsu_type'] for item in types_data]
        context['types_data'] = [item['count'] for item in types_data]
        ranks_data = Jutsu.objects.values('rank').annotate(
            count=Count('id')
        ).order_by('rank')
        
        context['ranks_labels'] = [item['rank'] for item in ranks_data]
        context['ranks_data'] = [item['count'] for item in ranks_data]
        context['recent_jutsus'] = Jutsu.objects.order_by('-created_at')[:5]
        
        return context
    
class HomeView(TemplateView):
    template_name = 'catalog/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_jutsus'] = Jutsu.objects.order_by('-created_at')[:3]
        context['fire_jutsus'] = Jutsu.objects.filter(element_type='fire').order_by('?')[:2]
        context['water_jutsus'] = Jutsu.objects.filter(element_type='water').order_by('?')[:2]
        context['high_rank_jutsus'] = Jutsu.objects.filter(rank__in=['A', 'S', 'SS']).order_by('?')[:3]
        context['total_jutsus'] = Jutsu.objects.count()
        
        return context