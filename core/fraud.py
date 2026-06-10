import pandas as pd


def calculate_risk(df):

    score = 0
    flags = []

    if "Operation" not in df.columns:
        return 0, [], {}, {}, [], None, ""

    ops = df["Operation"].value_counts()

    operation_counts = {
        operation: int(count)
        for operation, count in ops.items()
    }

    ul_fail = ops.get("UL.Fail", 0)
    p_fail = ops.get("P.Fail", 0)
    reboot = ops.get("F.Reboot", 0)
    airwatt_short = ops.get("UL.Airwatt short", 0)
    already_unlocked = ops.get("AL.Unlocked", 0)

    # ==========================
    # Risk Matrix
    # ==========================

    risk_matrix = {}

    risk_matrix["Unlock Failures"] = ul_fail
    risk_matrix["Passcode Failures"] = p_fail
    risk_matrix["Reboots"] = reboot
    risk_matrix["Low Balance Attempts"] = airwatt_short
    risk_matrix["Already Unlocked"] = already_unlocked

    # ==========================
    # Risk Scoring
    # ==========================

    if ul_fail >= 5:
        score += 20
        flags.append(
            f"High Unlock Failure Rate ({ul_fail})"
        )

    if p_fail >= 10:
        score += 20
        flags.append(
            f"Passcode Abuse ({p_fail})"
        )

    if reboot >= 5:
        score += 15
        flags.append(
            f"Abnormal Reboots ({reboot})"
        )

    if airwatt_short >= 10:
        score += 10
        flags.append(
            f"Repeated Low Balance Attempts ({airwatt_short})"
        )

    if already_unlocked >= 10:
        score += 10
        flags.append(
            f"Repeated Unlock Attempts ({already_unlocked})"
        )

    if ul_fail >= 5 and reboot >= 5:
        score += 15
        flags.append(
            "Unlock Failure + Reboot Pattern"
        )

    # ==========================
    # Suspicious Lanterns
    # ==========================

    valid_models = (
        "AF80",
        "AC20",
        "AC40",
        "AC10",
        "A100",
        "B100",
        "160A"
    )

    suspicious_ops = [
        "UL.Fail",
        "P.Fail",
        "F.Reboot",
        "UL.Airwatt short",
        "AL.Unlocked"
    ]

    suspicious_df = df[
        df["Operation"].isin(
            suspicious_ops
        )
    ]

    suspicious_lanterns = []

    if "S/N" in suspicious_df.columns:

        lantern_df = suspicious_df[

            suspicious_df["S/N"]
            .fillna("")
            .astype(str)
            .str.upper()
            .str.strip()
            .str.endswith(
                valid_models,
                na=False
            )
        ]

        suspicious_lanterns = (
            lantern_df["S/N"]
            .astype(str)
            .value_counts()
            .head(20)
            .index
            .tolist()
        )

    # ==========================
    # Suspicious Events
    # ==========================

    suspicious_events = suspicious_df.copy()

    # ==========================
    # Verdict
    # ==========================

    if score < 20:

        verdict = (
            "LOW RISK. No major fraud indicators detected."
        )

    elif score < 50:

        verdict = (
            "MEDIUM RISK. Some abnormal activity requires review."
        )

    elif score < 80:

        verdict = (
            "HIGH RISK. Multiple fraud indicators detected."
        )

    else:

        verdict = (
            "CRITICAL RISK. Immediate investigation recommended."
        )

    return (
        score,
        flags,
        operation_counts,
        risk_matrix,
        suspicious_lanterns,
        suspicious_events,
        verdict
    )