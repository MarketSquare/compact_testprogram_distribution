from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': ["robot"], 'excludes': []}

base = 'console'

executables = [
    Executable('robot', base=base, target_name = 'robot_run')
]

setup(name='robot',
      version = '1.0',
      description = '',
      options = {'build_exe': build_options},
      executables = executables)
