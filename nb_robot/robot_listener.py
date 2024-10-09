import robot
import json

from enum import auto

# Robot imports
from robot.libraries.BuiltIn import BuiltIn
from robot.model.tags import Tags 
from robot.running.model import TestCase
from robot.running.model import Argument
from .robot_utils import is_same_keyword

# NetBox imports
from utilities.querydict import dict_to_querydict

from .version import __version__

class nb_robot:
    
    ROBOT_LIBRARY_DOC_FORMAT = "reST"
    ROBOT_LIBRARY_VERSION = __version__
    ROBOT_LISTENER_API_VERSION = 3
    ROBOT_LIBRARY_SCOPE = "TEST SUITE"

    def __init__(self, project=None):
        self.ROBOT_LIBRARY_LISTENER = self
        self.report = []
        if project is not None:
            self.project = project
            self.project_vars = project.variables.all()

    def start_suite(self, suite, results):
        print(f"Starting suite: {suite.name}")
        for var in self.project_vars:
            if var.type == "queryset":
                if var.value != "":            
                    qs = dict_to_querydict(json.loads(var.value))
                    model_class = var.related_object_type.model_class()
                    BuiltIn().set_suite_variable(f"${{{var.name}}}", model_class.objects.filter(**qs.dict()))
                else:
                    model_class = var.related_object_type.model_class()
                    BuiltIn().set_suite_variable(f"${{{var.name}}}", model_class.objects.all())
            elif var.type == "savedfilter":
                saved_filter = var.value
                qs = dict_to_querydict(saved_filter.parameters)
                model_class = var.related_object_type.model_class()
                BuiltIn().set_suite_variable(f"${{{var.name}}}", model_class.objects.filter(**qs.dict()))
            else:
                BuiltIn().set_suite_variable(f"${{{var.name}}}", var.value)
        if suite.tests[0].template is not None:
            self.template_test = suite.tests[0]
            self.template_keyword = self._get_template_keyword(suite)

            arg = suite.tests[0].body[0].args[0]
            arg_values = BuiltIn().get_variable_value(arg)
            suite.tests.clear()
            test_list = self._get_test_list(arg_values)
            suite.tests.extend(test_list)
            
    def _get_template_keyword(self, suite):
        template = self.template_test.template
        if template:
            for keyword in suite.resource.keywords:
                if is_same_keyword(keyword.name, template):
                    return keyword
        raise AttributeError('No "Test Template" keyword found for first test case.')

    def _get_test_list(self, arg_values):
        test_list = []
        for arg_value in arg_values:
            print(f"Creating test for {arg_value}")
            self.test = TestCase(
                name = f'<a href="{arg_value.get_absolute_url()}">{arg_value.name}</a> -- {self.template_test.name}',
                doc=self.template_test.doc,
                tags=self.template_test.tags,
                template=self.template_test.template,
                lineno=self.template_test.lineno,
                timeout=self.template_test.timeout,
            )
            self.test.parent = self.template_test.parent
            self._replace_test_case_keywords(arg_value)
            test_list.append(self.test)
        return test_list
    
    def _replace_test_case_keywords(self, arg_value):
        self.test.setup = self.template_test.setup
        self.test.teardown = self.template_test.teardown
        self.test.body.create_keyword(
            name=self.template_keyword.name,
            args=self._get_template_arguments(arg_value),
            lineno=self.template_keyword.lineno,
        )
    
    def _get_template_arguments(self, arg_value):
        keyword_arguments = []
        for arg in self.template_keyword.args:
            arg_name = f"${{{arg.name}}}"
            keyword_arguments.append(Argument(arg.name, arg_value))
        return keyword_arguments
