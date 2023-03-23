# compact_testprogram_distribution

Zipapps are a sensible way to be able to distribute test programms with reasonable dependencies.:

## Zipapps with no native code

The only dependency is a python interpreter with a minimum version number, and the limitation 
that only zipapp compatible dependencies can be used.


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
