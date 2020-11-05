#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import math
import numpy as np
def sigmoid(x):
    r"""sigmoid function

    .. math::
        y = \frac{e^x}{e^x + 1}


    Arguments:
        x {lists or array} -- inputs

    Returns:
        array -- outputs
    """
    ex = np.exp(x)

    return ex / (ex + 1)


print(sigmoid(4))
print(sigmoid(-2))

print(sigmoid((0.98*2)-0.12))