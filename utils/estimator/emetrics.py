import numpy as np
from math import sqrt


def get_cindex(Y, P):
    summ = 0
    pair = 0

    for i in range(1, len(Y)):
        for j in range(0, i):
            if i is not j:
                if Y[i] > Y[j]:
                    pair += 1
                    summ += 1 * (P[i] > P[j]) + 0.5 * (P[i] == P[j])

    if pair is not 0:
        return summ / pair
    else:
        return 0


def r_squared_error(y_obs, y_pred):
    y_obs = np.array(y_obs)
    y_pred = np.array(y_pred)
    y_obs_mean = [np.mean(y_obs) for y in y_obs]
    y_pred_mean = [np.mean(y_pred) for y in y_pred]

    mult = sum((y_pred - y_pred_mean) * (y_obs - y_obs_mean))
    mult = mult * mult

    y_obs_sq = sum((y_obs - y_obs_mean) * (y_obs - y_obs_mean))
    y_pred_sq = sum((y_pred - y_pred_mean) * (y_pred - y_pred_mean))

    return mult / float(y_obs_sq * y_pred_sq)


def get_k(y_obs, y_pred):
    y_obs = np.array(y_obs)
    y_pred = np.array(y_pred)

    return sum(y_obs * y_pred) / float(sum(y_pred * y_pred))


def squared_error_zero(y_obs, y_pred):
    k = get_k(y_obs, y_pred)

    y_obs = np.array(y_obs)
    y_pred = np.array(y_pred)
    y_obs_mean = [np.mean(y_obs) for y in y_obs]
    upp = sum((y_obs - (k * y_pred)) * (y_obs - (k * y_pred)))
    down = sum((y_obs - y_obs_mean) * (y_obs - y_obs_mean))

    return 1 - (upp / float(down))


def get_rm2(ys_orig, ys_line):
    r2 = r_squared_error(ys_orig, ys_line)
    r02 = squared_error_zero(ys_orig, ys_line)

    return r2 * (1 - np.sqrt(np.absolute((r2 * r2) - (r02 * r02))))


def get_rmse(y, f):
    rmse = sqrt(((y - f) ** 2).mean(axis=0))
    return rmse


def get_mse(y, f):
    mse = ((y - f) ** 2).mean(axis=0)
    return mse


def get_pearson(y, f):
    rp = np.corrcoef(y, f)[0, 1]
    return rp


# def get_spearman(y, f):
#     rs = stats.spearmanr(y, f)[0]
#     return rs


def get_ci(y, f):
    ind = np.argsort(y)
    y = y[ind]
    f = f[ind]
    i = len(y) - 1
    j = i - 1
    z = 0.0
    S = 0.0
    while i > 0:
        while j >= 0:
            if y[i] > y[j]:
                z = z + 1
                u = f[i] - f[j]
                if u > 0:
                    S = S + 1
                elif u == 0:
                    S = S + 0.5
            j = j - 1
        i = i - 1
        j = i - 1
    ci = S / z
    return ci

def get_ci_torch(y, f):
    # 对 y 进行排序
    ind = torch.argsort(y)
    y = y[ind]
    f = f[ind]

    # 初始化变量
    i = len(y) - 1
    j = i - 1
    z = torch.tensor(0.0, dtype=torch.float32)
    S = torch.tensor(0.0, dtype=torch.float32)

    # 循环计算 CI
    while i > 0:
        while j >= 0:
            if y[i] > y[j]:
                z = z + 1
                u = f[i] - f[j]
                if u > 0:
                    S = S + 1
                elif u == 0:
                    S = S + 0.5
            j = j - 1
        i = i - 1
        j = i - 1

        # 计算 CI 并返回结果
    ci = S / z
    return ci.item()  # 将 tensor 转换为 Python 浮点数

def regression_scores(label, pred):
    label = np.array(label)
    pred = np.array(pred)

    ci = get_ci(label, pred)
    mse = get_mse(label, pred)
    pcc = get_pearson(label, pred)
    rm2 = get_rm2(label, pred)

    return {'ci': ci, 'mse': mse, 'pcc': pcc, 'rm2': rm2}


if __name__ == '__main__':
    preds = np.array([0, 0, 1, 1, 0, 1])
    target = np.array([0, 1, 1, 0, 0, 1])
    score = np.array([0.11, 0.22, 0.84, 0.73, 0.33, 0.92])
    d_array = regression_scores(target, score)
    print(d_array)
