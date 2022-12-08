# 소개

- TTS(텍스트를 음성으로 변환) 서비스를 사용자에게 제공하고자 합니다.

# 설계

## 모델링

### ERD

<div align="center">
  <img src="doc/img/ai_park.png" alt="AI-PARK ERD" width="80%" height="80%">
</div>

### Audio

- field
    - id
    - index: 텍스트의 순서를 뜻함
    - update_time: 최신 업데이트 시간을 반영
    - text : 오디오로 변환될 텍스트
    - speed : 오디오의 스피드
    - project_id : 오디오를 내포한 프로젝트의 식별자

### Project

- field
    - id
    - title : 프로젝트의 이름
    - update_time
    - create_time

### FIle

- field
    - id
    - path
    - audio_id(fk)

## 기능 구현

- 프로젝트 생성(오디오 생성)
    1. 텍스트(str)가 담긴 리스트를 받습니다. (length = 1)
    2. 이를 전처리하여 오디오를 생성하는 함수의 input으로 같이 넣습니다. [['text1', 'text2', 'text3', ....], path]
    3. 일정시간 이후 함수에서 (id, text)형태의 원소를 가진 리스트를 리턴합니다. [('id1' ,'text1'), ('id2', 'text2'), ('id3', 'text3'), ....]
    4. 오디오는 input의 path에 저장됩니다.

## API

- `POST` **/api/tts/project**: 프로젝트 생성(오디오 생성)
    1. 텍스트(str)가 담긴 리스트를 받습니다. (length = 1)
    2. 이를 전처리하여 오디오를 생성하는 함수의 input으로 같이 넣습니다. [['text1', 'text2', 'text3', ....], path]
    3. 일정시간 이후 함수에서 (id, text)형태의 원소를 가진 리스트를 리턴합니다. [('id1' ,'text1'), ('id2', 'text2'), ('id3', 'text3'), ....]
    4. 오디오는 input의 path에 저장됩니다.

- `GET` **/api/tts/project/:id/index/:index**: 텍스트 조회
    - 특정 프로젝트의 n번째 페이지를 조회합니다.
    - 한페이지는 10문장으로 이루어져 있습니다.

- `PUT/PATCH` **/api/tts/audio/:id**: 텍스트 수정
    - 한 문장의 텍스트와 스피드를 수정합니다.

- `GET` **/api/tts/audio/:id**: 오디오파일 송신
    - 요청받은 오디오파일을 송신한다.

- `POST` **/api/tts/audio/:id**: 텍스트(오디오) 생성 / 삭제
    - 삽입위치는 항상 앞, 뒤가 아닌 중간도 가능

- `DELETE` **/api/tts/project/:id**: 프로젝트 삭제

# 기능 구현
## 1. Project 처음 만들 때
1. 우선 프로젝트 최초 실행 시 sentence field 를 입력 받는다.
2. 이를 전처리 하여 Audio Model 에 저장한다
   - 이 때 `celery` 를 통해 비동기 작업을 실행
   - file 저장 경로는 user의 아이디를 기반으로 UUID 를 생성하여 파일명을 짓는다.

# 개발 중 나온 ISSUE

## 1. 문단 전처리 과정

1. 유효성 검사.

    - 한글, 영어, 숫자, 물음표, 느낌표, 마침표, 따옴표, 공백를 제외한 나머지는 문장에 포함되지 않는다.

      ``` python
      import re 

      def get_validate_sentence(sentence) -> str:
          pattern = r'[^\w.!?\s\'\"]'
          return re.sub(pattern, '', sentence)
      ```

2. 구분자를 유지하기

    - 문단을 구분자(?|.|!)로 구분하여 한 문장씩으로 끊어야함
    - 이때 구분자는 끊어진 문장에 붙여야 함
    - 두 단계를 구분지어 로직을 수행하고자 함 첫 번째는 구분자로 `split()` 을 한다.

    - split 으로 반환 된 `list` 를 순회하며 구분자를 결합 시킨다.

      ```python
      import logging
      import re
      
      def sentence2texts(sentence: str) -> list:
          sep = ['?', '.', '!']
          pattern = f'([{"".join(sep)}])'
          li = re.split(pattern, sentence)
          result = []
          for idx, x in enumerate(li):
              if not x:  # 공백 문자 삭제
                  continue
   
              x = x.strip()  # 문장 앞 뒤로 공백 제거
              if x in sep:
                    try:
                        result[-1] = result[-1] + x  # 문장 끝에 구분자 ('?', '.', '!') 를 붙여줌
                        continue
                    except IndexError as ie:
                        logging.warning(ie)
                        pass
              result.append(x)
   
          return result
      ```

## 2. 프로젝트 생성

1. 프로젝트의 문장 처리
    1. 프로젝트 생성 시 첫 문장을 어떻게 받을 것인가?
        - serializer custom field 로 write -> audio 에 쓰도록 하고 read 는 audio 의 index 를 붙이는 걸로
    2. 오디오의 순서는 어떻게 처리 할 것인가?
        - 하나씩 다 밀어버릴 것인가?(V)
          - 중간에 넣는 다면 그 뒤에 index 에 +1 을 다함
    3. 프로젝트의 문장을 어떻게 보여줄 것인가?