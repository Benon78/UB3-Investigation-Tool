def calculate_risk(df):

    score = 0
    flags = []

    if "Operation" not in df.columns:
        return 0, ["Operation column missing"]

    ops = df["Operation"].value_counts()

    ul_fail = ops.get("UL.Fail", 0)
    ensure_fail = ops.get("UL.Fail(ensure)", 0)
    p_fail = ops.get("P.Fail", 0)
    reboot = ops.get("F.Reboot", 0)
    airwatt_short = ops.get("UL.Airwatt short", 0)
    already_unlocked = ops.get("AL.Unlocked", 0)

    # Unlock failures
    if ul_fail >= 5:
        score += 20
        flags.append(
            f"High Unlock Failure Rate ({ul_fail})"
        )

    # Ensure process failures
    if ensure_fail >= 3:
        score += 15
        flags.append(
            f"Repeated Ensure Failures ({ensure_fail})"
        )

    # Passcode failures
    if p_fail >= 10:
        score += 20
        flags.append(
            f"Passcode Abuse ({p_fail})"
        )

    # Reboots
    if reboot >= 5:
        score += 15
        flags.append(
            f"Abnormal Reboots ({reboot})"
        )

    # Low balance unlock attempts
    if airwatt_short >= 10:
        score += 10
        flags.append(
            f"Repeated Low Balance Unlock Attempts ({airwatt_short})"
        )

    # Unlocking already unlocked lanterns
    if already_unlocked >= 10:
        score += 10
        flags.append(
            f"Repeated Unlock Attempts on Unlocked Lantern ({already_unlocked})"
        )

    # Combination rule
    if ul_fail >= 5 and reboot >= 5:
        score += 15
        flags.append(
            "Unlock Failures + Reboots Pattern"
        )

    # Combination rule
    if p_fail >= 10 and airwatt_short >= 10:
        score += 10
        flags.append(
            "Passcode Failure + Low Balance Pattern"
        )

    return score, flags