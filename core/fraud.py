def calculate_risk(df):

    score = 0
    flags = []

    ops = df["Operation"].value_counts()

    if ops.get("UL.Fail", 0) > 5:
        score += 20
        flags.append(
            "High Unlock Failure Rate"
        )

    if ops.get("P.Fail", 0) > 10:
        score += 20
        flags.append(
            "Passcode Abuse"
        )

    if ops.get("F.Reboot", 0) > 10:
        score += 20
        flags.append(
            "Abnormal Reboots"
        )

    return score, flags