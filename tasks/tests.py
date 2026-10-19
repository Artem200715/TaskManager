from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Task

class TaskTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.alice = User.objects.create_user('alice', password='Strong-pass-123')
        self.bob = User.objects.create_user('bob', password='Strong-pass-123')
        self.task = Task.objects.create(owner=self.alice, title='Личная задача')
        self.other = Task.objects.create(owner=self.bob, title='Чужая задача')

    def test_login_required(self):
        for path in [reverse('tasks:task_list'), reverse('tasks:task_new'),
                     reverse('tasks:task_edit', args=[self.task.pk]),
                     reverse('tasks:task_delete', args=[self.task.pk]),
                     reverse('tasks:task_toggle', args=[self.task.pk])]:
            self.assertEqual(self.client.get(path).status_code, 302)

    def test_only_my_tasks(self):
        self.client.force_login(self.alice)
        response = self.client.get(reverse('tasks:task_list'))
        self.assertContains(response, 'Личная задача')
        self.assertNotContains(response, 'Чужая задача')

    def test_create_assigns_owner(self):
        self.client.force_login(self.alice)
        response = self.client.post(reverse('tasks:task_new'), {
            'title': 'Новая', 'description': '', 'due_date': '', 'priority': 'high',
            'owner': self.bob.pk})
        self.assertRedirects(response, reverse('tasks:task_list'))
        self.assertEqual(Task.objects.get(title='Новая').owner, self.alice)

    def test_invalid_date_is_form_error(self):
        self.client.force_login(self.alice)
        response = self.client.post(reverse('tasks:task_new'),
            {'title': 'Проверка', 'priority': 'normal', 'due_date': 'bad-date'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(title='Проверка').exists())
        self.assertTrue(response.context['form'].errors)

    def test_cannot_edit_other_task(self):
        self.client.force_login(self.alice)
        url = reverse('tasks:task_edit', args=[self.other.pk])
        self.assertEqual(self.client.get(url).status_code, 404)
        self.assertEqual(self.client.post(url, {'title': 'Взлом', 'priority': 'low'}).status_code, 404)
        self.other.refresh_from_db()
        self.assertEqual(self.other.title, 'Чужая задача')

    def test_cannot_delete_other_task(self):
        self.client.force_login(self.alice)
        url = reverse('tasks:task_delete', args=[self.other.pk])
        self.assertEqual(self.client.post(url).status_code, 404)
        self.assertTrue(Task.objects.filter(pk=self.other.pk).exists())

    def test_missing_id_returns_404(self):
        self.client.force_login(self.alice)
        for name in ['task_edit', 'task_delete', 'task_toggle']:
            url = reverse('tasks:' + name, args=[999999])
            self.assertEqual(self.client.get(url).status_code, 404)

    def test_toggle_post_only(self):
        self.client.force_login(self.alice)
        url = reverse('tasks:task_toggle', args=[self.task.pk])
        self.assertEqual(self.client.get(url).status_code, 405)
        self.client.post(url)
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)
        self.client.post(url)
        self.task.refresh_from_db()
        self.assertFalse(self.task.completed)

    def test_delete_get_only_confirms(self):
        self.client.force_login(self.alice)
        url = reverse('tasks:task_delete', args=[self.task.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())
        self.client.post(url)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_logout_post_only(self):
        self.client.force_login(self.alice)
        url = reverse('users:logout')
        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertTrue(self.client.session.get('_auth_user_id'))
        self.client.post(url)
        self.assertFalse(self.client.session.get('_auth_user_id'))

    def test_order_and_overdue(self):
        self.client.force_login(self.alice)
        Task.objects.create(owner=self.alice, title='Высокий', priority='high',
                            due_date=timezone.now() - timedelta(days=1))
        response = self.client.get(reverse('tasks:task_list'))
        self.assertContains(response, 'Просрочена')
        self.assertEqual(response.context['tasks'][0].title, 'Высокий')
