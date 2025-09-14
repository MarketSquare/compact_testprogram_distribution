import robot
import zipimport
import importlib.resources
import runway.data


zipimport.zipimporter.invalidate_caches = lambda _: None


def main():
    robot.run_cli()


def main_with_packaged_robot_file():
    """
    This function demonstrates how to run the robot file included in the package data.

    the packaging of the robot file is configured in setup.cfg
    """
    with importlib.resources.path(runway.data, "demo.robot") as path:
        robot.run(path)
