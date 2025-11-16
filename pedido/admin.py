from django.contrib import admin
from .models import Pedido, ItemPedido, Produto, Categoria

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'telefone', 'total', 'pagamento', 'status', 'criado_em')
    list_filter = ('status', 'pagamento')
    search_fields = ('nome', 'telefone')
    list_editable = ('status',)

@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'nome_produto', 'quantidade', 'subtotal')

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'preco', 'categoria')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
