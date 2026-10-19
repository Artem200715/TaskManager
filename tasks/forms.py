from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        label='Срок выполнения', required=False,
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}),
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'completed']
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}
