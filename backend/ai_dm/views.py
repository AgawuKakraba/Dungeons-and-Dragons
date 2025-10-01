# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .utils import generate_ai_response

# dummy player list
PLAYERS = ["Alice", "Bob", "Charlie", "Diana"]

def chat_view(request):
    if request.method == "POST":
        user_input = request.POST.get("message", "")
        response = generate_ai_response(user_input, PLAYERS)
        return JsonResponse({"response": response})
    return render(request, "ai_dm/chat.html")