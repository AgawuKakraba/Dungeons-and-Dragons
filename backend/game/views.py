from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import GameSession, Player, Message
import re, random

# Create your views here.

def welcome(request):
    return render(request, "game/welcome.html")

@login_required
def lobby(request):
    sessions = GameSession.objects.all().order_by('-created_at')
    return render(request, 'game/lobby.html', {'sessions': sessions})

@login_required
def create_session(request):
    if request.method == 'POST':
        name = request.POST.get('name') or "New Adventure"
        gs = GameSession.objects.create(name=name, dm=request.user)
        return redirect('game:session', gs.id)
    return render(request, 'game/create_session.html')

@login_required
def session_view(request, session_id):
    gs = get_object_or_404(GameSession, id=session_id)
    chat_messages = gs.messages.order_by('created_at')
    return render(request, 'game/session.html', {
        'game': gs,
        'chat_messages': chat_messages
    })

@login_required
def post_message(request, session_id):
    if request.method == 'POST':
        gs = get_object_or_404(GameSession, id=session_id)
        content = request.POST.get('content', '').strip()
        if content:
            # Check if it's a dice roll
            dice_match = re.match(r"!roll (\d+)d(\d+)", content)
            if dice_match:
                n, sides = int(dice_match[1]), int(dice_match[2])
                rolls = [random.randint(1, sides) for _ in range(n)]
                content = f"{request.user.username} rolled {n}d{sides}: {rolls} (Total: {sum(rolls)})"

            is_dm = (request.user == gs.dm)
            Message.objects.create(
                game=gs,
                author=request.user,
                content=content,
                is_dm=is_dm
            )
        return redirect('game:session', session_id)