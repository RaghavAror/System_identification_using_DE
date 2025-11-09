### Problem Statement ###

Find the values of unknown variables in the given parametric equation of a curve given the x,y pairs in xy_data.csv :

x=tcos(θ)−eM∣t∣sin(0.3t)sin(θ)+X
𝑦=42+𝑡sin(𝜃)+𝑒𝑀∣𝑡∣sin(0.3𝑡)cos(𝜃)

unknowns are θ, M, X.

Given range for unknown params is :
   1. 0deg<θdeg<50deg
   2. −0.05<M<0.05
   3. 0<X<100
      
parameter ‘t’ has range: 6<t<60

Estimate the optimal values of the unknown parameters θ, M, and X such that the parametric curve best fits the given dataset.
The quality of fit is evaluated using:  L1 distance between predicted curve and actual data points 

### Code/Methodology Explanation ###

1. Load data — the CSV contains columns x, y (t is assumed to be distributed uniformly between given range 6 to 60).

2. Implementing Function — implemented x(t;θ,M,X),y(t;θ,M,X). Converted θ from degrees to radians before using np.sin/np.cos.

3. Objective — minimized the difference between model and data. The approach utilized L1 distance for scoring to minimize sum of absolute residuals (or equivalently minimized L2 for stability then computed L1 for final score).

4. Global search + local refine — Since the model was nonlinear and had local minima, a global optimizer (differential evolution) was used within bounds, and then finally it was refined with scipy.optimize.minimize (L-BFGS-B).

5. Constraints and bounds: enforcing given ranges.

6. Evaluation: computed final L1 (sum |dx|+|dy|) over uniformly sampled t.

### Results ###
The final results are as follows:
1. Results from Differential Evolution:
   θ = 28.12 deg ;The curve is rotated by ~28 degrees.
   M = 0.0214 ;Controls the growth/decay factor of the exponential term. Since M>0, the amplitude of the oscillation grows slightly with |t|.
   X = 54.90 ;Horizontal shift of the curve.
   L1 error ≈ 37865.10

2. Results from Local Refinement (L2 objective):
   θ = 29.583 deg
   M = -0.05 (boundary value)
   X = 55.0136
   L2 error = 771686.89

3. Results from Final Refinement (L1 objective):
   θ = 28.11842 deg
   M = 0.021389
   X = 54.90101
   Final L1 = 37865.09
   Final L2 = 776780.75

4. Final metrics: (total data samples were 1501)
   Total fitness error: 37865.09
   Average error per data point: = 37865.09/1501 = 25.22 units

### Requirements ###
```
pip install scipy matplotlib pandas numpy
```

### How to Run ###

Simply open the terminal in the project directory and run:
```
python script.py
```
