# compact_testprogram_distribution

Zipapps are a sensible way to be able to distribute test programms with reasonable dependencies.:

## Zipapps with no native code

The only dependency is a python interpreter with a minimum version number, and the limitation 
that only zipapp compatible dependencies can be used.

### Using pdm

A python only zipapp without any native code.

Create a pyproject.toml with this content

.. sourcecode:: bash

    [project]
    name = "zipapprobot"
    version = "0.0.1"
    description = ""
    authors = [{name = "you", email = "you@example.com"}]
    dependencies = ["robotframework @ git+https://github.com/franzhaas/robotframework.git@zipapp"]
    requires-python = "~=3.11.0"
    license = {text = "Apache License"}

the dependencies entry is the place to list the wheels you want to have inside your zipapp

.. sourcecode:: bash

    $ pdm install 
    $ pdm pack -m robot:run_cli
    $ py zipapprobot.pyz .

At this point you are presented with robot output... 

### going limbo

lets reduce the size of the zipapp.:
.. sourcecode:: bash

    $  -m robot:run_cli -c --compile
    $ py  -3.11 zipapprobot.pyz .

This comes out at less then 2MB...

## Zipapps with native code

Some native code libraries can be used with zipapps with these additional limitations
  - only one platform and one interpreter version is supported
  - some bootstrap code needs to be run before anything gets imported.
  
Imeediate goals.:
- cffi based extension working
- numpy
- pandas
- cython based extension
- polars
- scipy

# known interesting competitors

- pyoxidizer
- shiv
- pex

please share your experience

### with pdm

### Using pdm

A python only zipapp without any native code.

Create a pyproject.toml with this content

.. sourcecode:: bash

    [project]
    name = "zipapprobot"
    version = "0.0.1"
    description = ""
    authors = [{name = "you", email = "you@example.com"}]
    dependencies = ["robotframework @ git+https://github.com/franzhaas/robotframework.git@zipapp", "numpy", "pandas"]
    requires-python = "~=3.11.0"
    license = {text = "Apache License"}

Create a pyproject.toml with this content


the dependencies entry is the place to list the wheels you want to have inside your zipapp

.. sourcecode:: bash

    $ pdm install 
    $ pdm pack -m robot:run_cli
    $ py -3.11 zipapprobot.pyz .
