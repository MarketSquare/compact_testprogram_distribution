# Compact testprogram distribution

Zipapps are a sensible way to be able to distribute test programs with reasonable dependencies.

For executing Robot Framework in order to perform production facility / test floor automated tasks
the dependency list becomes.:

 - The operating system
 - The non python drivers for the used equipment
 - python itself

## Zipapps with no native code

The only dependency is a python interpreter with a minimum version number, and the limitation 
that only zipapp compatible dependencies can be used.

Python versions 3.10 and 3.11 are not recommended as a performance issue with zipimport.zipimporter.invalidate_caches 
causes a large performance impact. Python 3.12 and 3.13 do not have this problem.

### Using pdm with pdm-packer

A python only zipapp without any native code.

``` bash
    $ cd examples\basic
    $ pdm install 
    $ pdm pack -m runway:main
    $ py zipapprobot.pyz .
```
At this point you are presented with robot output... 

### Minimal zipapp build (a.k.a. Limbo Mode)

let’s reduce the size of the zipapp.:

``` bash
    $ cd examples\basic
    $ pdm install 
    $ pdm pack -m runway:main -c --compile
    $ py  zipapprobot.pyz .
```

This results in a zipapp of less than 2MB in size, making it highly portable.

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

However this is technically possible by using importlib.util, and either https://github.com/SeaHOH/memimport or importlib.resources. Thus said, this is hacky
and a bit off topic. There is an example of how this _can_ be achieved. In the example directory, it is a proof that this can generally be achieved, but
nothing more than that.

The feasibility of this approach heavily depends on the specific native code. For instance, polars works relatively well, whereas numpy presents significant challenges.

## cx_freeze

cx_freeze can create many targets, the one I personally find most interesting is bdist_appimage (currently linux only). The resulting file with 34MBytes is reasonably
close to the size of a python installer (28MBytes), and is a self contained, single file executable. Being dependent only of the operating system and drivers.

cx_freeze does use script entry points.

Robot Framework does come with a script, which is documented [here](https://robot-framework.readthedocs.io/en/latest/autodoc/robot.html#module-robot.run).

What is not documented (and as far as I understand from this [discussion](https://github.com/robotframework/robotframework/issues/5384) will not be, this
[pull request](https://github.com/robotframework/robotframework/pull/5390) was provided to remove pythonpathsetter), is that this script needs to live in 
the source tree, and can not use an installed Robot Framework, like in the zipapp/frozenapp/etc use case.

### background
It is possible to use Robot Framework straight from the source tree, without installation or configuring PYTHONPATH. This feature is not documented in the 
end user documentation, and not explained in the CONTRIBUTING.rst.

This is implemented using the `pythonpathsetter` module which can be loaded by `import pythonpathsetter` when the Robot Framework is run from the script,
additionally by `import robot.pythonpathsetter` when the script runs inside an environment where Robot Framework was installed into, and only using 
`import robot.pythonpathsetter`. This module changes the the `sys.path` at runtime, which can cause severe confusion when debugging dependency issues.

These are the symptoms to look out for.:
 1 is that Robot Framework fails, as pythonpathsetter can not be imported. 
 2 you can use ```import robot; robot.run()``` when debugging from a REPL.

 In total at the time of writing there are 34 instances of ```sys.path``` and 89 ```__file__```in the source, all of them bring the risk of causing issues 
 with zipapp/frozenapp usage. When I went over the source the first time, I missed how the ```pythonpathsetter``` can cause issues.

### solutions
#### make sure pythonpathsetter exits
Install a  ```pythonpathsetter.py``` into your environment. Be aware future releases of Robot Framework will call a ```pythonpathsetter.set_pythonpath``` fucntion.
This function is in the source tree where you would expect ```robot.pythonpathsetter.set_pythonpath```. It doesn’t need to do anything but if it is missing the code 
will not work. This change is introduced in response to linter messages.

#### do not use Robot Framework distributed scripts
Provide your own start script.

#### [merge](https://github.com/robotframework/robotframework/pull/5390) (would need to come from upstream)
Apart of improving the situation for frozenapp/zipapp use cases this brings these advantages.:

 1) Reduction of total complexity (cyclomatic complexity goes from 18329 to 18307 a delta of 22, number of lines from 58033 to 57967, a delta of 134)
 2) The ```pythonpathsetter``` feature is not advertised. It is likely that its most common use is in Robot Framework quality control.
    - if that would make testing easier/faster for multiple python installations that might be worth the risk.
    - solutions like [uvx](https://docs.astral.sh/uv/) ```uvx --python 3.14 --from . --reinstall robot``` are available, taking care of warehousing the python versions.
    - Virutal environments are cheap, get two.
    - Have you heard of ziapps? You can have the Robot Framework version you like installed into a single file, and then use the python of choice to execute it!
    - Have you heard of frozen apps? You can have Robot Framework with python frozen together ahead of time!
 3) The fact that Robot Framework "script edition" ignores installed Robot Framework but requires to be part of the Robot Framework source tree
    are two unusual properties, which can cause confusion.
      
 It is hard to get this point across, but the "unpack into a directory" distribution method is very much outdated by now.

#### do not modify the ```sys.path``` (would need to come from upstream)
Placing this code into the src directory, next to the robot directory of the source distribution. Using this code allows the robot code base to reduce 
the modifications of the ```sys.path```, while keeping the feature to use Robot Framework straight from the source directory.

```python
import pathlib

if __name__ == "__main__":
    try:
        source = (pathlib.Path(__file__).parent / "robot" / "run.py")
        with source.open() as run:
            source_code = run.read()
    except Exception as e:
        print(f"""run_rf is a tool allowing you to start Robot Framework from a source tree without installing anything. Exception {e} occurred.
              
              This script should not be used outside of Robot Framework development, and is not part of Robot Framework itself.""")
    exec(source_code)
```

### conclusion
There are alternatives available.

 - docker (way more heavy weight, user rights need to be managed)
 - astral [uv](https://docs.astral.sh/uv/) ```uvx --from robotframework==7.2.2 --with numpy==2.2.6 robot``` (not a single file, needs access to wheels...)
 - ...

I see value in frozen/zipapps and encourage everyone who is interested to tinker with them in an effort to learn. They are often faster than regular
environments, easier to deploy and manage. However I would not recommend using them in a productive environment.
