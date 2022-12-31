from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from tasks.models import Task


class TaskAPITestCase(APITestCase):
    def create_task(self):
        sample_task = {'title': 'Task 1', 'desc': 'desc 1'}
        response = self.client.post(reverse('tasks'), sample_task)
        return response

    def authenticate(self):
        self.client.post(reverse('register'), {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'testPassword',
        })
        response = self.client.post(reverse('login'), {
            'email': 'test@test.com',
            'password': 'testPassword'
        })
        self.client.credentials(HTTP_AUTHORIZATION=f"BEARER {response.data['token']}")


class TestListCreateTasks(TaskAPITestCase):

    def test_should_not_create_task_with_no_auth(self):
        sample_task = {'title': 'Task 1', 'desc': 'desc 1'}
        response = self.client.post(reverse('tasks'), sample_task)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_create_task_with_auth(self):
        self.authenticate()
        previous_tasks = Task.objects.all().count()
        response = self.create_task()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.all().count(), previous_tasks + 1)
        self.assertEqual(response.data['title'], 'Task 1')
        self.assertEqual(response.data['desc'], 'desc 1')

    def test_retrieves_all_tasks(self):
        self.authenticate()

        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.create_task()
        self.assertEqual(Task.objects.all().count(), 1)


class TestTaskDetailAPITasks(TaskAPITestCase):
    def test_retrieves_one_task(self):
        self.authenticate()
        response = self.create_task()
        res = self.client.get(reverse('task', kwargs={'id': 1}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=1)
        self.assertEqual(task.title, response.data['title'])

    def test_updates_one_task(self):
        self.authenticate()
        response = self.create_task()
        res = self.client.patch(reverse('task', kwargs={'id': 1}),
                                {"title": "new title",
                                 "desc": "new desc",
                                 "is_completed": True})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        updated_task = Task.objects.get(id=1)

        self.assertEqual(updated_task.title, "new title")
        self.assertEqual(updated_task.desc, "new desc")
        self.assertEqual(updated_task.is_completed, True)

    def test_deletes_one_task(self):
        self.authenticate()
        self.create_task()
        prev_db_count = Task.objects.all().count()

        self.assertEqual(prev_db_count, 1)

        response = self.client.delete(reverse('task', kwargs={'id': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(prev_db_count, 0)
