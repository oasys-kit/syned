#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------- #
# Copyright (c) 2021, UChicago Argonne, LLC. All rights reserved.         #
#                                                                         #
# Copyright 2021. UChicago Argonne, LLC. This software was produced       #
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
from scipy import integrate

from syned.tools.benders.bender_data import BenderData, BenderParameters

class DoubleRodBenderParameters(BenderParameters):
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
                 r=None,
                 l=None,
                 R0=None,
                 R0_max=False,
                 R0_min=None,
                 R0_fixed=None,
                 eta=None,
                 eta_max=False,
                 eta_min=None,
                 eta_fixed=None,
                 W2=None,
                 W2_max=False,
                 W2_min=None,
                 W2_fixed=None):
        super(DoubleRodBenderParameters, self).__init__(dim_x_minus=dim_x_minus,
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
        self.r = r
        self.l = l
        self.R0 = R0
        self.R0_max = R0_max
        self.R0_min = R0_min
        self.R0_fixed = R0_fixed
        self.eta = eta
        self.eta_max = eta_max
        self.eta_min = eta_min
        self.eta_fixed = eta_fixed
        self.W2 = W2
        self.W2_max = W2_max
        self.W2_min = W2_min
        self.W2_fixed = W2_fixed


class DoubleRodBenderData(BenderData):
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
                 R0_out=None,
                 eta_out=None,
                 W2_out=None,
                 alpha= None,
                 W0=None,
                 F_upstream=None,
                 F_downstream=None):
        super(DoubleRodBenderData, self).__init__(x,
                                            y,
                                            ideal_profile,
                                            bender_profile,
                                            correction_profile,
                                            titles,
                                            z_bender_correction,
                                            z_figure_error,
                                            z_bender_correction_no_figure_error)
        self.R0_out       = R0_out
        self.eta_out      = eta_out
        self.W2_out       = W2_out
        self.alpha        = alpha
        self.W0           = W0
        self.F_upstream   = F_upstream
        self.F_downstream = F_downstream

