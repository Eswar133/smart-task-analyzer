from django.test import TestCase
from .scoring import score_tasks


class ScoringTests(TestCase):
    def test_overdue_task_has_higher_score(self):
        """Overdue tasks should get a big urgency boost."""
        tasks = [
            {
                "id": 1,
                "title": "Old Task",
                "due_date": "1990-01-01",
                "importance": 5,
                "estimated_hours": 2,
                "dependencies": [],
            },
            {
                "id": 2,
                "title": "Future Task",
                "due_date": "2099-01-01",
                "importance": 5,
                "estimated_hours": 2,
                "dependencies": [],
            },
        ]

        scored = score_tasks(tasks, strategy="smart_balance")
        self.assertEqual(scored[0]["title"], "Old Task")

    def test_fastest_wins_prefers_quick_task(self):
        """Fastest Wins strategy should put smaller tasks first."""
        tasks = [
            {
                "id": 1,
                "title": "Long Task",
                "due_date": "2099-01-01",
                "importance": 7,
                "estimated_hours": 6,
                "dependencies": [],
            },
            {
                "id": 2,
                "title": "Quick Task",
                "due_date": "2099-01-01",
                "importance": 7,
                "estimated_hours": 0.5,
                "dependencies": [],
            },
        ]

        scored = score_tasks(tasks, strategy="fastest_wins")
        self.assertEqual(scored[0]["title"], "Quick Task")

    def test_circular_dependency_is_penalized(self):
        """Tasks in a dependency cycle should get an in_cycle flag and lower score."""
        tasks = [
            {
                "id": 1,
                "title": "Task A",
                "due_date": "2099-01-01",
                "importance": 5,
                "estimated_hours": 2,
                "dependencies": [2],
            },
            {
                "id": 2,
                "title": "Task B",
                "due_date": "2099-01-01",
                "importance": 5,
                "estimated_hours": 2,
                "dependencies": [1],
            },
            {
                "id": 3,
                "title": "Independent Task",
                "due_date": "2099-01-01",
                "importance": 5,
                "estimated_hours": 2,
                "dependencies": [],
            },
        ]

        scored = score_tasks(tasks, strategy="smart_balance")

        task_a = next(t for t in scored if t["id"] == 1)
        independent = next(t for t in scored if t["id"] == 3)

        self.assertTrue(task_a["in_cycle"])
        self.assertFalse(independent["in_cycle"])
        self.assertGreater(independent["score"], task_a["score"])
