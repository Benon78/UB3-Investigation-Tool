import pandas as pd


def operation_summary(df):

    operations = df["Operation"].value_counts()

    return operations.to_dict()


def balance_summary(df):

    balance = pd.to_numeric(
        df["Balance"],
        errors="coerce"
    )

    return {
        "current": balance.iloc[-1] if len(balance) else 0,
        "max": balance.max(),
        "min": balance.min(),
        "avg": round(balance.mean(), 2)
    }


def payment_summary(df):

    payment = pd.to_numeric(
        df["Payment"],
        errors="coerce"
    )

    return {
        "total": payment.sum(),
        "max": payment.max(),
        "avg": round(payment.mean(), 2)
    }