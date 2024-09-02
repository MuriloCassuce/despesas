from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Gastos
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect


# Create your views here.

#Verificação index
def index(request):
    gastos = Gastos.objects.all()
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    return(render(request, "usuarios/usuario.html", {
        "gastos": gastos
    }))

#Página de login // Em breve cadastro
def login_view(request):
    
    if request.method=="POST":
        usuario = request.POST.get("usuario")
        senha = request.POST.get("senha")
        usuario = authenticate(request, username = usuario, password = senha)
        
        if usuario is not None:
            login(request, usuario)
            return HttpResponseRedirect(reverse("index"))
        
        else:
            return render(request, "usuarios/login.html", {
                "mensagem": "Credenciais inválidas"
            })
    
    return render(request, "usuarios/login.html")

#Página de logout retornando o login
def logout_view(request):
    logout(request)
    return render(request, "usuarios/login.html", {
        "mensagem": "Logout realizado com sucesso!"
    })

#Pagina de criação de gastos // em breve data
def criar_gasto(request):
    if request.method == "POST":
        cartao = request.POST.get("cartao").capitalize()
        categoria = request.POST.get("categoria")
        item = request.POST.get("item").capitalize()
        valor = float(request.POST.get("valor"))
        parcelas = int(request.POST.get("parcelas"))
        p = Gastos(cartao=cartao, categoria=categoria, item=item, valor=valor, parcelas=parcelas)
        p.save()
        return redirect('criar_gasto')
    
    gastos = Gastos.objects.all()
    
    return render(request, "usuarios/usuario.html", {
        "gastos": gastos,
    })

#Páguna de visualizar gastos individualmente // em breve gráficos
def gastosIndividuais(request):
    cartoes = Gastos.objects.values_list('cartao', flat=True).distinct()
    cartoes_filtrados = None

    if request.method == "POST":
        cartao_buscado = request.POST.get("cartao")
        cartoes_filtrados = Gastos.objects.filter(cartao=cartao_buscado)
    
    return render(request, 'usuarios/gastosIndividuais.html', {
        'cartoes': cartoes,
        'gastos': cartoes_filtrados
    })


    