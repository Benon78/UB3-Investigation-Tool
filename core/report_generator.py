from datetime import datetime
import pandas as pd


def build_executive_report(session):

    report = f"""
        WASSHA UB3 EXECUTIVE REPORT
        Generated: {datetime.now():%Y-%m-%d %H:%M:%S}
        ========================================

        CUSTOMER SUMMARY
        UB3 Found: {session.ub3_count}
        Records Analyzed: {session.record_count}
        Lantern Activities: {len(session.lanterns)}
        Current Balance: {session.balance_summary.get("current", 0)}
        ========================================

        RISK ASSESSMENT
        Risk Score: {session.risk_score}
        Risk Level: {session.risk_level}
        Flags Detected: {len(session.flags)}
        ========================================

        TOP FLAGS

        """

    if session.flags:

        for flag in session.flags:
            report += f"• {flag}\n"

    else:

        report += "No suspicious activity detected.\n"

    return report


def build_fraud_report(session):

    report = f"""
        WASSHA FRAUD INVESTIGATION REPORT
        ========================================

        Risk Score: {session.risk_score}
        Risk Level: {session.risk_level}
        ========================================

        Suspicious Lanterns

        """

    if session.suspicious_lanterns:

        for lantern in session.suspicious_lanterns:
            report += f"• {lantern}\n"

    else:

        report += "No suspicious lanterns detected.\n"

    report += "\n\nFlags\n\n"

    if session.flags:

        for flag in session.flags:
            report += f"• {flag}\n"

    else:

        report += "No flags detected.\n"

    return report


def build_timeline_report(session):

    report = f"""
        WASSHA TIMELINE REPORT
        ========================================

        Total Records: {session.record_count}
        Total Operations: {len(session.operation_counts)}
        ========================================

        Operation Summary

        """

    sorted_ops = sorted(
        session.operation_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )

    for operation, count in sorted_ops:

        report += f"{operation}: {count}\n"

    return report

def build_preview(session):

    return f"""
        WASSHA UB3 ANALYZER REPORT PREVIEW
        =====================================

        UB3 Devices: {session.ub3_count}
        Records: {session.record_count}
        Risk Score: {session.risk_score}
        Risk Level: {session.risk_level}
        Flags: {len(session.flags)}
        Suspicious Lanterns: {len(session.suspicious_lanterns)}

        Current Balance:
        {session.balance_summary.get("current", 0)}
        =====================================

        Top Flags:
         {chr(10).join(session.flags[:10])}
        =====================================

        Verdict
        {session.verdict}
        """