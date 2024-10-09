import io
import os
import robot
import logging
import json

from robot.api import ExecutionResult
from robot import rebot

from netbox.jobs import JobRunner


from . import robot_listener
class RobotJob(JobRunner):
    
    """
    Robot Framework execution job.

    A wrapper for calling robot.run.
    """

    class Meta:
        # An explicit job name is not set because it doesn't make sense in this context. Currently, there's no scenario
        # where jobs other than this one are used. Therefore, it is hidden, resulting in a cleaner job table overview.
        name = ''

    def run_robot(self,  *args, **kwargs):
        """
        Core script execution task. We capture this within a method to allow for conditionally wrapping it with the
        event_tracking context manager (which is bypassed if commit == False).

        Args:
            request: The WSGI request associated with this execution (if any)
            data: A dictionary of data to be passed to the script upon execution
            commit: Passed through to Script.run()
        """

        project = kwargs.get('project')
        logger = logging.getLogger(f"robot.project.{project.name}")
        logger.info(f"Running robot")
        test_suite = project.resources.filter(resource_type='TestSuite').first()
        report = None
        try:
            output = io.StringIO()
            listener = robot_listener.nb_robot(project=project)
            robot_data = robot.run(
                test_suite.full_path,
                listener=listener,
                outputdir=project.project_path,
                stdout=output,
                output=f"{project.project_path}/output.xml",
                report=None,
                log=None,
                )
            
            report = listener.report
        except Exception as e:
            logger.error(f"Error running robot: {e}")
        result = output.getvalue()
        output.close()
        statistics = {
            "total": 0,
            "passed": 0,
            "failed": 0,
        }
        if os.path.isfile(f"{project.project_path}/output.xml"):
            statistics_obj = ExecutionResult(f"{project.project_path}/output.xml").statistics.total
            statistics["total"] = statistics_obj.total
            statistics["passed"] = statistics_obj.passed
            statistics["failed"] = statistics_obj.failed
            with open(f"{project.project_path}/output.xml", 'r') as f:
                xml_output = f.read()
            rebot_output = io.StringIO()
            rebot(f"{project.project_path}/output.xml",output=f"{project.project_path}/output.json", stdout=rebot_output)
            rebot_output.close()
            with open(f"{project.project_path}/output.json", 'r') as f:
                json_output = json.load(f)
            os.remove(f"{project.project_path}/output.xml")
            os.remove(f"{project.project_path}/output.json")
        else:
            xml_output = ""
            json_output = ""
        data = {
            "result": result,
            "xml": xml_output,
            "total": statistics["total"],
            "passed": statistics["passed"],
            "failed": statistics["failed"],
            "json": json_output
        }
        self.job.data = data

    def run(self, *args, **kwargs):
        """
        Run the Robot Framework script.

        Args:
            data: A dictionary of data to be passed to the script upon execution
            request: The WSGI request associated with this execution (if any)
            commit: Passed through to Script.run()
        """
        self.run_robot(*args, **kwargs)
       
