def validate_task(task):
    errors = []
    if not task.get("title"):
        errors.append("title is required")
    if not task.get("due_date"):
        errors.append("due_date is required (YYYY-MM-DD)")
    if "estimated_hours" not in task:
        errors.append("estimated_hours required")
    if "importance" not in task:
        errors.append("importance is required (1-10)")
    return len(errors) == 0, errors 
