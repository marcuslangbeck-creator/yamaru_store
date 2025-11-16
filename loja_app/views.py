from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import Produto, Categoria, Pedido, ItemPedido


# ============================
#   FUNÇÕES CARRINHO (SESSÃO)
# ============================

def _get_carrinho(request):
    return request.session.get('carrinho', {})


def _salvar_carrinho(request, carrinho):
    request.session['carrinho'] = carrinho
    request.session.modified = True


# ============================
#   PÁGINAS PRINCIPAIS
# ============================

def home(request):
    produtos = Produto.objects.all()
    return render(request, 'home.html', {'produtos': produtos})


def produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    return render(request, 'produto.html', {'produto': produto})


def categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias.html', {'categorias': categorias})


def categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    produtos = Produto.objects.filter(categoria=categoria)
    contexto = {
        'categoria': categoria,
        'produtos': produtos,
    }
    return render(request, 'categoria.html', contexto)


# ============================
#   CARRINHO
# ============================

def adicionar_ao_carrinho(request, id):
    produto = get_object_or_404(Produto, id=id)
    carrinho = _get_carrinho(request)
    pid = str(produto.id)

    if pid in carrinho:
        carrinho[pid]['quantidade'] += 1
    else:
        carrinho[pid] = {
            'nome': produto.nome,
            'preco': float(produto.preco),
            'quantidade': 1,
        }

    _salvar_carrinho(request, carrinho)
    return redirect('carrinho')


def remover_do_carrinho(request, id):
    carrinho = _get_carrinho(request)
    pid = str(id)

    if pid in carrinho:
        del carrinho[pid]
        _salvar_carrinho(request, carrinho)

    return redirect('carrinho')


def aumentar_qtd(request, id):
    carrinho = _get_carrinho(request)
    pid = str(id)

    if pid in carrinho:
        carrinho[pid]['quantidade'] += 1
        _salvar_carrinho(request, carrinho)

    return redirect('carrinho')


def diminuir_qtd(request, id):
    carrinho = _get_carrinho(request)
    pid = str(id)

    if pid in carrinho:
        carrinho[pid]['quantidade'] -= 1

        if carrinho[pid]['quantidade'] <= 0:
            del carrinho[pid]

        _salvar_carrinho(request, carrinho)

    return redirect('carrinho')


def carrinho(request):
    carrinho = _get_carrinho(request)

    itens = []
    total = 0

    for pid, dados in carrinho.items():
        subtotal = dados['preco'] * dados['quantidade']
        total += subtotal

        itens.append({
            'id': pid,
            'nome': dados['nome'],
            'preco': dados['preco'],
            'quantidade': dados['quantidade'],
            'subtotal': subtotal,
        })

    contexto = {
        'itens': itens,
        'total': total,
    }

    return render(request, 'carrinho.html', contexto)


# ============================
#   CHECKOUT + FINALIZAR PEDIDO
# ============================

def checkout(request):
    carrinho = _get_carrinho(request)

    if not carrinho:
        return redirect('carrinho')

    itens = []
    total = 0

    for pid, dados in carrinho.items():
        subtotal = dados['preco'] * dados['quantidade']
        total += subtotal
        itens.append({
            'id': pid,
            'nome': dados['nome'],
            'quantidade': dados['quantidade'],
            'subtotal': subtotal,
        })

    contexto = {
        'itens': itens,
        'total': total,
    }

    return render(request, 'checkout.html', contexto)


def finalizar_pedido(request):
    if request.method != 'POST':
        return redirect('checkout')

    carrinho = _get_carrinho(request)
    if not carrinho:
        return redirect('carrinho')

    nome = request.POST.get('nome')
    endereco = request.POST.get('endereco')
    telefone = request.POST.get('telefone')
    pagamento = request.POST.get('pagamento')

    itens = []
    total = 0

    for pid, dados in carrinho.items():
        subtotal = dados['preco'] * dados['quantidade']
        total += subtotal
        itens.append({
            'nome': dados['nome'],
            'quantidade': dados['quantidade'],
            'subtotal': subtotal,
        })

    pedido = Pedido.objects.create(
        usuario=request.user if request.user.is_authenticated else None,
        nome=nome,
        endereco=endereco,
        telefone=telefone,
        pagamento=pagamento,
        total=total,
    )

    for item in itens:
        ItemPedido.objects.create(
            pedido=pedido,
            nome_produto=item['nome'],
            quantidade=item['quantidade'],
            subtotal=item['subtotal'],
        )

    # Limpa carrinho
    request.session['carrinho'] = {}
    request.session.modified = True

    return redirect('pedido_finalizado', id=pedido.id)


def pedido_finalizado(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    contexto = {
        'pedido': pedido,
        'itens': pedido.itens.all(),
    }
    return render(request, 'pedido_finalizado.html', contexto)


# ============================
#   ÁREA DO CLIENTE
# ============================

def registrar(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registrar.html', {'form': form})


@login_required

def meus_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-criado_em')
    return render(request, 'meus_pedidos.html', {'pedidos': pedidos})
def checkout(request):
    carrinho = _get_carrinho(request)

    itens = []
    total = 0

    for pid, dados in carrinho.items():
        subtotal = dados['preco'] * dados['quantidade']
        total += subtotal
        itens.append({
            'id': pid,
            'nome': dados['nome'],
            'quantidade': dados['quantidade'],
            'subtotal': subtotal,
        })

    if not itens:
        return redirect('carrinho')

    contexto = {
        'itens': itens,
        'total': total,
    }
    return render(request, 'checkout.html', contexto)


def finalizar_pedido(request):
    if request.method != 'POST':
        return redirect('checkout')

    carrinho = request.session.get('carrinho', {})

    if not carrinho:
        return redirect('carrinho')

    nome = request.POST.get('nome')
    endereco = request.POST.get('endereco')
    telefone = request.POST.get('telefone')
    pagamento = request.POST.get('pagamento')

    itens = []
    total = 0

    for pid, dados in carrinho.items():
        subtotal = float(dados['preco']) * int(dados['quantidade'])
        total += subtotal
        itens.append({
            'nome': dados['nome'],
            'quantidade': dados['quantidade'],
            'subtotal': subtotal,
        })

    # Cria o pedido
    pedido = Pedido.objects.create(
        nome=nome,
        endereco=endereco,
        telefone=telefone,
        pagamento=pagamento,
        total=total,
    )

    # Salva itens
    for item in itens:
        ItemPedido.objects.create(
            pedido=pedido,
            nome_produto=item['nome'],
            quantidade=item['quantidade'],
            subtotal=item['subtotal'],
        )

    # Limpa carrinho
    request.session['carrinho'] = {}
    request.session.modified = True

    return redirect('pedido_finalizado', id=pedido.id)


def pedido_finalizado(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    return render(request, 'pedido_finalizado.html', {'pedido': pedido})


def meus_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-criado_em')
    contexto = {'pedidos': pedidos}
    return render(request, 'meus_pedidos.html', contexto)


def registrar(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registrar.html', {'form': form})

