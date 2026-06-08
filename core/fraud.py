def calculate_risk(df):

    score = 0
    flags = []

    if "Operation" not in df.columns:
        return 0, [], {}

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

    return score, flags, operation_counts