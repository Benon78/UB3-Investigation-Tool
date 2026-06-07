import re

# Excel forbidden characters
ILLEGAL_CHARACTERS_RE = re.compile(
    r'[\x00-\x08\x0B\x0C\x0E-\x1F]'
)


def clean_value(value):

    if value is None:
        return ""

    text = str(value)

    text = ILLEGAL_CHARACTERS_RE.sub("", text)

    # remove non-printable characters
    text = "".join(
        ch for ch in text
        if ch.isprintable()
    )

    return text


# def clean_dataframe(df):
#     """
#     Apply cleaning to full dataframe
#     """
#     return df.map(clean_value)