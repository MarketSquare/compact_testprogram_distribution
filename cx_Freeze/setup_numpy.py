from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': ["robot", "numpy", "pandas"], 'excludes': []}

base = 'console'

executables = [
    Executable('robot_starter.py', base=base, target_name = 'robot_run_numpy')
]

setup(name='robot',
      version = '1.0',
      description = '',
      options = {'build_exe': build_options},
      executables = executables)
