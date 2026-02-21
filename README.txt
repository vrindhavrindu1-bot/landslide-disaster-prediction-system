Project: Landslide Risk Prediction Model

Description:
This model predicts landslide risk level using rainfall, slope, soil type, crack observation, and soil flow.

Input Feature Order:

1.rainfall_level (0 = Low, 1 = Medium, 2 = High)

2.slope_type (0 = Flat, 1 = Moderate, 2 = Steep)

3.soil_type (0 = Stable/Rocky soil,1 = Moderately stable soil, 2 = Loose/unstable soil)

4.crack_obs (0 = No, 1 = Yes, 2 = Severe if used)

5.soil_flow (0 = No, 1 = Yes, 2 = Heavy if used)

Output:
0 = Low Risk
1 = Medium Risk
2 = High Risk

Model File: landslide_model.pkl
Language: Python
Library: scikit-learn