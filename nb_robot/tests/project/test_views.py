from utilities.testing import ViewTestCases, create_tags
from django.utils.text import slugify


from nb_robot.tests.custom import ModelViewTestCase
from nb_robot.models import Project


class ProjectViewTestCase(
    ModelViewTestCase,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = Project

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

        cls.form_data = {
            "name": "Project 4",
            "slug": "Project_4",
            "description": "A new project",
        }


        maxDiff = None
