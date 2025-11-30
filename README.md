
---

# 📘 **Smart Task Analyzer — AI-Powered Task Prioritization System**

An intelligent task-prioritization engine designed for **Singularium Internship Assignment 2025**.
This project helps users submit tasks, analyze them using multiple prioritization strategies, save results as "tickets," and view previously saved tickets grouped by strategy.

---

## 🚀 **Features**

### ✅ 1. Task Analyzer (Frontend)

* Users enter tasks with:

  * Title
  * Due Date
  * Importance
  * Estimated Hours
  * Dependencies
* Tasks are scored using AI-inspired logic:

  * Urgency
  * Importance
  * Effort
  * Dependency complexity
* Supports **4 prioritization strategies**:

  * **Smart Balance**
  * **High Impact**
  * **Fastest Wins**
  * **Deadline Driven**

---

### ✅ 2. Backend (Django + SQLite)

* `/api/tasks/analyze/` → Scores tasks and returns sorted results
* Automatically saves each analyzed task as a **Ticket**
* `/tickets/?strategy=high_impact` → Shows saved tickets filtered by strategy
* `/api/tasks/suggest/` → Returns top 3 recommended tasks along with explanations

---

### ✅ 3. Persistence Layer (SQLite)

Every analyzed task is stored as:

```plaintext
Ticket(strategy, title, due_date, importance, estimated_hours, score, created_at)
```

Tickets appear under tabs:

```
Smart Balance | High Impact | Fastest Wins | Deadline Driven
```

Clicking each tab shows only those strategy-specific tickets.

---

## 🛠️ **Tech Stack**

### **Frontend**

* HTML5 + CSS3
* Vanilla JavaScript
* Responsive design with modern UI

### **Backend**

* Django 5.x
* SQLite database
* REST responses via JsonResponse

### **Additional Modules**

* Custom scoring engine (`scoring.py`)
* Input validation (`serializers.py`)
* Ticket model (`models.py`)

---

## 📁 **Project Structure**

```
backend/
│
├── tasks/
│   ├── models.py
│   ├── views.py
│   ├── scoring.py
│   ├── serializers.py
│   ├── urls.py
│   └── templates/
│       ├── index.html
│       └── tickets.html
│
├── backend/
│   ├── settings.py
│   ├── urls.py
│
└── manage.py

static/
└── styles.css
```

---

## ▶️ **How to Run the Project**

### **1️⃣ Create Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

---

### **2️⃣ Install Dependencies**

```bash
pip install django
```

---

### **3️⃣ Run Migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### **4️⃣ Start Development Server**

```bash
python manage.py runserver
```

Your app will run at:

👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** — Task Analyzer Frontend
👉 **[http://127.0.0.1:8000/tickets/](http://127.0.0.1:8000/tickets/)** — Saved tickets dashboard

---

## 🔌 **API Endpoints**

### **POST /api/tasks/analyze/**

Request (JSON):

```json
{
  "strategy": "high_impact",
  "tasks": [
    {
      "title": "Fix login bug",
      "due_date": "2025-12-02",
      "importance": 9,
      "estimated_hours": 2,
      "dependencies": []
    }
  ]
}
```

Response:

```json
{
  "tasks": [
    {
      "title": "Fix login bug",
      "score": 92,
      "explanations": {
        "urgency": "...",
        "importance": "...",
        "effort": "...",
        "dependencies": "..."
      }
    }
  ]
}
```

---

### **GET /tickets/?strategy=high_impact**

Displays saved tickets filtered by strategy.

---

### **GET /api/tasks/suggest/?strategy=smart_balance&tasks_json=<json>**

Returns the **top 3 suggestions** with textual explanations.

---

## 💾 **Database Model**

```python
class Ticket(models.Model):
    strategy = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    importance = models.IntegerField()
    estimated_hours = models.FloatField()
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## 🧠 **Scoring Logic Overview**

Every task receives a numerical score combined from:

### **1. Urgency Score**

* Sooner deadlines = higher score
* Overdue tasks = very high urgency

### **2. Importance Score**

* Direct weighting

### **3. Effort Score**

* Low hours = bonus
* High hours = penalty

### **4. Dependency Score**

* More dependencies = lower score
* Circular dependencies → heavy penalty

---

## 🎨 **UI Features**

* Clean, modern design
* Tabs for switching between strategies
* Task cards displaying:

  * Title
  * Score
  * Due date
* Button to return to **Add Tasks** form

---

## 🧪 **Testing**

You can test using the recommended JSON samples from the README or by entering your own tasks.

---

## 📌 **Future Improvements**

* User authentication (personal ticket dashboards)
* Drag-and-drop task ordering
* Export tasks/tickets as PDF
* Integration with Jira / Notion / Trello
* AI auto-task generator

---

## 👤 **Author**

**Eswar Reddy**


---
