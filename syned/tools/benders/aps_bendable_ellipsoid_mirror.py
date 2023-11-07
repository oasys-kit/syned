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
#     * Redistributions of source code must retain the above copyright    #
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

from syned.tools.benders.bender_data_to_plot import BenderDataToPlot

TRAPEZIUM = 0
RECTANGLE = 1

SINGLE_MOMENTUM = 0
DOUBLE_MOMENTUM = 1

class ApsBenderParameters:
    dim_x_minus = None
    dim_x_plus = None
    bender_bin_x = None
    dim_y_minus = None
    dim_y_plus = None
    bender_bin_y = None
    conic_coefficients = None

    optimized_length = None
    n_fit_steps = None
    
    E = None
    h = None
    shape = None
    kind_of_bender = None

    M1 = None
    M1_min = None
    M1_max = None
    M1_fixed = None
    
    e = None
    e_min = None
    e_max = None
    e_fixed = None

    ratio = None
    ratio_min = None
    ratio_max = None
    ratio_fixed = None

    workspace_units_to_m = None

    figure_error = None


def calculate_ideal_surface(bender_parameters : ApsBenderParameters, sign=-1):
    x = numpy.linspace(-bender_parameters.dim_x_minus, bender_parameters.dim_x_plus, bender_parameters.bender_bin_x + 1)
    y = numpy.linspace(-bender_parameters.dim_y_minus, bender_parameters.dim_y_plus, bender_parameters.bender_bin_y + 1)

    c1  = round(bender_parameters.conic_coefficients[0], 10)
    c2  = round(bender_parameters.conic_coefficients[1], 10)
    c3  = round(bender_parameters.conic_coefficients[2], 10)
    c4  = round(bender_parameters.conic_coefficients[3], 10)
    c5  = round(bender_parameters.conic_coefficients[4], 10)
    c6  = round(bender_parameters.conic_coefficients[5], 10)
    c7  = round(bender_parameters.conic_coefficients[6], 10)
    c8  = round(bender_parameters.conic_coefficients[7], 10)
    c9  = round(bender_parameters.conic_coefficients[8], 10)
    c10 = round(bender_parameters.conic_coefficients[9], 10)

    xx, yy = numpy.meshgrid(x, y)

    c = c1 * (xx ** 2) + c2 * (yy ** 2) + c4 * xx * yy + c7 * xx + c8 * yy + c10
    b = c5 * yy + c6 * xx + c9
    a = c3

    z = (-b + sign * numpy.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    z[b ** 2 - 4 * a * c < 0] = numpy.nan

    return x, y, z.T

def calculate_bender_correction(bender_parameters : ApsBenderParameters):
    x, y, z = calculate_ideal_surface(bender_parameters)

    E              = bender_parameters.E
    h              = bender_parameters.h
    shape          = bender_parameters.shape
    kind_of_bender = bender_parameters.kind_of_bender
    
    optimized_length = bender_parameters.optimized_length

    n_fit_steps           = bender_parameters.n_fit_steps
    workspace_units_to_m  = bender_parameters.workspace_units_to_m

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

    if not bender_parameters.figure_error is None:
        x_e, y_e, z_e = bender_parameters.figure_error

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

    return parameters, BenderDataToPlot(x=bender_parameters.x,
                                        y=bender_parameters.y,
                                        ideal_profile=ideal_profile,
                                        bender_profile=bender_profile,
                                        correction_profile=correction_profile,
                                        titles=["Bender vs. Ideal Profiles" + "\n" + r'$R^2$ = ' + str(r_squared),
                                         "Correction Profile 1D, r.m.s. = " + str(rms) + " nm" + ("" if optimized_length is None else (", " + str(rms_opt) + " nm (optimized)"))],
                                        z_bender_correction=z_bender_correction,
                                        z_figure_error=z_figure_error,
                                        z_bender_correction_no_figure_error=z_bender_correction_no_figure_error)
