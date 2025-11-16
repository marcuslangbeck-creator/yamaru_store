from django.contrib import admin
from .models import Categoria, Produto, Pedido, ItemPedido

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'categoria', 'tamanho', 'prazo_entrega')
    list_filter = ('categoria', 'tamanho')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display  = ('id', 'nome', 'telefone', 'pagamento', 'total', 'criado_em')
    list_filter   = ('pagamento', 'criado_em')
    search_fields = ('nome', 'telefone')

@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display  = ('id', 'pedido', 'nome_produto', 'quantidade', 'subtotal')
    list_filter   = ('pedido',)
