from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200),
    due_date=models.DateField(),
    importance = models.IntegerField(default=5) #1-5
    estimated_hours = models.FloatField(default=1),
    dependencies = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return self.title 
    

class Ticket(models.Model):
    STRATEGY_CHOICES = [
        ("smart_balance", "Smart Balance"),
        ("high_impact", "High Impact"),
        ("fastest_wins", "Fastest Wins"),
        ("deadline_driven", "Deadline Driven"),
    ]

    strategy = models.CharField(max_length=50, choices=STRATEGY_CHOICES)
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    importance = models.IntegerField()
    estimated_hours = models.FloatField()
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.strategy})"
