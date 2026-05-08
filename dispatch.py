import pandas as pd

def assign_ambulance(severity):
    df = pd.read_csv("data/ambulances.csv")

    df = df[df["availability"] == "Available"]

    if severity.startswith("🔴"):
        df = df[df["type"] == "ALS"]

    elif severity.startswith("🟠"):
        als_df = df[df["type"] == "ALS"]
        if not als_df.empty:
            df = als_df

    df = df.sort_values(by="eta_minutes")

    if df.empty:
        return "No ambulance available"

    return df.iloc[0].to_dict()


def suggest_hospital(severity):
    df = pd.read_csv("data/hospitals.csv")

    df = df[df["available_beds"] > 0]

    if df.empty:
        return "No hospital available"

    if severity.startswith("🔴"):
        preferred = df[df["specialization"].isin(["Trauma", "Emergency"])]
        if not preferred.empty:
            df = preferred

    elif severity.startswith("🟠"):
        preferred = df[df["specialization"].isin(["Emergency", "General"])]
        if not preferred.empty:
            df = preferred

    df["capacity_rank"] = df["capacity"].map({
        "High": 3,
        "Medium": 2,
        "Low": 1
    })

    df = df.sort_values(by=["capacity_rank", "available_beds"], ascending=False)

    return df.iloc[0].to_dict()