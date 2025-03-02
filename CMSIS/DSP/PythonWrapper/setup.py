from distutils.core import setup, Extension
import glob
import numpy
import config
import sys
import os
import os.path
from config import ROOT
import re

includes = [os.path.join(ROOT,"Include"),os.path.join(ROOT,"PrivateInclude"),os.path.join("cmsisdsp_pkg","src")]

if sys.platform == 'win32':
  cflags = ["-DWIN",config.cflags,"-DUNALIGNED_SUPPORT_DISABLE"] 
else:
  cflags = ["-Wno-attributes","-Wno-unused-function","-Wno-unused-variable","-Wno-implicit-function-declaration",config.cflags,"-D__GNUC_PYTHON__"]

transform = glob.glob(os.path.join(ROOT,"Source","TransformFunctions","*.c"))
#transform.remove(os.path.join(ROOT,"Source","TransformFunctions","arm_dct4_init_q15.c"))
#transform.remove(os.path.join(ROOT,"Source","TransformFunctions","arm_rfft_init_q15.c"))
transform.remove(os.path.join(ROOT,"Source","TransformFunctions","TransformFunctions.c"))
transform.remove(os.path.join(ROOT,"Source","TransformFunctions","TransformFunctionsF16.c"))

support = glob.glob(os.path.join(ROOT,"Source","SupportFunctions","*.c"))
support.remove(os.path.join(ROOT,"Source","SupportFunctions","SupportFunctions.c"))
support.remove(os.path.join(ROOT,"Source","SupportFunctions","SupportFunctionsF16.c"))

fastmath = glob.glob(os.path.join(ROOT,"Source","FastMathFunctions","*.c"))
fastmath.remove(os.path.join(ROOT,"Source","FastMathFunctions","FastMathFunctions.c"))

filtering = glob.glob(os.path.join(ROOT,"Source","FilteringFunctions","*.c"))
filtering.remove(os.path.join(ROOT,"Source","FilteringFunctions","FilteringFunctions.c"))
filtering.remove(os.path.join(ROOT,"Source","FilteringFunctions","FilteringFunctionsF16.c"))

matrix = glob.glob(os.path.join(ROOT,"Source","MatrixFunctions","*.c"))
matrix.remove(os.path.join(ROOT,"Source","MatrixFunctions","MatrixFunctions.c"))
matrix.remove(os.path.join(ROOT,"Source","MatrixFunctions","MatrixFunctionsF16.c"))

statistics = glob.glob(os.path.join(ROOT,"Source","StatisticsFunctions","*.c"))
statistics.remove(os.path.join(ROOT,"Source","StatisticsFunctions","StatisticsFunctions.c"))
statistics.remove(os.path.join(ROOT,"Source","StatisticsFunctions","StatisticsFunctionsF16.c"))

complexf = glob.glob(os.path.join(ROOT,"Source","ComplexMathFunctions","*.c"))
complexf.remove(os.path.join(ROOT,"Source","ComplexMathFunctions","ComplexMathFunctions.c"))
complexf.remove(os.path.join(ROOT,"Source","ComplexMathFunctions","ComplexMathFunctionsF16.c"))

basic = glob.glob(os.path.join(ROOT,"Source","BasicMathFunctions","*.c"))
basic.remove(os.path.join(ROOT,"Source","BasicMathFunctions","BasicMathFunctions.c"))
basic.remove(os.path.join(ROOT,"Source","BasicMathFunctions","BasicMathFunctionsF16.c"))

controller = glob.glob(os.path.join(ROOT,"Source","ControllerFunctions","*.c"))
controller.remove(os.path.join(ROOT,"Source","ControllerFunctions","ControllerFunctions.c"))

common = glob.glob(os.path.join(ROOT,"Source","CommonTables","*.c"))
common.remove(os.path.join(ROOT,"Source","CommonTables","CommonTables.c"))
common.remove(os.path.join(ROOT,"Source","CommonTables","CommonTablesF16.c"))

interpolation = glob.glob(os.path.join(ROOT,"Source","InterpolationFunctions","*.c"))
interpolation.remove(os.path.join(ROOT,"Source","InterpolationFunctions","InterpolationFunctions.c"))
interpolation.remove(os.path.join(ROOT,"Source","InterpolationFunctions","InterpolationFunctionsF16.c"))

quaternion = glob.glob(os.path.join(ROOT,"Source","QuaternionMathFunctions","*.c"))
quaternion.remove(os.path.join(ROOT,"Source","QuaternionMathFunctions","QuaternionMathFunctions.c"))

#distance = glob.glob(os.path.join(ROOT,"Source","DistanceFunctions","*.c"))
#distance.remove(os.path.join(ROOT,"Source","DistanceFunctions","DistanceFunctions.c"))


#modulesrc = glob.glob(os.path.join("cmsisdsp_pkg","src","*.c"))
modulesrc = []
modulesrc.append(os.path.join("cmsisdsp_pkg","src","cmsismodule.c"))

