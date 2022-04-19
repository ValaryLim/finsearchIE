import numpy as np
import numba

@numba.njit(
    [
        "f4(f4[::1],f4[::1])",
        numba.types.float32(
            numba.types.Array(numba.types.float32, 1, "C", readonly=True),
            numba.types.Array(numba.types.float32, 1, "C", readonly=True),
        ),
    ],
    fastmath=True,
    locals={
        "result_1": numba.types.float32,
        "result_2": numba.types.float32,
        "norm_x1": numba.types.float32,
        "norm_y1": numba.types.float32,
        "norm_x2": numba.types.float32,
        "norm_y2": numba.types.float32,
        "dim": numba.types.intp,
        "i": numba.types.uint16,
        "cosine_1": numba.types.float32,
        "cosine_2": numba.types.float32,
    },
)
def relation_cosine(x, y):
    result_1, result_2 = 0.0, 0.0
    norm_x1, norm_x2 = 0.0, 0.0
    norm_y1, norm_y2 = 0.0, 0.0
    dim = x.shape[0]
    for i in range(dim / 2):
        result_1 += x[i] * y[i]
        norm_x1 += x[i] * x[i]
        norm_y1 += y[i] * y[i]
    for i in range(dim/2, dim):
        result_2 += x[i] * y[i]
        norm_x2 += x[i] * x[i]
        norm_y2 += y[i] * y[i]
    cosine_1, cosine_2 = 0.0, 0.0
    if norm_x1 == 0.0 and norm_y1 == 0.0:
        cosine_1 = 0.0
    elif norm_x1 == 0.0 or norm_y1 == 0.0:
        cosine_1 = 1.0
    else:
        cosine_1 = 1.0 - (result_1 / np.sqrt(norm_x1 * norm_y1))
    if norm_x2 == 0.0 and norm_y2 == 0.0:
        cosine_2 = 0.0
    elif norm_x2 == 0.0 or norm_y2 == 0.0:
        cosine_2 = 1.0
    else:
        cosine_2 = 1.0 - (result_2 / np.sqrt(norm_x2 * norm_y2))
    return np.log2(0.5 * (cosine_1 + cosine_2)) # remove bounds


@numba.njit(
    [
        "f4(f4[::1],f4[::1])",
        numba.types.float32(
            numba.types.Array(numba.types.float32, 1, "C", readonly=True),
            numba.types.Array(numba.types.float32, 1, "C", readonly=True),
        ),
    ],
    fastmath=True,
    locals={
        "result_1": numba.types.float32,
        "result_2": numba.types.float32,
        "result_3": numba.types.float32,
        "result_4": numba.types.float32,
        "norm_x1": numba.types.float32,
        "norm_y1": numba.types.float32,
        "norm_x2": numba.types.float32,
        "norm_y2": numba.types.float32,
        "dim": numba.types.intp,
        "dim_half": numba.types.intp,
        "i": numba.types.uint16,
        "cosine_1a": numba.types.float32,
        "cosine_1b": numba.types.float32,
        "cosine_2a": numba.types.float32,
        "cosine_2b": numba.types.float32,
    },
)
def relation_cosine_directionless(x, y):
    result_1, result_2, result_3, result_4 = 0.0, 0.0, 0.0, 0.0
    norm_x1, norm_x2 = 0.0, 0.0
    norm_y1, norm_y2 = 0.0, 0.0
    dim = x.shape[0]
    dim_half = dim / 2
    for i in range(dim_half):
        result_1 += x[i] * y[i]
        result_3 += x[i] * y[dim_half+i]
        result_4 += y[i] * x[dim_half+i]
        norm_x1 += x[i] * x[i]
        norm_y1 += y[i] * y[i]
    for i in range(dim_half, dim):
        result_2 += x[i] * y[i]
        norm_x2 += x[i] * x[i]
        norm_y2 += y[i] * y[i]
    cosine_1a, cosine_1b, cosine_2a, cosine_2b = 0.0, 0.0, 0.0, 0.0
    if norm_x1 == 0.0 and norm_y1 == 0.0:
        cosine_1a = 0.0
    elif norm_x1 == 0.0 or norm_y1 == 0.0:
        cosine_1a = 1.0
    else:
        cosine_1a = 1.0 - (result_1 / np.sqrt(norm_x1 * norm_y1))
    if norm_x2 == 0.0 and norm_y2 == 0.0:
        cosine_2a = 0.0
    elif norm_x2 == 0.0 or norm_y2 == 0.0:
        cosine_2a = 1.0
    else:
        cosine_2a = 1.0 - (result_2 / np.sqrt(norm_x2 * norm_y2))
    if norm_x1 == 0.0 and norm_y2 == 0.0:
        cosine_1b = 0.0
    elif norm_x1 == 0.0 or norm_y2 == 0.0:
        cosine_1b = 0.0
    else:
        cosine_1b = 1.0 - (result_3 / np.sqrt(norm_x1 * norm_y2))
    if norm_x2 == 0.0 and norm_y1 == 0.0:
        cosine_2b = 0.0
    elif norm_x2 == 0.0 or norm_y1 == 0.0:
        cosine_2b = 0.0
    else:
        cosine_2b = 1.0 - (result_4 / np.sqrt(norm_x2 * norm_y1))
    return min(np.log2(0.5 * (cosine_1a + cosine_2a)), np.log2(0.5 * (cosine_1b + cosine_2b))) 