from django.shortcuts import render, redirect
from django.http import JsonResponse
from home.models import Evento, User
import jwt #type:ignore
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date


def calendario(request):
    token = request.COOKIES.get("jwt")

    if not token:
        return redirect("home:login")  # se não tiver token, vai pro login

    try:
        # decodifica o token JWT
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")

        # busca o usuário no banco
        user = User.objects(id=user_id).first()
        
    except jwt.ExpiredSignatureError:
        return redirect("home:login")
    except jwt.DecodeError:
        return redirect("home:login")

    context = {'user':user}
    
    # renderiza o template e envia o nome do usuário
    return render(request, "home/index.html", context)


@csrf_exempt
def eventos_json(request):
    token = request.COOKIES.get("jwt")
    if not token:
        return JsonResponse({"error": "Não autorizado"}, status=401)

    # 🔹 Autenticação via JWT
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        user = User.objects(id=user_id).first()
        
        if not user:
            return JsonResponse({"error": "Usuário não encontrado"}, status=404)
        
    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "Token expirado"}, status=401)
    except jwt.DecodeError:
        return JsonResponse({"error": "Token inválido"}, status=401)
    
    # 🔹 GET → Retorna apenas os eventos do usuário
    if request.method == 'GET':
        eventos = Evento.objects(user=user)
        data = []
        
        colors = "#3498db"
        for i, e in  enumerate(eventos):
            if e.data_evento:
                cor_usada = colors[i % len(colors)]
                
                # Se o nome do evento for "pago", muda para vermelho
                if  "pago" in e.nome.lower():
                    cor_usada = "#e11d48"
                
                data.append({
                    "id": str(e.id),
                    "title": e.nome,
                    "start": e.data_evento.isoformat() if e.data_evento else None,
                    "allDay": True,
                    "color": cor_usada,
                })
        return JsonResponse(data, safe=False)

    # 🔹 POST → Cria evento para o usuário logado
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            nome = data.get("nome")
            data_str = data.get("data_evento")

            if not nome or not data_str:
                return JsonResponse({"error": "Nome ou data faltando"}, status=400)

            data_convertida = parse_date(data_str)
            if data_convertida is None:
                return JsonResponse({"error": "Data inválida"}, status=400)

            evento = Evento(
                nome=nome,
                data_evento=data_convertida,
                user=user
            )
            evento.save()
            
            return JsonResponse({
                "id": str(evento.id),
                "title": evento.nome,
                "start": evento.data_evento.isoformat() if evento.data_evento else None,
                "allDay": True,
            }, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    # 🔹 DELETE → Só pode deletar eventos do próprio usuário
    elif request.method == "DELETE":
        try:
            data = json.loads(request.body)
            event_id = data.get("id")            
            
            evento = Evento.objects.filter(id=event_id, user=user).first()
            if not evento:
                return JsonResponse({"error": "Evento não encontrado"}, status=404)
            
            evento.delete()
            return JsonResponse({"success":True})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
    # 🔹 PUT → Só pode editar seus próprios eventos
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            event_id = data.get("id")
            nome = data.get("nome")
            
            evento = Evento.objects.filter(id=event_id, user=user).first()
            if not evento:
                return JsonResponse({"error": "Evento não encontrado"}, status=404)
            
            evento.nome = nome
            evento.save()
            
            return JsonResponse({
                "id": str(evento.id),
                "title": evento.nome,
                "start": evento.data_evento.isoformat() if evento.data_evento else None,
                "allDay": True,
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
            
        
    else:
        return JsonResponse({"error": "Método não suportado"}, status=405)

def logout(request):
    response = redirect("home:login")
    response.delete_cookie("jwt")
    return response

def health(request):
    return JsonResponse({"status": "ok"})