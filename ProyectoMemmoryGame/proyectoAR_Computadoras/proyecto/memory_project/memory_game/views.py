from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def select_level(request):
    return render(request, "memory_game/select_level.html")


@login_required
def play_basic(request):
    context = {
        "level_name": "BÁSICO",
        "attempts": 6,
        "time_limit": 60,
        "grid_size": 4,
    }
    return render(request, "memory_game/game.html", context)


@login_required
def play_medium(request):
    context = {
        "level_name": "MEDIO",
        "attempts": 5,
        "time_limit": 90,
        "grid_size": 5,
    }
    return render(request, "memory_game/game.html", context)


@login_required
def play_hard(request):
    context = {
        "level_name": "AVANZADO",
        "attempts": 4,
        "time_limit": 120,
        "grid_size": 6,
    }
    return render(request, "memory_game/game.html", context)