def calculate_bender_correction(bender_parameters : DoubleRodBenderParameters) -> DoubleRodBenderData:
    workspace_units_to_m  = bender_parameters.workspace_units_to_m
    workspace_units_to_mm = bender_parameters.workspace_units_to_mm

    x             = numpy.linspace(-bender_parameters.dim_x_minus, bender_parameters.dim_x_plus, bender_parameters.bender_bin_x + 1)
    y             = numpy.linspace(-bender_parameters.dim_y_minus, bender_parameters.dim_y_plus, bender_parameters.bender_bin_y + 1)
    W1            = bender_parameters.dim_x_plus + bender_parameters.dim_x_minus
    L             = bender_parameters.dim_y_plus + bender_parameters.dim_y_minus
    p             = bender_parameters.p
    q             = bender_parameters.q
    grazing_angle = bender_parameters.grazing_angle

    optimized_length = bender_parameters.optimized_length

    E = bender_parameters.E
    l = bender_parameters.l
    h = bender_parameters.h
    r = bender_parameters.r

    if optimized_length is None:
        y_fit = y
    else:
        cursor = numpy.where(numpy.logical_and(y >= -optimized_length / 2, y <= optimized_length / 2))
        y_fit = y[cursor]

    ideal_slope_profile_fit = ideal_slope_profile(y_fit, p, q, grazing_angle)

    epsilon_minus = 1 - 1e-8
    epsilon_plus  = 1 + 1e-8

    initial_guess    = [bender_parameters.R0, bender_parameters.eta, bender_parameters.W2]
    constraints     =  [[bender_parameters.R0_min if bender_parameters.R0_fixed == False else (bender_parameters.R0 * epsilon_minus),
                         bender_parameters.eta_min if bender_parameters.eta_fixed == False else (bender_parameters.eta * epsilon_minus),
                         bender_parameters.W2_min if bender_parameters.W2_fixed == False else (bender_parameters.W2 * epsilon_minus)],
                        [bender_parameters.R0_max if bender_parameters.R0_fixed == False else (bender_parameters.R0 * epsilon_plus),
                         bender_parameters.eta_max if bender_parameters.eta_fixed == False else (bender_parameters.eta * epsilon_plus),
                         bender_parameters.W2_max if bender_parameters.W2_fixed == False else (bender_parameters.W2 * epsilon_plus)]
                       ]

    def bender_function(x, R0, eta, W2):
        return __bender_slope_profile(x, p, q, grazing_angle, W1, L, R0 / workspace_units_to_m, eta, W2 / workspace_units_to_mm)

    for i in range(bender_parameters.n_fit_steps):
        parameters, _ = curve_fit(f=bender_function,
                                  xdata=y_fit,
                                  ydata=ideal_slope_profile_fit,
                                  p0=initial_guess,
                                  bounds=constraints,
                                  method='trf')
        initial_guess = parameters

    R0  = parameters[0] / workspace_units_to_m # here in workspace units
    eta = parameters[1]
    W2  = parameters[2] / workspace_units_to_mm

    alpha = calculate_taper_factor(W1, W2, L, p, q, grazing_angle)
    W0    = calculate_W0(W1, alpha, L, p, q, grazing_angle) # W at the center

    bender_profile = __bender_height_profile(y, p, q, grazing_angle, R0, eta, alpha)

    F_upstream, F_downstream = calculate_bender_forces(q, R0, eta, E, W0, l, h, r)

    parameters = numpy.append(parameters, round(alpha, 3))
    parameters = numpy.append(parameters, round(W0 * workspace_units_to_mm, 4))
    parameters = numpy.append(parameters, round(F_upstream, 6))
    parameters = numpy.append(parameters, round(F_downstream, 6))

    ideal_profile  = ideal_height_profile(y, p, q, grazing_angle)

    # back to Shadow system
    bender_profile -= numpy.min(bender_profile)
    ideal_profile  -= numpy.min(ideal_profile)

    # from here it's Shadow Axis system
    correction_profile = ideal_profile - bender_profile
    if not optimized_length is None: correction_profile_fit = correction_profile[cursor]

    # r-squared = 1 - residual sum of squares / total sum of squares
    r_squared = 1 - (numpy.sum(correction_profile ** 2) / numpy.sum((ideal_profile - numpy.mean(ideal_profile)) ** 2))
    rms       = round(correction_profile.std() * 1e9 * workspace_units_to_m, 6)
    if not bender_parameters.optimized_length is None: rms_opt = round(correction_profile_fit.std() * 1e9 * workspace_units_to_m, 6)

    z_bender_correction = numpy.zeros((len(x), len(y)))

    for i in range(z_bender_correction.shape[0]): z_bender_correction[i, :] = numpy.copy(correction_profile)

    bender_data = DoubleRodBenderData(x=x,
                                      y=y,
                                      ideal_profile=ideal_profile,
                                      bender_profile=bender_profile,
                                      correction_profile=correction_profile,
                                      titles=["Bender vs. Ideal Profiles" + "\n" + r'$R^2$ = ' + str(r_squared),
                                              "Correction Profile 1D, r.m.s. = " + str(rms) + " nm" +
                                              ("" if optimized_length is None else (", " + str(rms_opt) + " nm (optimized)"))],
                                      z_bender_correction_no_figure_error=z_bender_correction)

    if not bender_parameters.figure_error_mesh is None:
        x_e, y_e, z_e = bender_parameters.figure_error_mesh

        if len(x) == len(x_e) and len(y) == len(y_e) and \
                x[0] == x_e[0] and x[-1] == x_e[-1] and \
                y[0] == y_e[0] and y[-1] == y_e[-1]:
            z_figure_error = z_e
        else:
            z_figure_error = interp2d(y_e, x_e, z_e, kind='cubic')(y, x)

        bender_data.z_figure_error      = z_figure_error
        bender_data.z_bender_correction = bender_data.z_bender_correction_no_figure_error + z_figure_error
    else:
        bender_data.z_bender_correction = bender_data.z_bender_correction_no_figure_error


    bender_data.R0_out       = round(parameters[0], 5)
    bender_data.eta_out      = parameters[1]
    bender_data.W2_out       = round(parameters[2], 3)
    bender_data.alpha        = parameters[3]
    bender_data.W0           = parameters[4]
    bender_data.F_upstream   = parameters[5]
    bender_data.F_downstream = parameters[6]

    return bender_data

