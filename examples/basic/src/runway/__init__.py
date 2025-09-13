import robot
import zipimport
import importlib.resources
import runway.data


zipimport.zipimporter.invalidate_caches = lambda _: None


def main():
    robot.run_cli()


def main2():
    with importlib.resources.path(runway.data, "demo.robot") as path:
        robot.run(str(path))
