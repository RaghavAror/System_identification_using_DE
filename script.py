import numpy as np
import pandas as pd
from scipy.optimize import differential_evolution, minimize
import math
import matplotlib.pyplot as plt


fn = "xy_data.csv"   
df = pd.read_csv(fn)
x_data = df['x'].values
y_data = df['y'].values

#assume rows are ordered and uniformly sampled from t=6 to t=60
t_data = np.linspace(6.0, 60.0, len(df))

def model_xy(params, t):

    theta_deg, M, X = params
    theta = theta_deg * np.pi / 180.0
    s03t = np.sin(0.3 * t)
    abs_t = np.abs(t)
    exp_term = np.exp(M * abs_t)
    x = t * np.cos(theta) - exp_term * s03t * np.sin(theta) + X
    y = 42.0 + t * np.sin(theta) + exp_term * s03t * np.cos(theta)
    return x, y

#objective functions

def residuals(params, t, x_obs, y_obs):
    x_pred, y_pred = model_xy(params, t)
    dx = x_pred - x_obs
    dy = y_pred - y_obs
    return np.concatenate([dx, dy])

def objective_L1(params, t, x_obs, y_obs):
    x_pred, y_pred = model_xy(params, t)
    return np.sum(np.abs(x_pred - x_obs) + np.abs(y_pred - y_obs))

def objective_L2(params, t, x_obs, y_obs):
    x_pred, y_pred = model_xy(params, t)
    return np.sum((x_pred - x_obs)**2 + (y_pred - y_obs)**2)


bounds = [(1e-6, 50.0 - 1e-6),  # theta in degrees
          (-0.05 + 1e-8, 0.05 - 1e-8),  # M
          (1e-6, 100.0 - 1e-6)]  # X

#optimization using Differential Evolution
seed = 42
result_de = differential_evolution(
    lambda params: objective_L1(params, t_data, x_data, y_data),
    bounds=bounds,
    strategy='best1bin',
    maxiter=400,
    popsize=15,
    tol=1e-6,
    seed=seed,
    polish=False,
    updating='deferred'
)

print("DE result:", result_de.x, "obj(L1)=", result_de.fun)

#Local refinement using L2
x0 = result_de.x
res_local = minimize(
    lambda p: objective_L2(p, t_data, x_data, y_data),
    x0,
    method='L-BFGS-B',
    bounds=bounds,
    options={'maxiter':10000}
)
print("Local refine (L2) result:", res_local.x, "obj(L2)=", res_local.fun)

#Local refinement using L1
x_init = res_local.x
x_init = np.clip(x_init, [b[0] for b in bounds], [b[1] for b in bounds])

res_nm = minimize(
    lambda p: objective_L1(p, t_data, x_data, y_data),
    x_init,
    method='Nelder-Mead',
    options={'maxiter':20000, 'xatol':1e-8, 'fatol':1e-8}
)


best_params = res_nm.x
best_params = np.clip(best_params, [b[0] for b in bounds], [b[1] for b in bounds])
print("Final params (after Nelder-Mead):", best_params)
print("Final L1:", objective_L1(best_params, t_data, x_data, y_data))
print("Final L2:", objective_L2(best_params, t_data, x_data, y_data))

#Evaluation and plotting
x_pred, y_pred = model_xy(best_params, t_data)

# L1 per point average
l1_total = np.sum(np.abs(x_pred - x_data) + np.abs(y_pred - y_data))
l1_avg = l1_total / len(t_data)
print(f"L1 total = {l1_total:.6f}, L1 avg per point = {l1_avg:.6f}")


plt.figure(figsize=(8,6))
plt.scatter(x_data, y_data, label='observed', s=20)
plt.scatter(x_pred, y_pred, label='predicted', s=20, marker='x')
plt.legend()
plt.title("Observed vs Predicted")
plt.xlabel("x")
plt.ylabel("y")
plt.axis('equal')
plt.show()


theta_deg, M_val, X_val = best_params
submission = (f"(t*cos({theta_deg:.6f}) - exp({M_val:.6f}*abs(t))*sin(0.3*t)*sin({theta_deg:.6f}) + {X_val:.6f}, "
              f"42 + t*sin({theta_deg:.6f}) + exp({M_val:.6f}*abs(t))*sin(0.3*t)*cos({theta_deg:.6f}))")
print("\nSubmission string (example):\n", submission)
latex = (r"\left(t\cos(" + f"{theta_deg:.6f}" + r") - e^{" + f"{M_val:.6f}" + r"|t|}\sin(0.3t)\sin(" + f"{theta_deg:.6f}" + r") + " + f"{X_val:.6f}" + r",\; 42 + t\sin(" + f"{theta_deg:.6f}" + r") + e^{" + f"{M_val:.6f}" + r"|t|}\sin(0.3t)\cos(" + f"{theta_deg:.6f}" + r")\right)")
print("\nLaTeX (approx):\n", latex)