def __focal_distance(p, q):
    return p*q/(p+q)

def __demagnification_factor(p, q):
    return p/q

def __mu_nu(m):
    return (m - 1) / (m + 1), m/(m+1)**2

def __calculate_ideal_slope_variation(y, fprime, K0id, mu, nu):
    return 2*fprime*K0id*((2 * nu * (y / fprime) + mu) / numpy.sqrt(1 - mu * (y / fprime) - nu * (y / fprime) ** 2) - mu)

def __fprime(p, q, grazing_angle):
    return __focal_distance(p, q) / numpy.cos(grazing_angle)


def __calculate_bender_slope_variation(y, fprime, K0, eta, alpha):
    return -(K0*fprime/alpha**2)*(eta * alpha * (y / fprime) + (eta + alpha) * numpy.log(1 - (alpha * y / fprime)))

def calculate_taper_factor(W1, W2, L, p, q, grazing_angle):
    # W2 = W1(1 - alpha L/f')
    # W2/W1 - 1 = - alpha  L/f'
    # f'/L ( 1 - W2/W1) = alpha
    return (1 - W2/W1) * (__fprime(p, q, grazing_angle) / L)

def calculate_W0(W1, alpha, L, p, q, grazing_angle):
    return W1*(1 - alpha * L / (2 * __fprime(p, q, grazing_angle)))

def ideal_slope_profile(y, p, q, grazing_angle):
    mu, nu = __mu_nu(__demagnification_factor(p, q))
    fprime = __focal_distance(p, q)/numpy.cos(grazing_angle)
    K0id   = numpy.tan(grazing_angle)/(2*fprime)

    return __calculate_ideal_slope_variation(y, fprime, K0id, mu, nu)

def ideal_height_profile(y, p, q, grazing_angle):
    mu, nu = __mu_nu(__demagnification_factor(p, q))
    fprime = __focal_distance(p, q)/numpy.cos(grazing_angle)
    K0id   = numpy.tan(grazing_angle)/(2*fprime)

    profile = numpy.zeros(len(y))
    for i in range(len(y)): profile[i] = integrate.quad(func=(lambda x: __calculate_ideal_slope_variation(x, fprime, K0id, mu, nu)), a=y[0], b=y[i])[0]

    return profile

def __bender_slope_profile(y, p, q, grazing_angle, W1, L, R0, eta, W2):
    return __calculate_bender_slope_variation(y, __fprime(p, q, grazing_angle), 1 / R0, eta, alpha=calculate_taper_factor(W1, W2, L, p, q, grazing_angle))

def __bender_height_profile(y, p, q, grazing_angle, R0, eta, alpha):
    fprime = __fprime(p, q, grazing_angle)

    profile = numpy.zeros(len(y))
    for i in range(len(y)):
        profile[i] = integrate.quad(func=(lambda x: __calculate_bender_slope_variation(x, fprime, 1/R0, eta, alpha)), a=y[0], b=y[i])[0]

    return profile

# -----------------------------------------------
# q = focus distance (from mirror center) (1/p + 1/q = 1/f lenses equation)
# eta = bender asymmetry factor (from slope minimization)
# K0 = 1/R (radius of curvature at the center)
# E0 = Young's modulus
# L = length of the mirror
# r = distance between inner ond outer rods
# ----------------------------------------------------------------
def calculate_bender_forces(q, R0, eta, E, W0, L, h, r):
    I0 = (W0*h**3)/12
    M0 = E*I0/R0
    F_upstream = (M0/r) * (1 - (eta*(L + 2*r)/(2*q)))
    F_downstream = (M0/r) * (1 + (eta*(L + 2*r)/(2*q)))

    return F_upstream, F_downstream
