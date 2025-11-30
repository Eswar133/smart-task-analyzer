import json
from datetime import date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .scoring import score_tasks
from .serializers import validate_task


@csrf_exempt
def analyze_tasks(request):
    """
    POST /api/tasks/analyze/
    Expects:
    {
      "strategy": "smart_balance",
      "tasks": [ { ... }, ... ]
    }
    or simply:
    [ { ... }, ... ]
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    # Support both object form and raw list form
    if isinstance(data, dict):
        strategy = data.get("strategy", "smart_balance")
        tasks = data.get("tasks", [])
    else:
        strategy = "smart_balance"
        tasks = data

    if not isinstance(tasks, list):
        return JsonResponse({"error": "tasks must be a list"}, status=400)

    # Validate each task
    validation_errors = []
    for idx, t in enumerate(tasks):
        ok, errs = validate_task(t)
        if not ok:
            validation_errors.append({"index": idx, "errors": errs})

    if validation_errors:
        return JsonResponse(
            {"error": "Validation failed", "details": validation_errors},
            status=400,
        )

    scored = score_tasks(tasks, strategy=strategy)

    return JsonResponse({"tasks": scored}, status=200)


def suggest_tasks(request):
    """
    GET /api/tasks/suggest/
    For simplicity, expect a query param:
      ?strategy=smart_balance&tasks_json=<url-encoded JSON array>
    In a real app, you'd load tasks from the database instead.
    """
    strategy = request.GET.get("strategy", "smart_balance")
    tasks_json = request.GET.get("tasks_json")

    if not tasks_json:
        return JsonResponse(
            {"error": "tasks_json query param is required"},
            status=400,
        )

    try:
        tasks = json.loads(tasks_json)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid tasks_json"}, status=400)

    if not isinstance(tasks, list):
        return JsonResponse({"error": "tasks_json must be a JSON array"}, status=400)

    scored = score_tasks(tasks, strategy=strategy)
    top_three = scored[:3]

    suggestions = []
    for t in top_three:
        expl = t.get("explanations", {})
        text_expl = (
            f"Urgency: {expl.get('urgency', '')} | "
            f"Importance: {expl.get('importance', '')} | "
            f"Effort: {expl.get('effort', '')} | "
            f"Dependencies: {expl.get('dependencies', '')}"
        )

        suggestions.append(
            {
                "title": t.get("title"),
                "due_date": t.get("due_date"),
                "score": t.get("score"),
                "explanation": text_expl,
            }
        )

    return JsonResponse(
        {
            "today": date.today().isoformat(),
            "strategy": strategy,
            "suggestions": suggestions,
        }
    )
