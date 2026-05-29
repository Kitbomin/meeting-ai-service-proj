import re

# --------------------------------------------------
# 한국어 직책 패턴
# --------------------------------------------------

TITLE_PATTERN = r'([가-힣]{2,4})(님|과장님|교수님|대리님|팀장님|대표님|책임님|선임님)'


def extract_names(text: str):

    matches = re.findall(TITLE_PATTERN, text)

    result = []

    for match in matches:

        full_name = match[0] + match[1]

        result.append(full_name)

    return list(set(result))