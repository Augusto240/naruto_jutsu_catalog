# 🍥 Naruto Jutsu Catalog

Catálogo completo de jutsus do universo Naruto, desenvolvido com Django, oferecendo sistema de busca, filtragem, dashboard com estatísticas e API REST documentada.

![Naruto Logo](https://gifman.net/wp-content/uploads/2021/11/naruto-e-sasuke-engracado-01.gif)

## 📋 Sobre o Projeto

Este projeto é um CRUD completo para catalogar as técnicas ninjas (jutsus) do universo Naruto, permitindo visualizar, filtrar, adicionar, editar e excluir jutsus, além de oferecer uma API REST para integração com outros sistemas.

## 🚀 Tecnologias Utilizadas

- **Backend:** Django 5.2, Django REST Framework
- **Frontend:** Bootstrap 5, Chart.js, Font Awesome
- **Banco de Dados:** SQLite
- **Extras:** Django Debug Toolbar, Crispy Forms, Swagger/OpenAPI

## 🔧 Como Instalar e Executar

```bash
# Clonar o repositório
git clone https://github.com/Augusto240/naruto-jutsu-catalog.git
cd naruto-jutsu-catalog

# Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Executar migrações
python manage.py migrate

# Criar superusuário (opcional)
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver

```

Acesse:

Aplicação: http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

API: http://127.0.0.1:8000/api/

Documentação API: http://127.0.0.1:8000/swagger/


## ✨ Funcionalidades
- Visualização de todos os jutsus com detalhes
- Filtragem por elemento (Fogo, Água, etc.) e tipo (Ofensivo, Defensivo)
- Busca por nome ou descrição
- Dashboard com estatísticas e gráficos
- API REST com documentação Swagger
- Upload de imagens para jutsus
- Sistema de permissões: somente usuários autenticados podem criar/editar


## 📂 Estrutura do Projeto

```
naruto_jutsu_catalog/
├── catalog/                # Aplicação principal
│   ├── templates/          # Templates HTML
│   ├── models.py           # Modelos de dados
│   ├── views.py            # Views da aplicação
│   ├── api_views.py        # Views da API REST
│   └── ...
├── media/                  # Arquivos de mídia
├── requirements.txt        # Dependências
└── manage.py               # Script de gerenciamento
```

## 👤 Autor
Augusto Oliveira 

Desenvolvido com 💖, chakra e Python!