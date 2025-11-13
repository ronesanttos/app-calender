from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from werkzeug.security import generate_password_hash, check_password_hash #type:ignore
import jwt #type:ignore
from django.conf import settings
from home.forms import RegisterForm
from home.models import User
from home.jwt_utils import generate_jwt_token
from django.shortcuts import redirect, render

@csrf_exempt
def register_api(request):

    # 🔹 GET → renderiza o template do register
    if request.method == "GET":
        return render(request, "home/register.html")

    # 🔹 Apenas aceita POST
    if request.method != "POST":
        return JsonResponse({"error": "Método inválido"}, status=405)

    # 🔹 Tenta ler JSON ou form-data
    try:
        if request.body:
            data = json.loads(request.body)
        else:
            data = request.POST.dict()
    except Exception:
        data = request.POST.dict()

    # 🔹 Validação
    form = RegisterForm(data)
    
    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=400)

    email = form.cleaned_data["email"]

    # 🔹 Checa se email já existe
    if User.objects(email=email).first():
        return JsonResponse(
            {"error": "Email já está cadastrado"},
            status=400
        )

    # 🔹 Cria usuário
    user = User(
        nome=form.cleaned_data["nome"],
        email=email,
        password=generate_password_hash(form.cleaned_data["password"])
    )
    user.save()

    # 🔹 Gera token JWT
    token = generate_jwt_token(user)

    response = JsonResponse({
        "message": "Usuário criado com sucesso",
        "token": token,
        "redirect": "/login/"
    })

    # 🔹 Salva cookie
    response.set_cookie(
        key="jwt",
        value=token,
        httponly=True,
        samesite="Lax"
    )

    return response


@csrf_exempt
def login_api(request):
    # 🔹 GET → renderiza o template de login
    if request.method == "GET":
        return render(request, "home/login.html")

    # 🔹 POST → autenticação
    if request.method != "POST":
        return JsonResponse({"error": "Método inválido"}, status=405)

    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    email = data.get("email")
    password = data.get("password")

    # 🔹 Valida dados básicos
    if not email or not password:
        return JsonResponse({"error": "Email e senha são obrigatórios"}, status=400)

    # 🔹 Busca o usuário
    user = User.objects(email=email).first()
    if not user:
        return JsonResponse({"error": "Usuário não encontrado"}, status=404)

    # 🔹 Valida senha
    if not check_password_hash(user.password, password):
        return JsonResponse({"error": "Senha incorreta"}, status=401)

    # 🔹 Gera token JWT
    token = generate_jwt_token(user)

    response = JsonResponse({
        "message": "Login realizado com sucesso",
        "token": token
    })

    # 🔹 Salva JWT em cookie
    response.set_cookie(
        key="jwt",
        value=token,
        httponly=True,
        samesite="Lax"
    )

    return response

@csrf_exempt
def update_user(request):
    token = request.COOKIES.get("jwt")
    
    if not token:
        return redirect("home:login")  # se não tiver token, vai pro login

    try:
        # decodifica o token JWT
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")

        # busca o usuário no banco
        user = User.objects(id=user_id).first()
        if not user:
            return redirect("home:login")
        
    except (jwt.ExpiredSignatureError, jwt.DecodeError):
        return redirect("home:login")
    
    if request.method == "GET":
        return render(request,'home/update_user.html', {'user':user})

    if request.method == "POST":
        try:
            data = json.loads(request.body) if request.body else request.POST.dict()
            
            nome = data.get("nome")
            email = data.get("email")
            senha = data.get("password")
            
            if nome:
                user.nome = nome
            if email:
                user.email = email
            if senha:
                user.password = generate_password_hash(senha)
            
            user.save()
            
            return JsonResponse({
                'message': 'Usuário atualizado com sucesso!',
                'redirect':'/'
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)