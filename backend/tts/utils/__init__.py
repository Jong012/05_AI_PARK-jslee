# audio 파일의 형식은 mp3, wav 두가지입니다.
# 전처리과정
# '.', '!', '?' 로 문장이 구분됩니다.
# 빈 문장은 삭제됩니다.
# 한글, 영어, 숫자, 물음표, 느낌표, 마침표, 따옴표, 공백를 제외한 나머지는 문장에 포함되지
# 않습니다.
# 문장의 맨앞, 맨뒤에는 공백이 위치하지 않습니다.
# flask or fastapi를 이용합니다.
# 텍스트는 한 문장이 아니며 문장단위의 list를 input으로 넣어야합니다.
# 별도의 화면은 필요하지 않습니다.
# 결과는 JSON형식 입니다.(오디오 제외)
# RDB를 사용하고, 테이블 갯수의 제한은 없습니다.
# 구체적으로 명세되지 않은 부분은 임의의 인풋/아웃풋을 주석으로 남긴 후 자유롭게 개발하시면 됩
# 니다.
import logging

import re


def get_validate_sentence(sentence: str) -> str:
    """
    한글, 영어, 숫자, 물음표, 느낌표, 마침표, 따옴표, 공백를 제외한 나머지는 문장에 포함되지
    않도록 문장을 치환함
    :param sentence: 문단
    :return: 유효성 검사를 체크한 문단을 반환
    """
    pattern = r'[^\w.!?\s\'\"]'
    return re.sub(pattern, '', sentence)


def sentence2texts(sentence: str) -> list:
    """
    구분자('?', '.', '!')를 통해 문단을 한 문장씩 끊는 함수 생성
    :param sentence: 문단
    :return: 한 문장씩 끊은 list 를 반환
    """
    sep = ['?', '.', '!']
    pattern = f'([{"".join(sep)}])'
    li = re.split(pattern, sentence_)  # 먼저 구분자를 통해 문단을 문장으로 끊음. 이때 구분자는 문장 뒤쪽에 위치하게 됨
    result = []
    # HACK: 한 문장씩 끊고 뒤에 구분자를 결합하기 위한 로직
    for idx, x in enumerate(li):
        if not x:  # 공백 문자 삭제
            continue

        x = x.strip()  # 문장 앞 뒤로 공백 제거
        if x in sep:
            try:
                result[-1] = result[-1] + x  # 문장 끝에 구분자 ('?', '.', '!') 를 붙여줌
                continue
            except IndexError as ie:
                logging.warning(ie)  # 첫 문장이 구분자로 시작할 수도 있으므로 그냥 오류 로그만 내놓고 result 리스트에 포함시키기로 함
                pass
        result.append(x)

    return result
