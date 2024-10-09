from django.test import TestCase
from django.utils.text import slugify


from utilities.testing import ChangeLoggedFilterSetTests

from nb_robot.models import Project
from nb_robot.filtersets import ProjectFilterSet


class ProjectFilterTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = Project.objects.all()
    filterset = ProjectFilterSet

    @classmethod
    def setUpTestData(cls):

        projects = (
            Project(
                name="Project 1",
                slug=slugify("Project 1"),
                description="Something 1",
            ),
            Project(
                name="Project 2",
                slug=slugify("Project 2"),
                description="Something 2",
            ),
            Project(
                name="Project 3",
                slug=slugify("Project 3"),
                description="Something 3",
            ),
        )
        Project.objects.bulk_create(projects)

    def test_name_none(self):
        params = {"name": ["None"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 0)

    def test_name(self):
        params = {"name": ["Project 1", "Project 2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_names(self):
        params = {"name__icontains": ["Project"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

