import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ============================================================
# STUDENT PERFORMANCE AI
# MODEL TRAINING
# ============================================================

DATA_PATH = "data/student-por.csv"
MODEL_PATH = "student_performance_model.pkl"


print("=" * 60)
print("       STUDENT PERFORMANCE AI - MODEL TRAINING")
print("=" * 60)


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(DATA_PATH, sep=";")

print("\nDataset loaded successfully.")
print(f"Students: {len(df)}")
print(f"Columns: {len(df.columns)}")


# ============================================================
# EARLY-PREDICTION FEATURES
# ============================================================
#
# G1 and G2 are deliberately excluded.
#
# These features are available before the final grade.
#
# We use several meaningful student characteristics rather
# than relying only on studytime and absences.
# ============================================================

features = [
    "school",
    "sex",
    "age",
    "address",
    "famsize",
    "Pstatus",
    "Medu",
    "Fedu",
    "Mjob",
    "Fjob",
    "reason",
    "guardian",
    "traveltime",
    "studytime",
    "failures",
    "schoolsup",
    "famsup",
    "paid",
    "activities",
    "nursery",
    "higher",
    "internet",
    "romantic",
    "famrel",
    "freetime",
    "goout",
    "Dalc",
    "Walc",
    "health",
    "absences"
]

target = "G3"


# ============================================================
# CHECK DATA
# ============================================================

missing_columns = [
    column for column in features + [target]
    if column not in df.columns
]

if missing_columns:
    print("\nERROR!")
    print("The following required columns are missing:")
    print(missing_columns)
    print("\nAvailable columns:")
    print(df.columns.tolist())
    raise SystemExit


# ============================================================
# REMOVE INVALID TARGET ROWS
# ============================================================

df = df.dropna(subset=[target])

X = df[features].copy()
y = df[target].astype(float)


# ============================================================
# FEATURE TYPES
# ============================================================

categorical_features = [
    "school",
    "sex",
    "address",
    "famsize",
    "Pstatus",
    "Mjob",
    "Fjob",
    "reason",
    "guardian",
    "schoolsup",
    "famsup",
    "paid",
    "activities",
    "nursery",
    "higher",
    "internet",
    "romantic"
]

numerical_features = [
    "age",
    "Medu",
    "Fedu",
    "traveltime",
    "studytime",
    "failures",
    "famrel",
    "freetime",
    "goout",
    "Dalc",
    "Walc",
    "health",
    "absences"
]


# ============================================================
# PREPROCESSING
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            ),
            categorical_features
        ),
        (
            "numerical",
            StandardScaler(),
            numerical_features
        )
    ]
)


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


# ============================================================
# MODELS TO COMPARE
# ============================================================

models = {

    "Random Forest": RandomForestRegressor(
        n_estimators=500,
        max_depth=None,
        min_samples_split=4,
        min_samples_leaf=2,
        max_features="sqrt",
        random_state=42,
        n_jobs=-1
    ),

    "Extra Trees": ExtraTreesRegressor(
        n_estimators=500,
        max_depth=None,
        min_samples_split=3,
        min_samples_leaf=1,
        max_features=0.8,
        random_state=42,
        n_jobs=-1
    ),

    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=300,
        learning_rate=0.03,
        max_depth=3,
        min_samples_leaf=4,
        loss="huber",
        random_state=42
    )
}


# ============================================================
# TRAIN AND COMPARE
# ============================================================

results = {}

print("\nTraining and comparing models...")
print("-" * 60)


for name, estimator in models.items():

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", estimator)
        ]
    )

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    rmse = np.sqrt(
        mean_squared_error(y_test, predictions)
    )

    r2 = r2_score(y_test, predictions)

    results[name] = {
        "pipeline": pipeline,
        "mae": mae,
        "rmse": rmse,
        "r2": r2
    }

    print(f"\n{name}")
    print(f"MAE  : {mae:.3f}")
    print(f"RMSE : {rmse:.3f}")
    print(f"R²   : {r2:.3f}")


# ============================================================
# SELECT BEST MODEL
# ============================================================
#
# Lower MAE is better.
# ============================================================

best_model_name = min(
    results,
    key=lambda name: results[name]["mae"]
)

best_pipeline = results[best_model_name]["pipeline"]


# ============================================================
# CROSS-VALIDATION
# ============================================================

print("\n" + "-" * 60)
print("Running 5-fold cross-validation...")

cv_scores = cross_val_score(
    best_pipeline,
    X,
    y,
    cv=5,
    scoring="neg_mean_absolute_error"
)

cv_mae = -cv_scores.mean()


# ============================================================
# SAVE MODEL
# ============================================================

model_information = {

    "model": best_pipeline,

    "features": features,

    "target": target,

    "model_name": best_model_name,

    "test_mae": results[best_model_name]["mae"],

    "test_rmse": results[best_model_name]["rmse"],

    "test_r2": results[best_model_name]["r2"],

    "cv_mae": cv_mae,

    "grade_min": 0,

    "grade_max": 20

}


joblib.dump(
    model_information,
    MODEL_PATH
)


# ============================================================
# FINAL REPORT
# ============================================================

print("\n" + "=" * 60)
print("TRAINING COMPLETE")
print("=" * 60)

print(f"\nBest model: {best_model_name}")

print(
    f"Test MAE: "
    f"{results[best_model_name]['mae']:.3f}"
)

print(
    f"Test RMSE: "
    f"{results[best_model_name]['rmse']:.3f}"
)

print(
    f"Test R²: "
    f"{results[best_model_name]['r2']:.3f}"
)

print(
    f"5-Fold CV MAE: "
    f"{cv_mae:.3f}"
)

print(f"\nSaved model: {MODEL_PATH}")

print("\nG1 and G2 were NOT used.")
print("Final grade G3 is the prediction target.")

print("\nYou can now run:")
print("streamlit run app.py")