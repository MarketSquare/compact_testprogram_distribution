# compact_testprogram_distribution

Zipapps are a sensible way to be able to distribute test programms with reasonable dependencies.

For executing robotframework in order to perform production facility / test floor automated tasks
the depency list becomes.:

 - The operating system
 - The non python drivers for the used equipment
 - python itself

## Zipapps with no native code

The only dependency is a python interpreter with a minimum version number, and the limitation 
that only zipapp compatible dependencies can be used.

For python versions 3.10 and 3.11 it is recomended to disable zipimport.zipimporter.invalidate_caches 
as it has a large performance inpact. Disabeling it, looses the feature to modify the zipapp during
runtime...

### Using pdm with pdm-packer

A python only zipapp without any native code.

``` bash
    $ cd examples\basic
    $ pdm install 
    $ pdm pack -m runway:main
    $ py zipapprobot.pyz .
```
At this point you are presented with robot output... 

### going limbo

lets reduce the size of the zipapp.:

``` bash
    $ cd examples\basic
    $ pdm install 
    $ pdm pack -m runway:main -c --compile
    $ py  zipapprobot.pyz .
```

This comes out at less then 2MB...

## Performance impact

The limbo zipapp is faster than the native version on my setup for this example.

``` powershell
    $sw = [Diagnostics.Stopwatch]::StartNew()
    pdm.exe run robot .
    $sw.Stop()
    $sw.Elapsed
    $sw = [Diagnostics.Stopwatch]::StartNew()
    py zipapprobot.pyz .
    $sw.Stop()
    $sw.Elapsed
```

## Zipapps with native code

This is not supported, and generally a bad idea. 

However this is technically possible by using importlib.util, and either https://github.com/SeaHOH/memimport or importlib.resources. Thus said, this is hacky and a bit of toppic. There is a example how this _can_ be achieved. In the example directory, but this is a proof that this can generally be achieved, but nothing more than that.

How well this can be donne heavily depends on the native code in question. Polars smoothly allows to load just the pyd file, and the rest from zipfile, numpy is hard...

### Open points for improvement

#### Windows

The given example clutters the tmp directory. This can be solved by using a 
bootstraping process to prepare the environment, and a seperate process to use
it, so when this child process terminated, all file handles to the environment
are closed and the directory can be removed.

#### Linux / MacOS / XXXBSD

The methods to handle native code have not been tried there.

# Interesting alternatives which provide improvements

 - memimport allows to import pyd files from within zipfiles. But needs to be loaded itself by other means.
 - pyoxidizer creates a true single file executable.
 - https://github.com/test-fullautomation/RobotFramework_AIO
 - shiv
 - pex 

# Infrastructure that is suitable to handle the environments

 - chocolatey
 - salt
 - ...
