# -*- coding: utf-8 -*-
from numpy import array, infty, log, nan, pi, sqrt
from pandas_ta._typing import Array, IntFloat, Number, Union
from pandas_ta.maps import Imports
from pandas_ta.utils import hpoly


def _gaussian_poly_coefficients() -> Array:
    """Three pairs of Polynomial Approximation Coefficients
    for the Gaussian Normal CDF"""

    p0 = array([
        -5.99633501014107895267E1, 9.80010754185999661536E1,
        -5.66762857469070293439E1, 1.39312609387279679503E1,
        -1.23916583867381258016E0
    ])
    q0 = array([
        1.00000000000000000000E0, 1.95448858338141759834E0,
        4.67627912898881538453E0, 8.63602421390890590575E1,
        -2.25462687854119370527E2, 2.00260212380060660359E2,
        -8.20372256168333339912E1, 1.59056225126211695515E1,
        -1.18331621121330003142E0
    ])

    p1 = array([
        4.05544892305962419923E0, 3.15251094599893866154E1,
        5.71628192246421288162E1, 4.40805073893200834700E1,
        1.46849561928858024014E1, 2.18663306850790267539E0,
        -1.40256079171354495875E-1, -3.50424626827848203418E-2,
        -8.57456785154685413611E-4
    ])
    q1 = array([
        1.00000000000000000000E0, 1.57799883256466749731E1,
        4.53907635128879210584E1, 4.13172038254672030440E1,
        1.50425385692907503408E1, 2.50464946208309415979E0,
        -1.42182922854787788574E-1, -3.80806407691578277194E-2,
        -9.33259480895457427372E-4
    ])

    p2 = array([
        3.23774891776946035970E0, 6.91522889068984211695E0,
        3.93881025292474443415E0, 1.33303460815807542389E0,
        2.01485389549179081538E-1, 1.23716634817820021358E-2,
        3.01581553508235416007E-4, 2.65806974686737550832E-6,
        6.23974539184983293730E-9
    ])
    q2 = array([
        1.00000000000000000000E0, 6.02427039364742014255E0,
        3.67983563856160859403E0, 1.37702099489081330271E0,
        2.16236993594496635890E-1, 1.34204006088543189037E-2,
        3.28014464682127739104E-4, 2.89247864745380683936E-6,
        6.79019408009981274425E-9
    ])

    return [p0, q0, p1, q1, p2, q2]


def inv_norm(value: IntFloat) -> Union[None, Number]:
    """Inverse Normal (inv_norm)
    Calculates the 'x' in which the area under the Gaussian PDF is
    equal to value.

    If the user has package "statsmodels" installed, the method will call and
    return norm().ppf(value)

    Source: https://github.com/scipy/scipy/blob/701ffcc8a6f04509d115aac5e5681c538b5265a2/scipy/special/cephes/ndtri.c
    """

    if Imports["statsmodels"]:
        from scipy.stats import norm
        return norm().ppf(value)

    negate = True
    v = value

    # if v == 0.0: return -npInfty
    if v == 0.0:
        return -infty
    if v == 1.0:
        return infty
    if v < 0.0 or value > 1.0:
        return nan

    p0, q0, p1, q1, p2, q2 = _gaussian_poly_coefficients()

    sqrt2pi = sqrt(2 * pi)
    threshold = 0.13533528323661269189
    if v > 1.0 - threshold:
        v, negate = 1.0 - v, False

    # 0 <= |x0 - 0.5| <= 3/8
    if v > threshold:
        v -= 0.5
        v2 = v * v
        y = v + v * (v2 * hpoly(p0, v2) / hpoly(q0, v2))
        y *= sqrt2pi
        return y

    y = sqrt(-2.0 * log(v))
    y0 = y - log(y) / y

    z = 1.0 / y
    if y < 8.0:
        # Approximation for interval z = sqrt(-2 log y ) between 2 and 8
        #  i.e., x between exp(-2) = .135 and exp(-32) = 1.27e-14.
        y1 = z * hpoly(p1, z) / hpoly(q1, z)
    else:
        # Approximation for interval z = sqrt(-2 log y ) between 8 and 64
        # i.e., x between exp(-32) = 1.27e-14 and exp(-2048) = 3.67e-890.
        y1 = z * hpoly(p2, z) / hpoly(q2, z)

    y = y0 - y1
    if negate:
        y = -y

    return y
