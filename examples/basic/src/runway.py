import robot
import zipimport


zipimport.zipimporter.invalidate_caches = lambda _: None


def main():
    robot.run_cli()
