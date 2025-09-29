#!/usr/bin/env python
from __future__ import annotations
import argparse, sys, os
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest


def load_file(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        print(f"Error: File '{path}' not found.")
        sys.exit(1)
    ext = path.split('.')[-1].lower()
    try:
        if ext == 'csv':
            return pd.read_csv(path)
        if ext in ['xls', 'xlsx']:
            return pd.read_excel(path)
        if ext == 'json':
            return pd.read_json(path)
        print(f"Unsupported file type: {ext}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def detect_missing(df: pd.DataFrame):
    return df.isna().sum()


def detect_duplicates(df: pd.DataFrame) -> int:
    return df.duplicated().sum()


def summary_stats(df: pd.DataFrame) -> dict:
    summary: dict = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            summary[col] = {
                'mean': df[col].mean(), 'median': df[col].median(),
                'min': df[col].min(), 'max': df[col].max(), 'std': df[col].std(),
                'missing': df[col].isna().sum(), 'unique': df[col].nunique()
            }
        else:
            mode_series = df[col].mode()
            summary[col] = {
                'missing': df[col].isna().sum(), 'unique': df[col].nunique(),
                'top': mode_series.iloc[0] if not mode_series.empty else None
            }
    return summary


def detect_anomalies_zscore(df: pd.DataFrame, threshold: float = 3) -> int:
    num_cols = df.select_dtypes(include=np.number).columns
    anomalies = pd.DataFrame(index=df.index)
    for col in num_cols:
        std = df[col].std()
        if std == 0 or pd.isna(std):
            continue
        zscores = (df[col] - df[col].mean()) / std
        anomalies[col + '_anomaly'] = zscores.abs() > threshold
    return int(anomalies.sum(axis=1).sum())


def detect_anomalies_ml(df: pd.DataFrame) -> int:
    num_cols = df.select_dtypes(include=np.number)
    if num_cols.empty:
        return 0
    clf = IsolationForest(contamination=0.05, random_state=42)
    filled = num_cols.fillna(num_cols.mean())
    clf.fit(filled)
    preds = clf.predict(filled)
    return int((preds == -1).sum())


def suggest_cleaning(df: pd.DataFrame) -> list[str]:
    suggestions: list[str] = []
    for col in df.columns:
        missing = df[col].isna().sum()
        if missing > 0:
            if pd.api.types.is_numeric_dtype(df[col]):
                suggestions.append(f"Fill missing numeric '{col}' with mean/median")
            else:
                suggestions.append(f"Fill missing categorical '{col}' with mode")
    if df.duplicated().sum() > 0:
        suggestions.append("Drop duplicate rows")
    return suggestions


def apply_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in df.columns:
        if df[col].isna().sum() > 0:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].mean())
            else:
                mode_series = df[col].mode()
                if not mode_series.empty:
                    df[col] = df[col].fillna(mode_series.iloc[0])
    if df.duplicated().sum() > 0:
        df = df.drop_duplicates()
    return df


def print_summary(summary: dict) -> None:
    for col, stats in summary.items():
        print(f"Column: {col}")
        for k, v in stats.items():
            print(f"  {k}: {v}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='DataSanity: Auto Data Crisis Fixer CLI')
    parser.add_argument('--file', required=True, help='Path to CSV/JSON/Excel file')
    parser.add_argument('--output', help='Path to save cleaned file')
    parser.add_argument('--ml', action='store_true', help='Enable ML anomaly detection (requires scikit-learn)')
    parser.add_argument('--threshold', type=float, default=3.0, help='Z-score threshold for anomalies')
    args = parser.parse_args(argv)

    df = load_file(args.file)

    print("\n=== Missing Values ===")
    missing = detect_missing(df)
    print(missing)

    print("\n=== Duplicate Rows ===")
    dup_count = detect_duplicates(df)
    print(f"Total duplicate rows: {dup_count}")

    print("\n=== Summary Statistics ===")
    summary = summary_stats(df)
    print_summary(summary)

    print("\n=== Anomalies Detected ===")
    z_anomalies = detect_anomalies_zscore(df, args.threshold)
    print(f"Numeric anomalies (z-score>{args.threshold}): {z_anomalies}")
    if args.ml:
        ml_anomalies = detect_anomalies_ml(df)
        print(f"ML-based anomalies: {ml_anomalies}")

    print("\n=== Cleaning Suggestions ===")
    suggestions = suggest_cleaning(df)
    for s in suggestions:
        print(f"- {s}")

    if args.output:
        df_clean = apply_cleaning(df)
        try:
            ext = args.output.split('.')[-1].lower()
            if ext == 'csv':
                df_clean.to_csv(args.output, index=False)
            elif ext in ['xls', 'xlsx']:
                df_clean.to_excel(args.output, index=False)
            elif ext == 'json':
                df_clean.to_json(args.output, orient='records')
            else:
                print(f"Unsupported output type: {ext}")
            print(f"Cleaned data saved to {args.output}")
        except Exception as e:
            print(f"Error saving cleaned file: {e}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