allsrcs = support + fastmath + filtering + matrix + statistics + complexf + basic
allsrcs = allsrcs + controller + transform + modulesrc + common+ interpolation
allsrcs = allsrcs + quaternion

missing=set(["arm_abs_f64"
,"arm_absmax_f64"
,"arm_absmin_f64"
,"arm_add_f64"
,"arm_barycenter_f32"
,"arm_braycurtis_distance_f32"
,"arm_canberra_distance_f32"
,"arm_chebyshev_distance_f32"
,"arm_chebyshev_distance_f64"
,"arm_circularRead_f32"
,"arm_cityblock_distance_f32"
,"arm_cityblock_distance_f64"
,"arm_cmplx_mag_f64"
,"arm_cmplx_mag_squared_f64"
,"arm_cmplx_mult_cmplx_f64"
,"arm_copy_f64"
,"arm_correlate_f64"
,"arm_correlation_distance_f32"
,"arm_cosine_distance_f32"
,"arm_cosine_distance_f64"
,"arm_dot_prod_f64"
,"arm_entropy_f32"
,"arm_entropy_f64"
,"arm_euclidean_distance_f32"
,"arm_euclidean_distance_f64"
,"arm_exponent_f32"
,"arm_fill_f64"
,"arm_fir_f64"
,"arm_fir_init_f64"
,"arm_gaussian_naive_bayes_predict_f32"
,"arm_jensenshannon_distance_f32"
,"arm_kullback_leibler_f32"
,"arm_kullback_leibler_f64"
,"arm_logsumexp_dot_prod_f32"
,"arm_logsumexp_f32"
,"arm_mat_cholesky_f32"
,"arm_mat_cholesky_f64"
,"arm_mat_init_f32"
,"arm_mat_ldlt_f32"
,"arm_mat_ldlt_f64"
,"arm_mat_mult_f64"
,"arm_mat_solve_lower_triangular_f32"
,"arm_mat_solve_lower_triangular_f64"
,"arm_mat_solve_upper_triangular_f32"
,"arm_mat_solve_upper_triangular_f64"
,"arm_mat_sub_f64"
,"arm_mat_trans_f64"
,"arm_max_f64"
,"arm_max_no_idx_f32"
,"arm_max_no_idx_f64"
,"arm_mean_f64"
,"arm_merge_sort_f32"
,"arm_merge_sort_init_f32"
,"arm_min_f64"
,"arm_minkowski_distance_f32"
,"arm_mult_f64"
,"arm_negate_f64"
,"arm_offset_f64"
,"arm_power_f64"
,"arm_scale_f64"
,"arm_sort_f32"
,"arm_sort_init_f32"
,"arm_spline_f32"
,"arm_spline_init_f32"
,"arm_std_f64"
,"arm_sub_f64"
,"arm_svm_linear_init_f32"
,"arm_svm_linear_predict_f32"
,"arm_svm_polynomial_init_f32"
,"arm_svm_polynomial_predict_f32"
,"arm_svm_rbf_init_f32"
,"arm_svm_rbf_predict_f32"
,"arm_svm_sigmoid_init_f32"
,"arm_svm_sigmoid_predict_f32"
,"arm_var_f64"
,"arm_vexp_f32"
,"arm_vexp_f64"
,"arm_vlog_f64"
,"arm_vsqrt_f32"
,"arm_weighted_sum_f32"
,"arm_circularRead_q15"
,"arm_circularRead_q7"
,"arm_div_q63_to_q31"
,"arm_fir_sparse_q15"
,"arm_fir_sparse_q31"
,"arm_fir_sparse_q7"
,"arm_mat_init_q15"
,"arm_mat_init_q31"])

def notf16(number):
  if re.search(r'f16',number):
     return(False)
  if re.search(r'F16',number):
     return(False)
  return(True)

def isnotmissing(src):
  name=os.path.splitext(os.path.basename(src))[0]
  return(not (name in missing))

# If there are too many files, the linker command is failing on Windows.
# So f16 functions are removed since they are not currently available in the wrapper.
# A next version will have to structure this wrapper more cleanly so that the
# build can work even with more functions
srcs = list(filter(isnotmissing,list(filter(notf16, allsrcs))))


module1 = Extension(config.extensionName,
                    sources = (srcs
                              )
                              ,
                    include_dirs =  includes + [numpy.get_include()],
                    #extra_compile_args = ["-Wno-unused-variable","-Wno-implicit-function-declaration",config.cflags]
                    extra_compile_args = cflags
                              )

setup (name = config.setupName,
       version = '1.0.0',
       packages=['cmsisdsp'],
       description = config.setupDescription,
       ext_modules = [module1],
       author = 'Copyright (C) 2010-2021 ARM Limited or its affiliates. All rights reserved.',
       url="https://github.com/ARM-software/CMSIS_5",
       classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ])
