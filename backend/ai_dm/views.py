from django.shortcuts import render
from .utils import generate_ai_response
# Create your views here.

def ai_dm_chat(request):
    bot_response = None
    if request.method == "POST":
        user_input = request.POST.get("user_input")
        bot_response = generate_ai_response(user_input)
    return render(request, "ai_dm/chat.html", {"bot_response": bot_response})

