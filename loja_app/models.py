from django.conf import settings
from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=120)

    def __str__(self):
        return self.nome


TAMANHO_CHOICES = (
    ('P', 'P'),
    ('M', 'M'),
    ('G', 'G'),
    ('GG', 'GG'),
)


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='produtos'
    )
    imagem = models.ImageField(
        upload_to='produtos/',
        blank=True,
        null=True
    )

    # NOVO: tamanho (use para categoria Camisas)
    tamanho = models.CharField(
        max_length=2,
        choices=TAMANHO_CHOICES,
        blank=True,
        null=True,
        help_text='Use apenas para produtos da categoria "Camisas".'
    )

    # NOVO: prazo de entrega (texto livre)
    prazo_entrega = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Ex.: "5 dias úteis", "Pronta entrega", etc.'
    )

    def __str__(self):
        return self.nome


class Pedido(models.Model):

    STATUS_CHOICES = [
        ('novo', 'Novo'),
        ('aguardando_pagamento', 'Aguardando pagamento'),
        ('pago', 'Pago'),
        ('processando', 'Processando'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]

    nome = models.CharField(max_length=150)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    pagamento = models.CharField(max_length=30)  # PIX ou Cartão
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='novo')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.nome}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    nome_produto = models.CharField(max_length=100)
    quantidade = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome_produto