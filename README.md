# compact_testprogram_distribution

Zipapps are a sensible way to be able to distribute test programms with reasonable dependencies.:

## Zipapps with no native code

The only dependency is a python interpreter with a minimum version number, and the limitation 
that only zipapp compatible dependencies can be used.

### Using pdm with pdm-packer

A python only zipapp without any native code.

.. sourcecode:: bash

    $ cd examples\basic
    $ pdm install 
    $ pdm pack -m robot:run_cli
    $ py zipapprobot.pyz .

At this point you are presented with robot output... 

### going limbo

lets reduce the size of the zipapp.:
.. sourcecode:: bash

    $  -m robot:run_cli -c --compile
    $ py  zipapprobot.pyz .

This comes out at less then 2MB...

## Zipapps with native code

.. sourcecode:: bash

    $ cd examples\numpy
    $ pdm install 
    $ pdm pack -m runway:main
    $ py zipapprobot.pyz .

At this point you are presented with robot output... 

The way this works is that the runway module goes trough the zipapp and extract
all elements which can not be loaded from a zipapp on the file system, and adds 
this directory to the sys.path.

This example is not optimised and copies more than actually necessary.
