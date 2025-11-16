from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('categorias/', views.categorias, name='categorias'),
    path('categoria/<int:id>/', views.categoria, name='categoria'),

    path('produto/<int:id>/', views.produto, name='produto'),

    # CARRINHO
    path('carrinho/', views.carrinho, name='carrinho'),
    path('carrinho/adicionar/<int:id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/remover/<int:id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('aumentar/<int:id>/', views.aumentar_qtd, name='aumentar_qtd'),
    path('diminuir/<int:id>/', views.diminuir_qtd, name='diminuir_qtd'),

    # CHECKOUT E PEDIDO
    path('checkout/', views.checkout, name='checkout'),
    path('finalizar/', views.finalizar_pedido, name='finalizar_pedido'),
    path('pedido-finalizado/<int:id>/', views.pedido_finalizado, name='pedido_finalizado'),

    # USUÁRIO
    path('conta/', include('django.contrib.auth.urls')),
    path('registrar/', views.registrar, name='registrar'),
    path('meus_pedidos/', views.meus_pedidos, name='meus_pedidos'),
]
