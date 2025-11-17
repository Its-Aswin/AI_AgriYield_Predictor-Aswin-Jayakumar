Project Overview

AgriYield Predictor is a machine learning project designed to predict crop yields based on agricultural factors such as soil nutrients (N, P, K), environmental conditions (temperature, humidity, rainfall, pH), crop type, and fertilizer usage. The workflow includes data preprocessing, exploratory data analysis (EDA), feature engineering, model training, evaluation, and optimization for deployment.

1. Setup and Prerequisites

The project utilizes Python and several data science libraries.

    Libraries Used: pandas, numpy, matplotlib, seaborn, sklearn, xgboost, joblib, json.

    Input: The script runs as a sequential process, originally converted from a Jupyter Notebook.

2. Data Loading and Inspection

The project initializes by loading the dataset directly from a remote source.

    Source: Hugging Face Datasets (Jakehills/Crop_Yield_Fertilizer).

    Action: The CSV is loaded into a Pandas DataFrame.

    Inspection Steps:

        df.head(): Displays the first 5 rows to understand the structure.

        df.info(): Checks data types and verifies non-null counts.

        df.describe(): Provides statistical summaries (mean, std, min, max) for numerical columns.

3. Data Cleaning and Preprocessing

This stage ensures the data is ready for analysis.

    Null Value Check: The script checks for missing values using .isnull().sum(). (Result: No missing values found).

    Consistency Check: Prints unique values for categorical columns (label, fertilizer) to identify potential naming inconsistencies.

    Outlier Detection: Box plots are generated for all numerical columns (N, P, K, temperature, etc.) to visually identify outliers.

4. Exploratory Data Analysis (EDA)

Visualizations are generated to understand relationships between variables.

    Distributions: Histograms with Kernel Density Estimates (KDE) show how data points are distributed across different ranges.

    Correlation Analysis: A Heatmap displays the correlation matrix, highlighting how different numerical features relate to each other and the target variable (yield).

    Yield Relationships: Scatter plots visualize the direct relationship between key nutrients/rainfall and the crop yield.

    Categorical Analysis: Count plots display the frequency distribution of different crops (label) and fertilizers.

5. Feature Engineering

Raw data is transformed to improve model performance.

    One-Hot Encoding:

        Categorical columns label (Crop Type) and fertilizer are converted into numerical binary columns using pd.get_dummies.

        drop_first=True is used to prevent multicollinearity (dummy variable trap).

    Interaction Features: New features are created to capture relationships between soil/environmental factors:

        N_temp: Nitrogen × Temperature

        P_humidity: Phosphorus × Humidity

        K_rainfall: Potassium × Rainfall

6. Data Splitting

The dataset is divided to prepare for training.

    Features (X): All columns except yield.

    Target (y): The yield column.

    Split Ratio: 80% Training data, 20% Testing data.

    Random State: Set to 42 for reproducibility.

7. Model Training (Baseline)

Three different regression algorithms are trained to establish a baseline performance.

    Random Forest Regressor: An ensemble method using multiple decision trees.

    XGBoost Regressor: A gradient boosting framework known for speed and performance.

    Linear Regression: A simple approach assuming a linear relationship between features and target.

8. Model Evaluation

Each model is evaluated on the Test set using standard regression metrics:

    MAE (Mean Absolute Error): Average magnitude of errors.

    MSE (Mean Squared Error): Average squared difference between estimated values and the actual value.

    RMSE (Root Mean Squared Error): Square root of MSE; represents error in the same units as the target.

    R² Score: Indicates the proportion of variance in the dependent variable predictable from the independent variables.

Result: The Random Forest model is identified as the best performer based on Feature Importance analysis.

9. Feature Importance Analysis

The script extracts and visualizes which features contribute most to the Random Forest model's predictions.

    A bar chart displays the Top 10 most influential features.

10. Model Artifacts & Metadata generation

Preparation for deployment or external usage.

    Metadata Extraction: A JSON object is constructed containing:

        Model type (Regressor vs Classifier).

        Library versions.

        Input feature names and data types.

        Hyperparameters (n_estimators, max_depth).

    Serialization: The metadata is saved to model_metadata.json and the heavy model is saved to random_forest_model.pkl.

11. Model Optimization (Size Reduction)

To optimize the model for storage or deployment (likely to reduce file size), the Random Forest model is retrained with constrained hyperparameters.

    Configuration:

        n_estimators: Reduced to 50.

        max_depth: Capped at 20.

    Evaluation: The reduced model is re-evaluated against the test set to ensure performance remains acceptable despite the complexity reduction.

    Saving: The optimized model is saved as random_forest_model_reduced.pkl.

    Size Check: The script calculates and prints the file size (in MB) of the optimized model.

12. User Inference Interface

The script concludes with an interactive Command Line Interface (CLI) for manual testing.

    User Input Collection:

        Prompts the user for numerical inputs (N, P, K, pH, etc.).

        Prompts for categorical inputs (Crop Type, Fertilizer).

    Input Validation: Checks if the entered crop/fertilizer exists in the original dataset.

    Preprocessing Pipeline:

        Matches user input to the One-Hot Encoded feature structure used during training.

        Calculates the required Interaction Features (N_temp, etc.) on the fly.

    Prediction: Uses the Reduced Random Forest Model to predict the yield based on the user's input.

13. Web Interface (UI) 

The project features a web-based user interface built with Django, a high-level Python web framework. This UI allows users to interact with the predictive model without needing to write code, providing a user-friendly form to input agricultural data and receive yield predictions.

Technology Stack

    Backend Framework: Django 

    Frontend: HTML5, CSS3 (Internal styling)

    Data Processing: Pandas (for structuring input data)

    Model Integration: Joblib (for loading the serialized model)

14. Deployment

The predictive model is deployed as a live Django web application on Render.

    Live URL: https://agriyield-2-0.onrender.com/

    Infrastructure: The app runs on Gunicorn, using WhiteNoise to serve static assets efficiently in a production environment.

    Configuration: Secured for production with DEBUG=False and strict host settings. Application entry is managed via a Procfile.

    Model Serving: The optimized random_forest_model_reduced.pkl is loaded into memory at startup, allowing for real-time low-latency predictions based on user input.

    CI/CD Pipeline: Deployment is automated via GitHub. Git LFS (Large File Storage) was utilized to handle the model file, ensuring seamless updates whenever code is pushed to the repository.