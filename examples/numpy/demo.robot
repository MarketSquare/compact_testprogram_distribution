*** Settings ***
Documentation     A test suite 

*** Test Cases ***
demo    
    ${a}=                    Evaluate     numpy.array([1,2,3,4])     numpy
    Should be equal as Numbers      4      ${a[-1]}
