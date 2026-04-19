from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

from .models import GameRecord

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
        "attempts": 6,
        "time_limit": 60,
        "grid_size": 4,
    }
    return render(request, "memory_game/game.html", context)


@login_required
def play_hard(request):
    context = {
        "level_name": "AVANZADO",
        "attempts": 2,
        "time_limit": 60,
        "grid_size": 4,
    }
    return render(request, "memory_game/game.html", context)


@login_required
def save_result(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Método no permitido")

    level = request.POST.get("level", "").lower()
    win = request.POST.get("win") == "true"
    duration = request.POST.get("duration")

    try:
        duration_seconds = int(duration)
    except (TypeError, ValueError):
        duration_seconds = 0

    valid_levels = dict(GameRecord.LEVEL_CHOICES).keys()
    if level not in valid_levels:
        return HttpResponseBadRequest("Nivel inválido")

    GameRecord.objects.create(
        user=request.user,
        level=level,
        win=win,
        duration_seconds=duration_seconds,
    )

    return JsonResponse({"status": "ok"})


@login_required
def profile(request):
    records = request.user.game_records.order_by("-created_at")
    total_games = records.count()
    total_wins = records.filter(win=True).count()
    total_losses = total_games - total_wins
    average_time = records.aggregate(avg=Avg("duration_seconds"))["avg"] or 0

    most_played = (
        records.values("level")
        .annotate(count=Count("level"))
        .order_by("-count")
        .first()
    )
    favorite_level = (
        dict(GameRecord.LEVEL_CHOICES).get(most_played["level"]) if most_played else "Ninguno"
    )

    level_counts = {
        value: records.filter(level=value).count()
        for value, label in GameRecord.LEVEL_CHOICES
    }

    context = {
        "total_games": total_games,
        "total_wins": total_wins,
        "total_losses": total_losses,
        "average_time": round(average_time, 1),
        "favorite_level": favorite_level,
        "records": records,
        "level_counts": level_counts,
    }
    return render(request, "memory_game/profile.html", context)