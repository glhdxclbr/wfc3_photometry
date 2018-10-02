import numpy as np

from bisect import bisect_left

def make_id_list(coord_ints, x_digits=None, y_digits=None):
    """
    Turns pixel coordinates into IDs for each star.

    Each ID is just the X and Y integer pixel postions concatenated.
    For example, (3894, 215) becomes 38940215.  These IDs are then
    used in the matching process.

    Parameters
    ----------
    coord_ints : ndarray
        Nx2 array of coordinates.  Must be integers
    x_digits : int, optional
        Number of digits in the x coordinates.  If none, will
        calculate from largest value.  Necessary for correct
        padding of of ID.
    y_digits : int, optional
        Number of digits in the y coordinates.  If none, will
        calculate from largest value.  Necessary for correct
        padding of of ID.

    Returns
    -------
    ids: list
        List of ids for the source positions from the input coords.
    """
    xs = coord_ints[0]
    ys = coord_ints[1]
    if not x_digits:
        x_digits = len(str(max(xs)))
    if not y_digits:
        y_digits = len(str(max(ys)))
    ids = []
    for i in range(len(xs)):
        coord_id = str(xs[i]).zfill(x_digits) + str(ys[i]).zfill(y_digits)
        ids.append(coord_id)
    return ids


def get_match_indices(master_ids, input_ids):
    """Matches ID from master list with input ids from input catalog"""

    matched_indices = []
    input_sorted_inds = np.argsort(input_ids)
    input_ids = sorted(input_ids)
    for master_id in master_ids:
        ind = binary_search_index(input_ids, master_id)

        if ind >= 0:
            matched_indices.append(input_sorted_inds[ind])
        else:
            matched_indices.append(-1)
    print 'N matched: {}'.format(len(matched_indices)-matched_indices.count(-1))
    return matched_indices

def binary_search_index(a, x):
    """Binary searches array a for element x and returns index"""
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    return -1
