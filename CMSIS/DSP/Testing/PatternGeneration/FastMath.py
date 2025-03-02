import os.path
import numpy as np
import itertools
import Tools
import math

import numpy as np

def q31accuracy(x):
     return(np.round(1.0*x * (1<<31)))

def q15accuracy(x):
     return(np.round(1.0*x * (1<<15)))

def q7accuracy(x):
     return(np.round(1.0*x * (1<<7)))

def Q31toF32(x):
     return(1.0*x / 2**31)

def Q15toF32(x):
     return(1.0*x / 2**15)

def Q7toF32(x):
     return(1.0*x / 2**7)

# Those patterns are used for tests and benchmarks.
# For tests, there is the need to add tests for saturation

# For benchmarks
NBSAMPLES=256

def cartesian(*somelists):
   r=[]
   for element in itertools.product(*somelists):
       r.append(element)
   return(r)

# Fixed point division should not be called with a denominator of zero.
# But if it is, it should return a saturated result.
def divide(f,r):
    e = 0
    a,b=r

    if f == Tools.Q31:
        e = 1.0 / (1<<31)
        a = 1.0*q31accuracy(a) / (2**31)
        b = 1.0*q31accuracy(b) / (2**31)
    if f == Tools.Q15:
        e = 1.0 / (1<<15)
        a = 1.0*q15accuracy(a) / (2**15)
        b = 1.0*q15accuracy(b) / (2**15)
    if f == Tools.Q7:
        e = 1.0 / (1<<7)
        a = 1.0*q7accuracy(a) / (2**7)
        b = 1.0*q7accuracy(b) / (2**7)

    if b == 0.0:
        if a >= 0.0:
           return(1.0,0)
        else:
           return(-1.0,0)
        
    k = 0
    while abs(a) > abs(b):
       a = a / 2.0
       k = k + 1 
    # In C code we don't saturate but instead generate the right value
    # with a shift of 1.
    # So this test is to ease the comparison between the Python reference
    # and the output of the division algorithm in C
    if abs(a/b) > 1 - e:
       a = a / 2.0
       k = k + 1 

    return(a/b,k)

def initLogValues(format):
    if format == Tools.Q15:
        vals=np.linspace(np.float_power(2,-15),1.0,num=125)
    elif format == Tools.F16:
        vals=np.linspace(np.float_power(2,-10),1.0,num=125)
    else:
        vals=np.linspace(np.float_power(2,-31),1.0,num=125)


    ref=np.log(vals)
    if format==Tools.Q31 :
        # Format must be Q5.26
        ref = ref / 32.0
    if format == Tools.Q15:
        # Format must be Q4.11
        ref = ref / 16.0
    return(vals,ref)


def writeTests(config,format):
    
    a1=np.array([0,math.pi/4,math.pi/2,3*math.pi/4,math.pi,5*math.pi/4,3*math.pi/2,2*math.pi-1e-6])
    a2=np.array([-math.pi/4,-math.pi/2,-3*math.pi/4,-math.pi,-5*math.pi/4,-3*math.pi/2,-2*math.pi-1e-6])
    a3 = a1 + 2*math.pi  
    angles=np.concatenate((a1,a2,a3))
    refcos = np.cos(angles)
    refsin = np.sin(angles)


    vals=np.array([0.0, 0.0, 0.1,1.0,2.0,3.0,3.5,3.6])
    sqrtvals=np.sqrt(vals)

    # Negative values in CMSIS are giving 0
    vals[0] = -0.4
    sqrtvals[0] = 0.0
    
    if format != Tools.F64 and format != 0 and format != 16:
        angles=np.concatenate((a1,a2,a1))
        angles = angles / (2*math.pi)
    config.writeInput(1, angles,"Angles")
    config.writeInput(1, vals,"SqrtInput")
    config.writeReference(1, refcos,"Cos")
    config.writeReference(1, refsin,"Sin")
    config.writeReference(1, sqrtvals,"Sqrt")

    # For benchmarks
    samples=np.random.randn(NBSAMPLES)
    samples = np.abs(Tools.normalize(samples))
    config.writeInput(1, samples,"Samples")

    numerator=np.linspace(-0.9,0.9)
    denominator=np.linspace(-0.9,0.9)

    samples=cartesian(numerator,denominator)
    numerator=[x[0] for x in samples]
    denominator=[x[1] for x in samples]

    result=[divide(format,x) for x in samples]

    resultValue=[x[0] for x in result]
    resultShift=[x[1] for x in result]

    config.writeInput(1, numerator,"Numerator")
    config.writeInput(1, denominator,"Denominator")
    config.writeReference(1, resultValue,"DivisionValue")
    config.writeReferenceS16(1, resultShift,"DivisionShift")


    vals,ref=initLogValues(format)
    config.writeInput(1, vals,"LogInput")
    config.writeReference(1, ref,"Log")





def writeTestsFloat(config,format):

    writeTests(config,format)

    data1 = np.random.randn(20)
    data1 = np.abs(data1)
    data1 = data1 + 1e-3 # To avoid zero values
    data1 = Tools.normalize(data1)


    samples=np.concatenate((np.array([0.0,1.0]),np.linspace(-0.4,0.4)))
    config.writeInput(1, samples,"ExpInput")
    v = np.exp(samples)
    config.writeReference(1, v,"Exp")

    # For benchmarks and other tests
    samples=np.random.randn(NBSAMPLES)
    samples = np.abs(Tools.normalize(samples))
    config.writeInput(1, samples,"Samples")

    v = 1.0 / samples
    config.writeReference(1, v,"Inverse")





    
def generatePatterns():
    PATTERNDIR = os.path.join("Patterns","DSP","FastMath","FastMath")
    PARAMDIR = os.path.join("Parameters","DSP","FastMath","FastMath")
    
    configf64=Tools.Config(PATTERNDIR,PARAMDIR,"f64")
    configf32=Tools.Config(PATTERNDIR,PARAMDIR,"f32")
    configf16=Tools.Config(PATTERNDIR,PARAMDIR,"f16")
    configq31=Tools.Config(PATTERNDIR,PARAMDIR,"q31")
    configq15=Tools.Config(PATTERNDIR,PARAMDIR,"q15")
    
    configf64.setOverwrite(False)
    configf32.setOverwrite(False)
    configf16.setOverwrite(False)
    configq31.setOverwrite(False)
    configq15.setOverwrite(False)

    writeTestsFloat(configf64,Tools.F64)
    writeTestsFloat(configf32,0)
    writeTestsFloat(configf16,16)
    writeTests(configq31,31)
    writeTests(configq15,15)


if __name__ == '__main__':
  generatePatterns()

