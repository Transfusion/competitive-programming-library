def q_part(a, l, r):
    """https://onlinejudge.u-aizu.ac.jp/status/users/Transfusion/submissions/1/ALDS1_6_B/judge/6327096/Python3"""
    pivot = a[r]
    i = l - 1
    for j in range(l, r):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[r] = a[r], a[i + 1]
    return i + 1


def q_sort(a, l, r):
    """https://onlinejudge.u-aizu.ac.jp/status/users/Transfusion/submissions/1/ALDS1_6_C/judge/6327113/Python3"""
    if l < r:
        pvt_idx = q_part(a, l, r)
        q_sort(a, l, pvt_idx - 1)
        q_sort(a, pvt_idx + 1, r)
