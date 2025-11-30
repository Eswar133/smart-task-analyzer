from datetime import date, datetime


def parse_due_date(value):
    """
    Accepts either a date object or 'YYYY-MM-DD' string.
    Returns a date object or None if invalid.
    """
    if hasattr(value, 'year'):  
        return value

    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return None

    return None


def find_cycle_task_ids(tasks):
    """
    Detect circular dependencies using a simple DFS.
    Each task should have an 'id' and 'dependencies' (list of ids).
    Returns a set of ids of tasks that are in at least one cycle.
    """
    graph = {}
    for t in tasks:
        tid = t.get("id")
        deps = t.get("dependencies") or []
        if tid is not None:
            graph[tid] = deps

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {tid: WHITE for tid in graph.keys()}
    in_cycle = set()

    def dfs(node, stack):
        if color[node] == GRAY:
            # found a cycle – everything from first occurrence of node to end of stack
            if node in stack:
                idx = stack.index(node)
                in_cycle.update(stack[idx:])
            return

        if color[node] != WHITE:
            return

        color[node] = GRAY
        stack.append(node)

        for nxt in graph.get(node, []):
            if nxt in graph:
                dfs(nxt, stack)

        stack.pop()
        color[node] = BLACK

    for tid in graph.keys():
        if color[tid] == WHITE:
            dfs(tid, [])

    return in_cycle


def calculate_base_score(task):
    """
    Calculate the base score using urgency, importance, effort, and dependencies.
    Returns (score, explanations_dict).
    """
    today = date.today()
    score = 0
    explanations = {
        "urgency": "",
        "importance": "",
        "effort": "",
        "dependencies": "",
    }

    due = parse_due_date(task.get("due_date"))
    if due is None:
        explanations["urgency"] = "Due date missing/invalid: treated as low urgency (+0)"
    else:
        days = (due - today).days
        if days < 0:
            score += 100
            explanations["urgency"] = f"Overdue by {-days} day(s): +100"
        elif days <= 1:
            score += 70
            explanations["urgency"] = "Due within 1 day: +70"
        elif days <= 3:
            score += 50
            explanations["urgency"] = "Due within 3 days: +50"
        elif days <= 7:
            score += 30
            explanations["urgency"] = "Due within a week: +30"
        else:
            score += 10
            explanations["urgency"] = "Due later than a week: +10"

    try:
        importance = int(task.get("importance", 5))
    except (TypeError, ValueError):
        importance = 5

    score += importance * 5
    explanations["importance"] = f"Importance {importance}/10: +{importance * 5}"

 
    try:
        hours = float(task.get("estimated_hours", 1))
    except (TypeError, ValueError):
        hours = 1

    if hours < 1:
        score += 15
        explanations["effort"] = "Very small task (<1 hour): +15"
    elif hours < 2:
        score += 10
        explanations["effort"] = "Small task (<2 hours): +10"
    elif hours <= 4:
        score += 5
        explanations["effort"] = "Medium (2–4 hours): +5"
    else:
        explanations["effort"] = "Large task (>4 hours): +0"

    deps = task.get("dependencies") or []
    if deps:
        bonus = min(len(deps) * 5, 30)
        score += bonus
        explanations["dependencies"] = f"{len(deps)} dependency(ies): +{bonus}"
    else:
        explanations["dependencies"] = "No dependencies: +0"

    return score, explanations


def apply_strategy(score, task, strategy):

    strategy = strategy or "smart_balance"

    try:
        importance = int(task.get("importance", 5))
    except (TypeError, ValueError):
        importance = 5

    try:
        hours = float(task.get("estimated_hours", 1))
    except (TypeError, ValueError):
        hours = 1

    due = parse_due_date(task.get("due_date"))
    days = 9999
    if due is not None:
        days = (due - date.today()).days

    if strategy == "fastest_wins":
        # Reward super tasks (quick)
        if hours <= 1:
            score += 30
        elif hours <= 2:
            score += 20

    elif strategy == "high_impact":
        # Rewarding for importance 
        score += importance * 2

    elif strategy == "deadline_driven":
     
        if days <= 1:
            score += 40
        elif days <= 3:
            score += 25
        elif days <= 7:
            score += 10

    elif strategy == "smart_balance":
     
        if importance >= 8:
            score += 10
        if hours <= 2:
            score += 10
        if days <= 3:
            score += 10

    return score


def score_tasks(tasks, strategy="smart_balance"):
    # id for each task
    for i, t in enumerate(tasks):
        if "id" not in t:
            t["id"] = i + 1

    cycle_ids = find_cycle_task_ids(tasks)

    scored = []
    for t in tasks:
        base_score, explanations = calculate_base_score(t)
        final_score = apply_strategy(base_score, t, strategy)

        in_cycle = t["id"] in cycle_ids
        if in_cycle:
            final_score -= 20
            explanations["dependencies"] += " | In circular dependency: -20"

        new_task = dict(t)  # copy
        new_task["score"] = round(final_score, 2)
        new_task["explanations"] = explanations
        new_task["in_cycle"] = in_cycle
        scored.append(new_task)

    # score sorting in desc order 
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored
