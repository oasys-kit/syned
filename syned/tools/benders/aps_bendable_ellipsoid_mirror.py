#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------- #
# Copyright (c) 2023, UChicago Argonne, LLC. All rights reserved.         #
#                                                                         #
# Copyright 2023. UChicago Argonne, LLC. This software was produced       #
# under U.S. Government contract DE-AC02-06CH11357 for Argonne National   #
# Laboratory (ANL), which is operated by UChicago Argonne, LLC for the    #
# U.S. Department of Energy. The U.S. Government has rights to use,       #
# reproduce, and distribute this software.  NEITHER THE GOVERNMENT NOR    #
# UChicago Argonne, LLC MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR        #
# ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.  If software is     #
# modified to produce derivative works, such modified software should     #
# be clearly marked, so as not to confuse it with the version available   #
# from ANL.                                                               #
#                                                                         #
# Additionally, redistribution and use in source and binary forms, with   #
# or without modification, are permitted provided that the following      #
# conditions are met:                                                     #
#                                                                         #
#     * Redistributions of source code must rein the above copyright    #
#       notice, this list of conditions and the following disclaimer.     #
#                                                                         #
#     * Redistributions in binary form must reproduce the above copyright #
#       notice, this list of conditions and the following disclaimer in   #
#       the documentation and/or other materials provided with the        #
#       distribution.                                                     #
#                                                                         #
#     * Neither the name of UChicago Argonne, LLC, Argonne National       #
#       Laboratory, ANL, the U.S. Government, nor the names of its        #
#       contributors may be used to endorse or promote products derived   #
#       from this software without specific prior written permission.     #
#                                                                         #
# THIS SOFTWARE IS PROVIDED BY UChicago Argonne, LLC AND CONTRIBUTORS     #
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT       #
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS       #
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL UChicago     #
# Argonne, LLC OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,        #
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,    #
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;        #
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER        #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT      #
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN       #
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE         #
# POSSIBILITY OF SUCH DAMAGE.                                             #
# ----------------------------------------------------------------------- #
import numpy
from scipy.interpolate import interp2d
from scipy.optimize import curve_fit

from syned.tools.benders.bender_data import BenderData, BenderParameters


class ApsBenderParameters(BenderParameters):
    def __init__(self,
                 dim_x_minus=None,
                 dim_x_plus=None,
                 bender_bin_x=None,
                 dim_y_minus=None,
                 dim_y_plus=None,
                 bender_bin_y=None,
                 optimized_length=None,
                 p=None,
                 q=None,
                 grazing_angle=None,
                 E=None,
                 h=None,
                 figure_error_mesh=None,
                 n_fit_steps=None,
                 workspace_units_to_m=None,
                 workspace_units_to_mm=None,
                 shape=None,
                 kind_of_bender=None,
                 M1=None,
                 M1_max=False,
                 M1_min=None,
                 M1_fixed=None,
                 e=None,
                 e_max=False,
                 e_min=None,
                 e_fixed=None,
                 ratio=None,
                 ratio_max=False,
                 ratio_min=None,
                 ratio_fixed=None):
        super(ApsBenderParameters, self).__init__(dim_x_minus=dim_x_minus,
                                                  dim_x_plus=dim_x_plus,
                                                  bender_bin_x=bender_bin_x,
                                                  dim_y_minus=dim_y_minus,
                                                  dim_y_plus=dim_y_plus,
                                                  bender_bin_y=bender_bin_y,
                                                  optimized_length=optimized_length,
                                                  p=p,
                                                  q=q,
                                                  grazing_angle=grazing_angle,
                                                  E=E,
                                                  h=h,
                                                  figure_error_mesh=figure_error_mesh,
                                                  n_fit_steps=n_fit_steps,
                                                  workspace_units_to_m=workspace_units_to_m,
                                                  workspace_units_to_mm=workspace_units_to_mm)
        self.shape = shape
        self.kind_of_bender = kind_of_bender
        self.M1 = M1
        self.M1_max = M1_max
        self.M1_min = M1_min
        self.M1_fixed = M1_fixed
        self.e = e
        self.e_max = e_max
        self.e_min = e_min
        self.e_fixed = e_fixed
        self.ratio = ratio
        self.ratio_max = ratio_max
        self.ratio_min = ratio_min
        self.ratio_fixed = ratio_fixed

class ApsBenderData(BenderData):
    def __init__(self,
                 x=None,
                 y=None,
                 ideal_profile=None,
                 bender_profile=None,
                 correction_profile=None,
                 titles=None,
                 z_bender_correction=None,
                 z_figure_error=None,
                 z_bender_correction_no_figure_error=None,
                 M1_out=None,
                 e_out=None,
                 ratio_out=None):
        super(ApsBenderData, self).__init__(x,
                                            y,
                                            ideal_profile,
                                            bender_profile,
                                            correction_profile,
                                            titles,
                                            z_bender_correction,
                                            z_figure_error,
                                            z_bender_correction_no_figure_error)
        self.M1_out    = M1_out
        self.e_out     = e_out
        self.ratio_out = ratio_out

TRAPEZIUM = 0
RECTANGLE = 1

SINGLE_MOMENTUM = 0
DOUBLE_MOMENTUM = 1


def __get_conic_coefficients(bender_parameters : ApsBenderParameters):
    theta_grazing = bender_parameters.grazing_angle
    ssour = bender_parameters.p
    simag = bender_parameters.q

    theta = (numpy.pi / 2) - theta_grazing

    ax_maj = (ssour + simag) / 2
    ax_min = numpy.sqrt(simag * ssour) * numpy.cos(theta)
    eccentricity = numpy.sqrt(ax_maj ** 2 - ax_min ** 2) / ax_maj
    #
    # The center is computed on the basis of the object and image positions
    #
    y_center = (ssour - simag) * 0.5 / eccentricity
    z_center = -numpy.sqrt(1 - y_center ** 2 / ax_maj ** 2) * ax_min
    #
    # Computes now the normal in the mirror center.
    #
    rn_center = numpy.zeros(3)
    rn_center[0] = 0.0
    rn_center[1] = -2 * y_center / ax_maj ** 2
    rn_center[2] = -2 * z_center / ax_min ** 2
    rn_center /= numpy.sqrt((rn_center ** 2).sum())
    #
    # Computes the tangent versor in the mirror center.
    #
    rt_center = numpy.zeros(3)
    rt_center[0] = 0.0
    rt_center[1] = rn_center[2]
    rt_center[2] = -rn_center[1]

    # Computes now the quadric coefficient with the mirror center
    # located at (0,0,0) and normal along (0,0,1)

    A = 1 / ax_min ** 2
    B = 1 / ax_maj ** 2
    C = A

    c1 = 0.0 # A if ellipsoid and 0 if cylinder
    c2 = B * rt_center[1] ** 2 + C * rt_center[2] ** 2
    c3 = B * rn_center[1] ** 2 + C * rn_center[2] ** 2
    c4 = 0.0
    c5 = 2 * (B * rn_center[1] * rt_center[1] + C * rn_center[2] * rt_center[2])
    c6 = 0.0
    c7 = 0.0
    c8 = 0.0
    c9 = 2 * (B * y_center * rn_center[1] + C * z_center * rn_center[2])
    c10 = 0.0

    return c1, c2, c3, c4, c5, c6, c7, c8, c9, c10

def __calculate_ideal_surface(bender_parameters : ApsBenderParameters, sign=-1):
    c1, c2, c3, c4, c5, c6, c7, c8, c9, c10 = __get_conic_coefficients(bender_parameters)

    print("CCC2", [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10])

    x = numpy.linspace(-bender_parameters.dim_x_minus, bender_parameters.dim_x_plus, bender_parameters.bender_bin_x + 1)
    y = numpy.linspace(-bender_parameters.dim_y_minus, bender_parameters.dim_y_plus, bender_parameters.bender_bin_y + 1)

    xx, yy = numpy.meshgrid(x, y)

    c = c1 * (xx ** 2) + c2 * (yy ** 2) + c4 * xx * yy + c7 * xx + c8 * yy + c10
    b = c5 * yy + c6 * xx + c9
    a = c3

    z = (-b + sign * numpy.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    z[b ** 2 - 4 * a * c < 0] = numpy.nan

    return x, y, z.T

def calculate_bender_correction(bender_parameters : ApsBenderParameters) -> ApsBenderData:
    x, y, z = __calculate_ideal_surface(bender_parameters)

    E              = bender_parameters.E
    h              = bender_parameters.h
    shape          = bender_parameters.shape
    kind_of_bender = bender_parameters.kind_of_bender
    
    optimized_length = bender_parameters.optimized_length

    n_fit_steps           = bender_parameters.n_fit_steps
    workspace_units_to_m  = bender_parameters.workspace_units_to_m
    workspace_units_to_mm = bender_parameters.workspace_units_to_mm

    b0 = bender_parameters.dim_x_plus + bender_parameters.dim_x_minus
    L  = bender_parameters.dim_y_plus + bender_parameters.dim_y_minus  # add optimization length

    # flip the coordinate system to be consistent with Mike's formulas
    ideal_profile = z[0, :][::-1]  # one row is the profile of the cylinder, enough for the minimizer
    ideal_profile += -ideal_profile[0] + ((L / 2 + y) * (ideal_profile[0] - ideal_profile[-1])) / L  # Rotation

    if bender_parameters.optimized_length is None:
        y_fit             = y
        ideal_profile_fit = ideal_profile
    else:
        cursor = numpy.where(numpy.logical_and(y >= -optimized_length / 2, y <= optimized_length / 2))
        y_fit             = y[cursor]
        ideal_profile_fit = ideal_profile[cursor]

    epsilon_minus = 1 - 1e-8
    epsilon_plus  = 1 + 1e-8

    Eh_3 = E * h ** 3

    initial_guess   = None
    constraints     = None
    bender_function = None

    if shape == TRAPEZIUM:
        def general_bender_function(Y, M1, e, ratio):
            M2 = M1 * ratio
            A = (M1 + M2) / 2
            B = (M1 - M2) / L
            C = Eh_3 * (2 * b0 + e * b0) / 24
            D = Eh_3 * e * b0 / (12 * L)
            H = (A * D + B * C) / D ** 2
            CDLP = C + D * L / 2
            CDLM = C - D * L / 2
            F = (H / L) * ((CDLM * numpy.log(CDLM) - CDLP * numpy.log(CDLP)) / D + L)
            G = (-H * ((CDLM * numpy.log(CDLM) + CDLP * numpy.log(CDLP))) + (B * L ** 2) / 4) / (2 * D)
            CDY = C + D * Y

            return H * ((CDY / D) * numpy.log(CDY) - Y) - (B * Y ** 2) / (2 * D) + F * Y + G

        def bender_function_2m(Y, M1, e, ratio):
            return general_bender_function(Y, M1, e, ratio)

        def bender_function_1m(Y, M1, e):
            return general_bender_function(Y, M1, e, 1.0)

        if kind_of_bender == SINGLE_MOMENTUM:
            bender_function = bender_function_1m
            initial_guess = [bender_parameters.M1, bender_parameters.e]
            constraints = [[bender_parameters.M1_min if bender_parameters.M1_fixed == False else (bender_parameters.M1 * epsilon_minus),
                            bender_parameters.e_min if bender_parameters.e_fixed == False else (bender_parameters.e * epsilon_minus)],
                           [bender_parameters.M1_max if bender_parameters.M1_fixed == False else (bender_parameters.M1 * epsilon_plus),
                            bender_parameters.e_max if bender_parameters.e_fixed == False else (bender_parameters.e * epsilon_plus)]]
        elif kind_of_bender == DOUBLE_MOMENTUM:
            bender_function = bender_function_2m
            initial_guess = [bender_parameters.M1, bender_parameters.e, bender_parameters.ratio]
            constraints = [[bender_parameters.M1_min if bender_parameters.M1_fixed == False else (bender_parameters.M1 * epsilon_minus),
                            bender_parameters.e_min if bender_parameters.e_fixed == False else (bender_parameters.e * epsilon_minus),
                            bender_parameters.ratio_min if bender_parameters.ratio_fixed == False else (bender_parameters.ratio * epsilon_minus)],
                           [bender_parameters.M1_max if bender_parameters.M1_fixed == False else (bender_parameters.M1 * epsilon_plus),
                            bender_parameters.e_max if bender_parameters.e_fixed == False else (bender_parameters.e * epsilon_plus),
                            bender_parameters.ratio_max if bender_parameters.ratio_fixed == False else (bender_parameters.ratio * epsilon_plus)]]
    elif shape == RECTANGLE:
        def general_bender_function(Y, M1, ratio):
            M2 = M1 * ratio
            A = (M1 + M2) / 2
            B = (M1 - M2) / L
            C = Eh_3 * b0 / 12
            F = (B * L ** 2) / (24 * C)
            G = -(A * L ** 2) / (8 * C)

            return -(B * Y ** 3) / (6 * C) + (A * Y ** 2) / (2 * C) + F * Y + G

        def bender_function_2m(Y, M1, ratio):
            return general_bender_function(Y, M1, ratio)

        def bender_function_1m(Y, M1):
            return general_bender_function(Y, M1, 1.0)

        if kind_of_bender == SINGLE_MOMENTUM:
            bender_function = bender_function_1m
            initial_guess = [bender_parameters.M1]
            constraints = [[bender_parameters.M1_min if bender_parameters.M1_fixed == False else (bender_parameters.M1 * epsilon_minus)],
                           [bender_parameters.M1_max if bender_parameters.M1_fixed == False else (bender_parameters.M1 * epsilon_plus)]]
        elif kind_of_bender == DOUBLE_MOMENTUM:
            bender_function = bender_function_2m
            initial_guess = [bender_parameters.M1, bender_parameters.ratio]
            constraints = [[bender_parameters.M1_min if bender_parameters.M1_fixed == False else (bender_parameters.M1 * epsilon_minus),
                            bender_parameters.ratio_min if bender_parameters.ratio_fixed == False else (bender_parameters.ratio * epsilon_minus)],
                           [bender_parameters.M1_max if bender_parameters.M1_fixed == False else (bender_parameters.M1 * epsilon_plus),
                            bender_parameters.ratio_max if bender_parameters.ratio_fixed == False else (bender_parameters.ratio * epsilon_plus)]]

    for i in range(n_fit_steps):
        parameters, _ = curve_fit(f=bender_function,
                                  xdata=y_fit,
                                  ydata=ideal_profile_fit,
                                  p0=initial_guess,
                                  bounds=constraints,
                                  method='trf')
        initial_guess = parameters

    if len(parameters) == 1:    bender_profile = bender_function(y, parameters[0])
    elif len(parameters) == 2:  bender_profile = bender_function(y, parameters[0], parameters[1])
    else:                       bender_profile = bender_function(y, parameters[0], parameters[1], parameters[2])

    # rotate back to Shadow system
    bender_profile = bender_profile[::-1]
    ideal_profile  = ideal_profile[::-1]

    # from here it's Shadow Axis system
    correction_profile = ideal_profile - bender_profile

    # r-squared = 1 - residual sum of squares / total sum of squares
    r_squared         = 1 - (numpy.sum(correction_profile ** 2) / numpy.sum((ideal_profile - numpy.mean(ideal_profile)) ** 2))
    rms               = round(correction_profile.std() * 1e9 * workspace_units_to_m, 6)
    if not bender_parameters.optimized_length is None:  rms_opt = round(correction_profile[cursor].std() * 1e9 * workspace_units_to_m, 6)

    z_bender_correction_no_figure_error = numpy.zeros(z.shape)

    for i in range(z_bender_correction_no_figure_error.shape[0]): z_bender_correction_no_figure_error[i, :] = numpy.copy(correction_profile)

    if not bender_parameters.figure_error_mesh is None:
        x_e, y_e, z_e = bender_parameters.figure_error_mesh

        if len(x) == len(x_e) and len(y) == len(y_e) and \
                x[0] == x_e[0] and x[-1] == x_e[-1] and \
                y[0] == y_e[0] and y[-1] == y_e[-1]:
            z_figure_error = z_e
        else:
            z_figure_error = interp2d(y_e, x_e, z_e, kind='cubic')(y, x)

        z_bender_correction = z_bender_correction_no_figure_error + z_figure_error
    else:                                          
        z_figure_error = None
        z_bender_correction = z_bender_correction_no_figure_error

    bender_data = ApsBenderData(x=x,
                                y=y,
                                ideal_profile=ideal_profile,
                                bender_profile=bender_profile,
                                correction_profile=correction_profile,
                                titles=["Bender vs. Ideal Profiles" + "\n" + r'$R^2$ = ' + str(r_squared),
                                        "Correction Profile 1D, r.m.s. = " + str(rms) + " nm" +
                                        ("" if optimized_length is None else (", " + str(rms_opt) + " nm (optimized)"))],
                                z_bender_correction=z_bender_correction,
                                z_figure_error=z_figure_error,
                                z_bender_correction_no_figure_error=z_bender_correction_no_figure_error)


    bender_data.M1_out = round(parameters[0], int(6 * workspace_units_to_mm))
    if shape == TRAPEZIUM:
        bender_data.e_out = round(parameters[1], 5)
        if kind_of_bender == DOUBLE_MOMENTUM: bender_data.ratio_out = round(parameters[2], 5)
    elif shape == RECTANGLE:
        if kind_of_bender == DOUBLE_MOMENTUM: bender_data.ratio_out = round(parameters[1], 5)

    return bender_data
