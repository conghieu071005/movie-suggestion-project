import numpy as np 
import pandas as pd
from web.models import Myrating
import scipy.optimize 

def Myrecommend():
    # --- Các hàm con ---
    def normalizeRatings(myY, myR):
        Ymean = np.zeros((myY.shape[0], 1))
        Ynorm = np.zeros(myY.shape)
        for i in range(myY.shape[0]):
            idx = myR[i, :] == 1
            if np.sum(idx) > 0:
                Ymean[i] = np.mean(myY[i, idx])
                Ynorm[i, idx] = myY[i, idx] - Ymean[i]
        return Ynorm, Ymean

    def flattenParams(myX, myTheta):
        return np.concatenate((myX.flatten(), myTheta.flatten()))
    
    def reshapeParams(flattened_XandTheta, mynm, mynu, mynf):
        reX = flattened_XandTheta[:int(mynm*mynf)].reshape((mynm, mynf))
        reTheta = flattened_XandTheta[int(mynm*mynf):].reshape((mynu, mynf))
        return reX, reTheta

    def cofiCostFunc(myparams, myY, myR, mynu, mynm, mynf, mylambda=0.):
        myX, myTheta = reshapeParams(myparams, mynm, mynu, mynf)
        term1 = np.multiply(myX.dot(myTheta.T), myR)
        cost = 0.5 * np.sum(np.square(term1 - myY))
        cost += (mylambda/2.) * (np.sum(np.square(myTheta)) + np.sum(np.square(myX)))
        return cost

    def cofiGrad(myparams, myY, myR, mynu, mynm, mynf, mylambda=0.):
        myX, myTheta = reshapeParams(myparams, mynm, mynu, mynf)
        term1 = np.multiply(myX.dot(myTheta.T), myR) - myY
        Xgrad = term1.dot(myTheta) + mylambda * myX
        Thetagrad = term1.T.dot(myX) + mylambda * myTheta
        return flattenParams(Xgrad, Thetagrad)

    # --- Lấy dữ liệu từ database ---
    df = pd.DataFrame(list(Myrating.objects.all().values('user_id', 'movie_id', 'rating')))
    if df.empty:
        raise ValueError("⚠️ Không có dữ liệu rating trong database!")

    # 🔹 Gán lại chỉ số liên tục cho user và movie
    user_mapping = {uid: i for i, uid in enumerate(df['user_id'].unique())}
    movie_mapping = {mid: i for i, mid in enumerate(df['movie_id'].unique())}

    df['user_idx'] = df['user_id'].map(user_mapping)
    df['movie_idx'] = df['movie_id'].map(movie_mapping)

    mynu = len(user_mapping)   # số người dùng
    mynm = len(movie_mapping)  # số phim
    mynf = 10

    # --- Tạo ma trận rating ---
    Y = np.zeros((mynm, mynu))
    R = np.zeros((mynm, mynu))
    for row in df.itertuples():
        Y[row.movie_idx, row.user_idx] = row.rating
        R[row.movie_idx, row.user_idx] = 1

    # --- Chuẩn hóa dữ liệu ---
    Ynorm, Ymean = normalizeRatings(Y, R)

    # --- Tối ưu collaborative filtering ---
    X = np.random.rand(mynm, mynf)
    Theta = np.random.rand(mynu, mynf)
    myflat = flattenParams(X, Theta)
    mylambda = 10.0

    result = scipy.optimize.fmin_cg(
        cofiCostFunc,
        x0=myflat,
        fprime=cofiGrad,
        args=(Y, R, mynu, mynm, mynf, mylambda),
        maxiter=30,
        disp=False,
        full_output=True
    )

    resX, resTheta = reshapeParams(result[0], mynm, mynu, mynf)
    prediction_matrix = resX.dot(resTheta.T)

    # --- Trả kết quả ---
    return prediction_matrix, Ymean, user_mapping, movie_mapping
