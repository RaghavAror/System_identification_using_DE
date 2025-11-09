### Project Overview ###

This project processes and visualizes the given xy_data.
The script loads the data, performs interpolation, smoothing, and generates plots to help understand the patterns and trends.

* Code/Methodology Explanation *

1. Load data — the CSV contains columns x, y (t is assumed to be distributed uniformly between given range 6 to 60).

2. Implementing Function — implemented x(t;θ,M,X),y(t;θ,M,X). Converted θ from degrees to radians before using np.sin/np.cos.

3. Objective — minimized the difference between model and data. The approach utilized L1 distance for scoring to minimize sum of absolute residuals (or equivalently minimized L2 for stability then computed L1 for final score).

4. Global search + local refine — Since the model was nonlinear and had local minima, a global optimizer (differential evolution) was used within bounds, and then finally it was refined with scipy.optimize.minimize (L-BFGS-B).

5. Constraints and bounds: enforcing given ranges.

6. Evaluation: computed final L1 (sum |dx|+|dy|) over uniformly sampled t. 


* Requirements *
pip install scipy matplotlib pandas numpy

* How to Run *

Simply open the terminal in the project directory and run:
```
python script.py
```
