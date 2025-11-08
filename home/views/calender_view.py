from django.shortcuts import render
from django.http import JsonResponse
from home.models import Evento
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date

@csrf_exempt
def eventos_json(request):
    if request.method == 'GET':
        eventos = Evento.objects(data_evento__ne=None)
        data = []
        for e in eventos:
            if e.data_evento:
                data.append({
                    "id": str(e.id),
                    "title": e.nome,
                    "start": e.data_evento.isoformat() if e.data_evento else None,
                    "allDay": True,
                })
        return JsonResponse(data, safe=False)

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

            evento = Evento.objects.create(
                nome=nome,
                data_evento=data_convertida
            )

            return JsonResponse({
                "id": str(evento.id),
                "title": evento.nome,
                "start": evento.data_evento.isoformat() if evento.data_evento else None,
                "allDay": True,
            }, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
    elif request.method == "DELETE":
        try:
            data = json.loads(request.body)
            event_id = data.get("id")            
            
            evento = Evento.objects.filter(id=event_id).first()
            if not evento:
                return JsonResponse({"error": "Evento não encontrado"}, status=404)
            
            evento.delete()
            return JsonResponse({"success":True})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
    
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            event_id = data.get("id")
            nome = data.get("nome")
            
            evento = Evento.objects.filter(id=event_id).first()
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
def calendario(request):
    return render(request,'home/index.html')