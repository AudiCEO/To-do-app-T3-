from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "notes", "due_date"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "What needs to be done?"}),
            "notes": forms.Textarea(attrs={"rows": 2, "placeholder": "Notes (optional)"}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }
