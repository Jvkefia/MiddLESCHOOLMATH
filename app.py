from flask import Flask, render_template, request, jsonify
import random
import math
from collections import Counter

app = Flask(__name__)

# 중학교 수학 학기별 데이터
MATH_TOPICS = {
    'grade1-1': {
        'name': '중1-1',
        'description': '중학교 1학년 1학기 수학: 정수와 유리수, 문자와 식, 일차방정식, 좌표평면과 그래프',
        'lessons': [
            {
                'title': '1. 정수와 유리수',
                'content': '''정수와 유리수의 개념과 성질을 학습합니다.
                
• 정수: 양의 정수, 0, 음의 정수로 이루어진 수
  - 양의 정수: 1, 2, 3, ...
  - 음의 정수: -1, -2, -3, ...
  - 0은 양수도 음수도 아닌 정수

• 유리수: 두 정수 a, b(b≠0)에 대하여 a/b (분수)로 나타낼 수 있는 수
  - 정수는 유리수에 포함됨 (예: 3 = 3/1)
  - 유리수는 소수로 나타낼 수 있음 (유한소수 또는 순환소수)

• 수직선: 수를 직선 위의 점으로 나타낸 것
  - 원점(0)을 기준으로 오른쪽은 양수, 왼쪽은 음수
  - 절댓값: 수직선에서 원점으로부터의 거리 (항상 0 이상)
  
• 유리수의 대소 관계
  - 양수 > 0 > 음수
  - 두 양수 중 절댓값이 큰 수가 더 큼
  - 두 음수 중 절댓값이 작은 수가 더 큼'''
            },
            {
                'title': '2. 정수와 유리수의 사칙연산',
                'content': '''정수와 유리수의 덧셈, 뺄셈, 곱셈, 나눗셈을 학습합니다.

• 덧셈
  - 같은 부호: 절댓값의 합에 공통 부호
    예: (+3) + (+5) = +8, (-3) + (-5) = -8
  - 다른 부호: 절댓값의 차에 절댓값이 큰 수의 부호
    예: (+5) + (-3) = +2, (-5) + (+3) = -2

• 뺄셈: 빼는 수의 부호를 바꾸어 덧셈으로 계산
  예: (+5) - (+3) = (+5) + (-3) = +2
      (+5) - (-3) = (+5) + (+3) = +8

• 곱셈
  - 같은 부호: 양수 (예: (+3) × (+5) = +15, (-3) × (-5) = +15)
  - 다른 부호: 음수 (예: (+3) × (-5) = -15, (-3) × (+5) = -15)
  - 0과의 곱: 항상 0

• 나눗셈: 곱셈과 같은 부호 규칙 적용
  예: (+15) ÷ (+3) = +5, (-15) ÷ (-3) = +5
      (+15) ÷ (-3) = -5, (-15) ÷ (+3) = -5

• 분배법칙: a(b + c) = ab + ac, a(b - c) = ab - ac'''
            },
            {
                'title': '3. 문자와 식',
                'content': '''문자를 사용한 식의 표현과 계산을 학습합니다.

• 문자를 사용한 식
  - 수량을 문자로 나타내어 일반화
  - 예: 속력 v, 시간 t → 거리 = v × t

• 일차식: 차수가 1인 다항식
  - 예: 3x + 2, -2x + 5, 4x
  - 항: 수나 문자, 또는 수와 문자의 곱으로 이루어진 식
  - 계수: 문자 앞에 곱해진 수
  - 상수항: 문자를 포함하지 않은 항

• 식의 값: 문자에 수를 대입하여 계산한 값
  예: x = 3일 때, 2x + 5 = 2 × 3 + 5 = 11

• 일차식의 계산
  - 동류항: 문자와 차수가 같은 항
  - 동류항끼리만 덧셈, 뺄셈 가능
  예: 3x + 2x = 5x, 3x + 2y (계산 불가)

• 곱셈과 나눗셈
  - 분배법칙: a(b + c) = ab + ac
  - 예: 2(3x + 5) = 6x + 10
  - 나눗셈: 분수 형태로 표현
    예: (6x + 9) ÷ 3 = (6x + 9)/3 = 2x + 3'''
            },
            {
                'title': '4. 일차방정식',
                'content': '''일차방정식의 개념과 풀이 방법을 학습합니다.

• 방정식: 미지수를 포함한 등식
  - 예: 2x + 3 = 7
  - 해(근): 방정식을 참이 되게 하는 미지수의 값
  - 예: x = 2일 때, 2 × 2 + 3 = 7 (참)

• 일차방정식: ax + b = 0 (a ≠ 0) 형태의 방정식
  - 예: 3x - 6 = 0, 2x + 5 = 3x - 1

• 일차방정식의 풀이
  1) 이항: 등식의 한 변에 있는 항을 부호를 바꾸어 다른 변으로 옮김
     예: 3x - 6 = 0 → 3x = 6
  2) 양변을 같은 수로 나누거나 곱함
     예: 3x = 6 → x = 2
  
• 일차방정식의 활용
  - 문제 상황을 방정식으로 나타내기
  - 예: "어떤 수에 3을 곱하고 5를 더하면 20이 된다"
        → 3x + 5 = 20 → x = 5

• 등식의 성질
  - 등식의 양변에 같은 수를 더하거나 빼도 등식은 성립
  - 등식의 양변에 같은 수를 곱하거나 나눠도 등식은 성립 (0으로 나누기 제외)'''
            },
            {
                'title': '5. 좌표평면과 그래프',
                'content': '''좌표평면에서 점의 위치를 나타내고 그래프를 그리는 방법을 학습합니다.

• 좌표평면
  - x축(가로축)과 y축(세로축)이 만나는 점을 원점(0, 0)이라 함
  - 점의 위치: (x좌표, y좌표)로 나타냄
  - 제1사분면: x > 0, y > 0
  - 제2사분면: x < 0, y > 0
  - 제3사분면: x < 0, y < 0
  - 제4사분면: x > 0, y < 0

• 순서쌍과 좌표
  - 순서쌍: (x, y) 형태로 나타낸 두 수의 쌍
  - 예: (3, 4)는 x좌표가 3, y좌표가 4인 점

• 그래프
  - 좌표평면에 점들을 나타낸 것
  - 일차방정식의 해를 좌표평면에 나타내면 직선이 됨
  - 예: y = 2x + 1의 그래프는 직선

• 두 점 사이의 거리
  - 수평선: |x₂ - x₁|
  - 수직선: |y₂ - y₁|
  - 대각선: √{(x₂ - x₁)² + (y₂ - y₁)²}'''
            }
        ]
    },
    'grade1-2': {
        'name': '중1-2',
        'description': '중학교 1학년 2학기 수학: 기본도형, 평면도형, 입체도형, 통계',
        'lessons': [
            {
                'title': '1. 기본도형',
                'content': '''점, 직선, 평면 등 기본 도형의 개념을 학습합니다.

• 점, 직선, 평면
  - 점: 위치만 있고 크기가 없는 것
  - 직선: 양쪽으로 무한히 뻗어 나가는 선
  - 반직선: 한 점에서 한쪽으로만 뻗어 나가는 선
  - 선분: 두 점을 양 끝으로 하는 직선의 일부

• 각
  - 각: 한 점에서 두 반직선이 만나 이루는 도형
  - 각의 크기: 두 반직선이 벌어진 정도
  - 각의 표기: ∠ABC 또는 ∠B
  - 각의 단위: 도(°), 분('), 초(")
    1° = 60', 1' = 60"

• 각의 종류
  - 예각: 0° < 각 < 90°
  - 직각: 90°
  - 둔각: 90° < 각 < 180°
  - 평각: 180°
  - 맞꼭지각: 두 직선이 만날 때 마주보는 각 (크기가 같음)
  - 동위각: 두 직선과 한 직선이 만날 때 같은 위치에 있는 각
  - 엇각: 두 직선과 한 직선이 만날 때 엇갈린 위치에 있는 각

• 평행선의 성질
  - 평행한 두 직선에 한 직선이 만날 때
    • 동위각의 크기는 같다
    • 엇각의 크기는 같다
  - 동위각 또는 엇각의 크기가 같으면 두 직선은 평행하다'''
            },
            {
                'title': '2. 평면도형',
                'content': '''다각형, 원 등 평면도형의 성질과 넓이를 학습합니다.

• 다각형
  - 다각형: 세 개 이상의 선분으로 둘러싸인 도형
  - n각형: n개의 변을 가진 다각형
  - 내각: 다각형의 내부에 있는 각
  - 외각: 한 내각의 꼭짓점에서 한 변과 그 변의 연장선이 이루는 각
  - 대각선: 다각형에서 이웃하지 않은 두 꼭짓점을 잇는 선분

• 다각형의 내각의 합
  - 삼각형: 180°
  - 사각형: 360°
  - n각형: (n - 2) × 180°

• 다각형의 외각의 합: 항상 360°

• 삼각형
  - 종류: 정삼각형, 이등변삼각형, 직각삼각형, 예각삼각형, 둔각삼각형
  - 이등변삼각형: 두 변의 길이가 같은 삼각형
    • 두 밑각의 크기가 같다
    • 꼭짓점에서 밑변에 내린 수선은 밑변을 이등분한다
  - 정삼각형: 세 변의 길이가 모두 같은 삼각형
    • 세 내각의 크기가 모두 60°이다

• 사각형
  - 평행사변형: 두 쌍의 대변이 각각 평행한 사각형
    • 대변의 길이가 같다
    • 대각의 크기가 같다
    • 두 대각선은 서로 이등분한다
  - 직사각형: 네 내각이 모두 직각인 사각형
  - 마름모: 네 변의 길이가 모두 같은 사각형
  - 정사각형: 네 변의 길이가 모두 같고 네 내각이 모두 직각인 사각형
  - 사다리꼴: 한 쌍의 대변이 평행한 사각형

• 원과 부채꼴
  - 원: 한 점에서 같은 거리에 있는 점들의 집합
  - 중심: 원의 중심이 되는 점
  - 반지름: 중심에서 원 위의 한 점까지의 거리
  - 지름: 원 위의 두 점을 지나고 중심을 지나는 선분 (반지름의 2배)
  - 호: 원 위의 두 점 사이의 부분
  - 부채꼴: 두 반지름과 호로 둘러싸인 도형
  - 중심각: 부채꼴에서 두 반지름이 이루는 각

• 넓이 공식
  - 삼각형: (밑변 × 높이) ÷ 2
  - 평행사변형: 밑변 × 높이
  - 사다리꼴: (윗변 + 아랫변) × 높이 ÷ 2
  - 원: π × 반지름²
  - 부채꼴: 원의 넓이 × (중심각 / 360°)'''
            },
            {
                'title': '3. 입체도형',
                'content': '''입체도형의 성질과 겉넓이, 부피를 학습합니다.

• 다면체
  - 다면체: 평면으로만 둘러싸인 입체도형
  - 면: 다면체를 둘러싸는 평면
  - 모서리: 두 면이 만나는 선분
  - 꼭짓점: 세 개 이상의 면이 만나는 점

• 각기둥
  - 각기둥: 두 밑면이 서로 평행하고 합동인 다각형인 다면체
  - 종류: 삼각기둥, 사각기둥, 오각기둥, ...
  - 직각기둥: 옆면이 밑면에 수직인 각기둥
  - 정각기둥: 밑면이 정다각형이고 직각기둥인 각기둥

• 각뿔
  - 각뿔: 한 밑면이 다각형이고 옆면이 모두 삼각형인 다면체
  - 종류: 삼각뿔, 사각뿔, 오각뿔, ...
  - 정각뿔: 밑면이 정다각형이고 옆면이 모두 합동인 이등변삼각형인 각뿔

• 원기둥
  - 원기둥: 두 밑면이 서로 평행하고 합동인 원인 입체도형
  - 겉넓이: 2 × (밑면의 넓이) + (옆면의 넓이)
    = 2πr² + 2πrh (r: 반지름, h: 높이)
  - 부피: (밑면의 넓이) × 높이 = πr²h

• 원뿔
  - 원뿔: 밑면이 원이고 옆면이 부채꼴인 입체도형
  - 겉넓이: (밑면의 넓이) + (옆면의 넓이)
    = πr² + πrl (r: 반지름, l: 모선의 길이)
  - 부피: (밑면의 넓이) × 높이 ÷ 3 = (1/3)πr²h

• 구
  - 구: 한 점에서 같은 거리에 있는 점들의 집합으로 이루어진 입체도형
  - 겉넓이: 4πr² (r: 반지름)
  - 부피: (4/3)πr³

• 겉넓이와 부피
  - 겉넓이: 입체도형의 모든 면의 넓이의 합
  - 부피: 입체도형이 차지하는 공간의 크기'''
            },
            {
                'title': '4. 통계',
                'content': '''자료의 정리와 표현, 대표값을 학습합니다.

• 자료의 정리
  - 도수분포표: 자료를 구간별로 나누어 각 구간에 속하는 자료의 개수를 나타낸 표
  - 계급: 자료를 나눈 구간
  - 도수: 각 계급에 속하는 자료의 개수
  - 상대도수: (도수) / (전체 자료의 개수)
  - 도수분포다각형: 도수분포표를 그래프로 나타낸 것

• 히스토그램: 계급의 크기를 가로로, 도수를 세로로 나타낸 그래프

• 대표값
  - 평균: 모든 자료의 값을 더한 후 자료의 개수로 나눈 값
    평균 = (모든 자료의 합) / (자료의 개수)
  - 중앙값: 자료를 크기 순으로 나열했을 때 가운데에 오는 값
    • 자료의 개수가 홀수: (n+1)/2번째 값
    • 자료의 개수가 짝수: n/2번째와 (n/2+1)번째 값의 평균
  - 최빈값: 자료 중에서 가장 많이 나타나는 값
  - 범위: 최댓값 - 최솟값

• 그래프의 종류
  - 막대그래프: 각 항목의 크기를 막대의 길이로 나타낸 그래프
  - 꺾은선그래프: 시간에 따른 변화를 선으로 나타낸 그래프
  - 원그래프: 전체에 대한 각 부분의 비율을 부채꼴로 나타낸 그래프
  - 히스토그램: 도수분포를 나타낸 그래프'''
            }
        ]
    },
    'grade2-1': {
        'name': '중2-1',
        'description': '중학교 2학년 1학기 수학: 유리수와 순환소수, 식의 계산, 일차부등식, 연립일차방정식',
        'lessons': [
            {
                'title': '1. 유리수와 순환소수',
                'content': '''유리수와 순환소수의 관계를 학습합니다.

• 유리수
  - 유리수: 두 정수 a, b(b≠0)에 대하여 a/b로 나타낼 수 있는 수
  - 정수는 유리수에 포함됨

• 유한소수와 무한소수
  - 유한소수: 소수점 아래 자릿수가 유한한 소수
    예: 0.5, 0.25, 1.234
  - 무한소수: 소수점 아래 자릿수가 무한한 소수
    예: 0.333..., 0.142857142857...

• 순환소수
  - 순환소수: 소수점 아래의 어떤 자리부터 일정한 숫자의 배열이 반복되는 무한소수
  - 순환마디: 반복되는 숫자의 배열
  - 순환소수 표기: 순환마디의 첫 숫자와 마지막 숫자 위에 점을 찍어 표시
    예: 0.333... = 0.3̇, 0.142857142857... = 0.1̇42857̇

• 순환소수를 분수로 나타내기
  - 방법: 순환소수를 x로 놓고, 10의 거듭제곱을 곱하여 순환마디를 소수점 아래로 옮긴 후 빼기
  - 예: 0.3̇ = 1/3, 0.1̇42857̇ = 1/7

• 유리수와 순환소수
  - 모든 유리수는 유한소수 또는 순환소수로 나타낼 수 있음
  - 모든 유한소수와 순환소수는 유리수임'''
            },
            {
                'title': '2. 식의 계산',
                'content': '''다항식의 연산을 학습합니다.

• 다항식
  - 다항식: 한 개 또는 여러 개의 항의 합으로 이루어진 식
  - 항: 수나 문자, 또는 수와 문자의 곱으로 이루어진 식
  - 계수: 문자 앞에 곱해진 수
  - 차수: 항에서 문자가 곱해진 개수
  - 상수항: 문자를 포함하지 않은 항

• 일차식과 이차식
  - 일차식: 차수가 1인 다항식 (예: 3x + 2)
  - 이차식: 차수가 2인 다항식 (예: 2x² + 3x + 1)

• 다항식의 덧셈과 뺄셈
  - 동류항끼리만 계산 가능
  - 예: (3x² + 2x + 1) + (2x² - 3x + 5) = 5x² - x + 6
       (3x² + 2x + 1) - (2x² - 3x + 5) = x² + 5x - 4

• 다항식의 곱셈
  - 분배법칙 사용
  - 예: 2x(3x + 5) = 6x² + 10x
       (x + 2)(x + 3) = x² + 3x + 2x + 6 = x² + 5x + 6
       (x + 2)(x - 3) = x² - 3x + 2x - 6 = x² - x - 6

• 곱셈 공식
  - (a + b)² = a² + 2ab + b²
  - (a - b)² = a² - 2ab + b²
  - (a + b)(a - b) = a² - b²
  - (x + a)(x + b) = x² + (a + b)x + ab

• 다항식의 나눗셈
  - 분수 형태로 표현하거나 분배법칙 사용
  - 예: (6x² + 9x) ÷ 3x = (6x² + 9x) / (3x) = 2x + 3'''
            },
            {
                'title': '3. 일차부등식',
                'content': '''부등식의 개념과 일차부등식의 풀이를 학습합니다.

• 부등식
  - 부등식: 부등호(>, <, ≥, ≤)를 사용하여 두 수 또는 두 식의 크기를 비교한 식
  - 예: 3x + 2 > 7, 2x - 5 ≤ 3

• 부등식의 해
  - 부등식을 참이 되게 하는 미지수의 값
  - 예: x > 2인 모든 수가 부등식 3x + 2 > 7의 해

• 일차부등식
  - 일차부등식: ax + b > 0, ax + b < 0, ax + b ≥ 0, ax + b ≤ 0 (a ≠ 0) 형태의 부등식
  - 예: 3x - 6 > 0, 2x + 5 ≤ 3x - 1

• 일차부등식의 풀이
  1) 이항: 부등호의 방향은 그대로 유지
     예: 3x - 6 > 0 → 3x > 6
  2) 양변을 같은 양수로 나누거나 곱함 (부등호 방향 유지)
     예: 3x > 6 → x > 2
  3) 양변을 같은 음수로 나누거나 곱함 (부등호 방향 바뀜)
     예: -3x > 6 → x < -2

• 부등식의 성질
  - 부등식의 양변에 같은 수를 더하거나 빼도 부등호의 방향은 변하지 않음
  - 부등식의 양변에 같은 양수를 곱하거나 나눠도 부등호의 방향은 변하지 않음
  - 부등식의 양변에 같은 음수를 곱하거나 나누면 부등호의 방향이 바뀜

• 일차부등식의 활용
  - 문제 상황을 부등식으로 나타내기
  - 예: "어떤 수의 3배에서 5를 뺀 값이 10보다 크다"
        → 3x - 5 > 10 → x > 5'''
            },
            {
                'title': '4. 연립일차방정식',
                'content': '''연립일차방정식의 개념과 풀이 방법을 학습합니다.

• 연립일차방정식
  - 두 개 이상의 일차방정식을 한 쌍으로 묶어 놓은 것
  - 예: {2x + y = 7
        {x - y = 2
  - 해: 두 방정식을 모두 만족하는 x, y의 값
  - 예: 위 연립방정식의 해는 x = 3, y = 1

• 연립일차방정식의 풀이
  1) 대입법: 한 방정식을 한 문자에 대해 풀어 다른 방정식에 대입
     예: x - y = 2에서 x = y + 2
         이를 2x + y = 7에 대입: 2(y + 2) + y = 7
         3y + 4 = 7 → y = 1, x = 3
  
  2) 가감법: 두 방정식을 더하거나 빼서 한 문자를 소거
     예: {2x + y = 7
         {x - y = 2
         두 식을 더하면: 3x = 9 → x = 3
         x = 3을 대입하면: y = 1

• 연립일차방정식의 해의 개수
  - 해가 한 개: 두 직선이 한 점에서 만남
  - 해가 없음: 두 직선이 평행함 (일치하지 않음)
  - 해가 무수히 많음: 두 직선이 일치함

• 연립일차방정식의 활용
  - 두 미지수를 사용하는 문제를 연립방정식으로 해결
  - 예: "두 수의 합은 7이고 차는 3이다"
        → {x + y = 7
           {x - y = 3'''
            }
        ]
    },
    'grade2-2': {
        'name': '중2-2',
        'description': '중학교 2학년 2학기 수학: 일차함수, 도형의 닮음, 피타고라스 정리',
        'lessons': [
            {
                'title': '1. 일차함수',
                'content': '''일차함수의 개념과 그래프를 학습합니다.

• 함수
  - 함수: x의 값에 따라 y의 값이 하나씩 정해지는 관계
  - 정의역: x가 취할 수 있는 값의 범위
  - 치역: y가 취할 수 있는 값의 범위
  - 함수의 표기: y = f(x)

• 일차함수
  - 일차함수: y = ax + b (a ≠ 0) 형태의 함수
  - a: 기울기, b: y절편
  - 예: y = 2x + 3, y = -x + 5

• 일차함수의 그래프
  - 일차함수의 그래프는 직선
  - y = ax의 그래프: 원점을 지나는 직선
  - y = ax + b의 그래프: y = ax의 그래프를 y축 방향으로 b만큼 평행이동한 직선

• 기울기
  - 기울기: 직선이 x축의 양의 방향과 이루는 각의 크기
  - 기울기 = (y의 증가량) / (x의 증가량)
  - a > 0: 오른쪽 위로 향하는 직선
  - a < 0: 오른쪽 아래로 향하는 직선
  - |a|가 클수록 직선이 더 가파름

• 절편
  - x절편: 그래프가 x축과 만나는 점의 x좌표 (y = 0일 때의 x값)
  - y절편: 그래프가 y축과 만나는 점의 y좌표 (x = 0일 때의 y값)
  - y = ax + b에서 y절편은 b

• 일차함수의 식 구하기
  - 기울기와 한 점을 알 때: y - y₁ = a(x - x₁)
  - 두 점을 알 때: 기울기 a = (y₂ - y₁) / (x₂ - x₁)를 먼저 구한 후 한 점 대입
  - x절편과 y절편을 알 때: y = ax + b에서 b는 y절편, x절편을 대입하여 a 구하기

• 일차함수의 활용
  - 실생활 문제를 일차함수로 나타내기
  - 예: 시속 60km로 달리는 자동차의 이동 거리
        → y = 60x (x: 시간, y: 거리)'''
            },
            {
                'title': '2. 도형의 닮음',
                'content': '''닮은 도형의 성질과 닮음비를 학습합니다.

• 닮은 도형
  - 닮은 도형: 모양이 같고 크기만 다른 도형
  - 닮음 기호: ∽
  - 예: △ABC ∽ △DEF

• 닮음비
  - 닮은 도형에서 대응하는 변의 길이의 비
  - 예: △ABC ∽ △DEF이고 닮음비가 2:1이면
        AB:DE = BC:EF = CA:FD = 2:1

• 닮은 도형의 성질
  - 대응하는 각의 크기는 각각 같다
  - 대응하는 변의 길이의 비는 모두 같다
  - 닮음비가 m:n이면 넓이의 비는 m²:n², 부피의 비는 m³:n³

• 삼각형의 닮음 조건
  1) SSS 닮음: 세 쌍의 대응하는 변의 길이의 비가 모두 같을 때
  2) SAS 닮음: 두 쌍의 대응하는 변의 길이의 비가 같고, 그 끼인각의 크기가 같을 때
  3) AA 닮음: 두 쌍의 대응하는 각의 크기가 각각 같을 때

• 평행선과 선분의 비
  - 평행선 사이의 선분의 비는 같다
  - 예: l ∥ m일 때, AB:BC = DE:EF

• 닮은 도형의 활용
  - 높이나 거리를 구하는 문제
  - 예: 그림자의 길이를 이용하여 나무의 높이 구하기'''
            },
            {
                'title': '3. 피타고라스 정리',
                'content': '''피타고라스 정리와 그 활용을 학습합니다.

• 피타고라스 정리
  - 직각삼각형에서 빗변의 길이를 c, 나머지 두 변의 길이를 a, b라 할 때
    a² + b² = c²가 성립한다
  - 역으로 a² + b² = c²이면 이 삼각형은 직각삼각형이다

• 피타고라스 정리의 증명
  - 여러 가지 방법으로 증명 가능
  - 가장 간단한 방법: 정사각형의 넓이를 이용

• 피타고라스 정리의 활용
  - 직각삼각형에서 한 변의 길이를 구할 때
  - 예: 빗변의 길이 c = √(a² + b²)
        한 변의 길이 a = √(c² - b²)

• 피타고라스 수
  - 피타고라스 정리를 만족하는 세 자연수 (a, b, c)
  - 예: (3, 4, 5), (5, 12, 13), (8, 15, 17)

• 평면도형에서의 활용
  - 정사각형의 대각선의 길이: 한 변의 길이가 a이면 대각선 = a√2
  - 정삼각형의 높이: 한 변의 길이가 a이면 높이 = (a√3)/2

• 입체도형에서의 활용
  - 직육면체의 대각선의 길이
    가로 a, 세로 b, 높이 c일 때 대각선 = √(a² + b² + c²)
  - 원뿔의 모선의 길이
    반지름 r, 높이 h일 때 모선 l = √(r² + h²)'''
            }
        ]
    },
    'grade3-1': {
        'name': '중3-1',
        'description': '중학교 3학년 1학기 수학: 제곱근과 실수, 인수분해, 이차방정식, 이차함수',
        'lessons': [
            {
                'title': '1. 제곱근과 실수',
                'content': '''제곱근의 개념과 실수를 학습합니다.

• 제곱근
  - 제곱근: 제곱하여 a가 되는 수
  - a의 제곱근: x² = a를 만족하는 x
  - 양수 a의 제곱근: √a (양의 제곱근), -√a (음의 제곱근)
  - 0의 제곱근: 0
  - 음수의 제곱근: 실수 범위에서는 존재하지 않음

• 근호(√)
  - 근호: 제곱근을 나타내는 기호
  - √a: a의 양의 제곱근 (a ≥ 0)
  - 예: √9 = 3, √16 = 4

• 제곱근의 성질
  - (√a)² = a (a ≥ 0)
  - √(a²) = |a|
  - √(ab) = √a × √b (a ≥ 0, b ≥ 0)
  - √(a/b) = √a / √b (a ≥ 0, b > 0)

• 제곱근의 값
  - √2 ≈ 1.414, √3 ≈ 1.732, √5 ≈ 2.236
  - 제곱근표를 이용하여 근사값 구하기

• 무리수
  - 무리수: 유리수가 아닌 실수
  - 순환하지 않는 무한소수
  - 예: √2, √3, π, e

• 실수
  - 실수: 유리수와 무리수를 통틀어 이르는 수
  - 수직선 위의 모든 점에 대응
  - 실수의 대소 관계: 수직선에서 오른쪽에 있는 수가 더 큼

• 제곱근의 사칙연산
  - 덧셈, 뺄셈: 같은 근호끼리만 계산 가능
    예: 2√3 + 3√3 = 5√3
  - 곱셈, 나눗셈: 근호 안의 수끼리 곱하거나 나눔
    예: √2 × √3 = √6, √8 ÷ √2 = √4 = 2

• 분모의 유리화
  - 분모에 근호가 있을 때 분모를 유리수로 만드는 것
  - 예: 1/√2 = √2/2, 1/(√3 + 1) = (√3 - 1)/2'''
            },
            {
                'title': '2. 인수분해',
                'content': '''다항식을 인수의 곱으로 나타내는 방법을 학습합니다.

• 인수분해
  - 인수분해: 다항식을 두 개 이상의 다항식의 곱으로 나타내는 것
  - 예: x² + 5x + 6 = (x + 2)(x + 3)
  - 전개와 인수분해는 역의 관계

• 인수분해의 기본
  - 공통인수로 묶기
    예: 2x + 4 = 2(x + 2)
        x² + 3x = x(x + 3)

• 인수분해 공식
  1) a² + 2ab + b² = (a + b)²
  2) a² - 2ab + b² = (a - b)²
  3) a² - b² = (a + b)(a - b)
  4) x² + (a + b)x + ab = (x + a)(x + b)
  5) acx² + (ad + bc)x + bd = (ax + b)(cx + d)

• 이차식의 인수분해
  - x² + px + q 형태
    두 수의 합이 p, 곱이 q가 되는 두 수를 찾기
    예: x² + 5x + 6 = (x + 2)(x + 3)
  
  - ax² + bx + c 형태 (a ≠ 1)
    ac를 두 수의 곱으로 나타내고, 그 두 수의 합이 b가 되도록 하기
    예: 2x² + 7x + 3 = (2x + 1)(x + 3)

• 인수분해의 활용
  - 복잡한 식의 계산
  - 방정식의 풀이
  - 수의 성질 증명'''
            },
            {
                'title': '3. 이차방정식',
                'content': '''이차방정식의 개념과 풀이 방법을 학습합니다.

• 이차방정식
  - 이차방정식: ax² + bx + c = 0 (a ≠ 0) 형태의 방정식
  - 예: x² - 5x + 6 = 0, 2x² + 3x - 1 = 0

• 이차방정식의 해
  - 이차방정식을 만족하는 x의 값
  - 이차방정식은 최대 2개의 해를 가짐

• 인수분해를 이용한 풀이
  - 이차방정식을 인수분해하여 각 인수를 0으로 만드는 x 구하기
  - 예: x² - 5x + 6 = 0
        (x - 2)(x - 3) = 0
        x - 2 = 0 또는 x - 3 = 0
        따라서 x = 2 또는 x = 3

• 제곱근을 이용한 풀이
  - x² = a 형태의 이차방정식
  - x = ±√a
  - 예: x² = 9 → x = ±3
        (x - 2)² = 5 → x - 2 = ±√5 → x = 2 ± √5

• 완전제곱식을 이용한 풀이
  - 이차방정식을 완전제곱식으로 변형
  - 예: x² + 6x + 5 = 0
        x² + 6x + 9 = 4
        (x + 3)² = 4
        x + 3 = ±2
        x = -1 또는 x = -5

• 근의 공식
  - 이차방정식 ax² + bx + c = 0의 해
    x = (-b ± √(b² - 4ac)) / (2a)
  - 판별식: D = b² - 4ac
    • D > 0: 서로 다른 두 실근
    • D = 0: 중근 (한 개의 실근)
    • D < 0: 허근 (실근 없음)

• 이차방정식의 활용
  - 문제 상황을 이차방정식으로 나타내기
  - 예: "어떤 수의 제곱에서 그 수의 2배를 뺀 값이 3이다"
        → x² - 2x = 3 → x² - 2x - 3 = 0'''
            },
            {
                'title': '4. 이차함수',
                'content': '''이차함수의 개념과 그래프를 학습합니다.

• 이차함수
  - 이차함수: y = ax² + bx + c (a ≠ 0) 형태의 함수
  - 예: y = x², y = 2x² + 3x + 1, y = -x² + 4

• 이차함수 y = ax²의 그래프
  - 포물선 모양
  - 원점을 지남
  - y축에 대하여 대칭
  - a > 0: 아래로 볼록한 포물선
  - a < 0: 위로 볼록한 포물선
  - |a|가 클수록 그래프가 더 좁아짐

• 이차함수 y = ax² + bx + c의 그래프
  - y = ax²의 그래프를 평행이동한 것
  - 꼭짓점: (-b/(2a), (4ac - b²)/(4a))
  - 축: x = -b/(2a)
  - y절편: c

• 이차함수의 최댓값과 최솟값
  - a > 0: 최솟값만 존재 (꼭짓점의 y좌표)
  - a < 0: 최댓값만 존재 (꼭짓점의 y좌표)

• 이차함수의 식 구하기
  - 꼭짓점과 한 점을 알 때: y = a(x - p)² + q
  - 세 점을 알 때: y = ax² + bx + c에 대입하여 연립방정식 풀기
  - x절편을 알 때: y = a(x - α)(x - β) 형태

• 이차함수와 이차방정식
  - 이차함수 y = ax² + bx + c의 그래프와 x축의 교점의 x좌표가
    이차방정식 ax² + bx + c = 0의 해

• 이차함수의 활용
  - 최댓값, 최솟값 문제
  - 예: 직사각형의 넓이를 최대로 하는 문제'''
            }
        ]
    },
    'grade3-2': {
        'name': '중3-2',
        'description': '중학교 3학년 2학기 수학: 삼각비, 원의 성질, 통계',
        'lessons': [
            {
                'title': '1. 삼각비',
                'content': '''삼각비의 개념과 활용을 학습합니다.

• 삼각비
  - 직각삼각형에서 한 예각의 크기가 정해지면 세 변의 비가 정해짐
  - 삼각비: 직각삼각형의 변의 비
  - 예각 A에 대한 삼각비:
    • sin A = (높이) / (빗변) = BC / AB
    • cos A = (밑변) / (빗변) = AC / AB
    • tan A = (높이) / (밑변) = BC / AC

• 삼각비의 값
  - sin 30° = 1/2, cos 30° = √3/2, tan 30° = 1/√3
  - sin 45° = √2/2, cos 45° = √2/2, tan 45° = 1
  - sin 60° = √3/2, cos 60° = 1/2, tan 60° = √3

• 삼각비의 관계
  - sin² A + cos² A = 1
  - tan A = sin A / cos A
  - sin(90° - A) = cos A
  - cos(90° - A) = sin A
  - tan(90° - A) = 1 / tan A

• 삼각비표
  - 각도에 따른 삼각비의 값을 나타낸 표
  - 삼각비표를 이용하여 각도나 변의 길이 구하기

• 삼각비의 활용
  - 직각삼각형에서 한 변의 길이와 한 각의 크기를 알 때
    나머지 변의 길이 구하기
  - 예: 높이를 직접 측정하기 어려운 물체의 높이 구하기
  - 예각이 주어졌을 때 삼각비를 이용하여 변의 길이 구하기

• 사인법칙과 코사인법칙 (참고)
  - 사인법칙: a/sin A = b/sin B = c/sin C = 2R
  - 코사인법칙: a² = b² + c² - 2bc cos A'''
            },
            {
                'title': '2. 원의 성질',
                'content': '''원과 원주각의 성질을 학습합니다.

• 원과 현
  - 현: 원 위의 두 점을 잇는 선분
  - 지름: 원의 중심을 지나는 현 (가장 긴 현)
  - 현의 수직이등분선: 원의 중심을 지남

• 원주각
  - 원주각: 원 위의 한 점에서 두 현이 이루는 각
  - 중심각: 원의 중심에서 두 반지름이 이루는 각
  - 같은 호에 대한 원주각의 크기는 모두 같음
  - 원주각의 크기는 같은 호에 대한 중심각의 크기의 1/2

• 원주각의 성질
  - 반원의 원주각은 직각
  - 원에 내접하는 사각형의 대각의 합은 180°
  - 원에 내접하는 사각형의 한 외각의 크기는 그 내대각의 크기와 같음

• 접선과 할선
  - 접선: 원과 한 점에서 만나는 직선
  - 할선: 원과 두 점에서 만나는 직선
  - 접선의 길이: 원 밖의 한 점에서 원에 그은 접선의 길이는 모두 같음
  - 접선과 반지름: 접선은 접점에서 반지름에 수직

• 원의 접선의 성질
  - 원 밖의 한 점에서 원에 그은 두 접선의 길이는 같음
  - 접선과 할선: 할선과 접선이 만나는 점에서
    (접선의 길이)² = (할선의 밖 부분) × (할선의 전체 길이)

• 원과 비례
  - 두 현이 원 안에서 만날 때
    PA × PB = PC × PD
  - 두 할선이 원 밖에서 만날 때
    PA × PB = PC × PD
  - 접선과 할선이 만날 때
    (접선의 길이)² = PA × PB

• 원의 방정식
  - 중심이 (a, b)이고 반지름이 r인 원의 방정식
    (x - a)² + (y - b)² = r²
  - 중심이 원점이고 반지름이 r인 원의 방정식
    x² + y² = r²'''
            },
            {
                'title': '3. 통계',
                'content': '''자료의 분석과 확률을 학습합니다.

• 대푯값
  - 평균: 모든 자료의 값을 더한 후 자료의 개수로 나눈 값
    평균 = (모든 자료의 합) / (자료의 개수)
  - 중앙값: 자료를 크기 순으로 나열했을 때 가운데에 오는 값
  - 최빈값: 자료 중에서 가장 많이 나타나는 값
  - 분산: 편차의 제곱의 평균
    분산 = Σ(xᵢ - 평균)² / n
  - 표준편차: 분산의 제곱근
    표준편차 = √분산

• 상관관계
  - 두 변량 사이의 관계를 조사하는 것
  - 산점도: 두 변량의 관계를 점으로 나타낸 그래프
  - 양의 상관관계: 한 변량이 증가하면 다른 변량도 증가
  - 음의 상관관계: 한 변량이 증가하면 다른 변량은 감소
  - 상관관계가 없음: 두 변량 사이에 관계가 없음

• 확률
  - 확률: 어떤 사건이 일어날 가능성을 수로 나타낸 것
  - 확률 P(A) = (사건 A가 일어나는 경우의 수) / (모든 경우의 수)
  - 확률의 성질
    • 0 ≤ P(A) ≤ 1
    • P(전체) = 1
    • P(사건 A 또는 사건 B) = P(A) + P(B) - P(A 그리고 B)

• 경우의 수
  - 합의 법칙: 두 사건이 동시에 일어나지 않을 때
    경우의 수 = (첫 번째 사건의 경우의 수) + (두 번째 사건의 경우의 수)
  - 곱의 법칙: 두 사건이 동시에 일어날 때
    경우의 수 = (첫 번째 사건의 경우의 수) × (두 번째 사건의 경우의 수)

• 확률의 계산
  - 여사건의 확률: P(A') = 1 - P(A)
  - 두 사건이 동시에 일어날 확률: P(A 그리고 B) = P(A) × P(B) (독립일 때)
  - 두 사건 중 적어도 하나가 일어날 확률
    P(A 또는 B) = P(A) + P(B) - P(A 그리고 B)

• 통계적 추정
  - 모집단: 조사하려는 대상 전체
  - 표본: 모집단에서 선택한 일부
  - 표본 조사를 통하여 모집단의 특성 추정하기'''
            }
        ]
    }
}

@app.route('/')
def index():
    return render_template('index.html', topics=MATH_TOPICS)

@app.route('/topic/<topic_name>')
def topic(topic_name):
    if topic_name not in MATH_TOPICS:
        return "주제를 찾을 수 없습니다.", 404
    return render_template('topic.html', topic=MATH_TOPICS[topic_name], topic_key=topic_name)

@app.route('/practice/<topic_name>')
def practice(topic_name):
    if topic_name not in MATH_TOPICS:
        return "주제를 찾을 수 없습니다.", 404
    return render_template('practice.html', topic=MATH_TOPICS[topic_name], topic_key=topic_name)

@app.route('/api/generate_problem/<topic_name>')
def generate_problem(topic_name):
    """학기별 문제 생성 API"""
    if topic_name == 'grade1-1':
        problem_type = random.choice(['integer', 'rational', 'expression', 'equation', 'coordinate'])
        if problem_type == 'integer':
            # 정수와 유리수 문제
            a = random.randint(-20, 20)
            b = random.randint(-20, 20)
            op = random.choice(['+', '-', '×', '÷'])
            if op == '+':
                answer = a + b
                problem = f"({a}) + ({b}) = ?"
            elif op == '-':
                answer = a - b
                problem = f"({a}) - ({b}) = ?"
            elif op == '×':
                answer = a * b
                problem = f"({a}) × ({b}) = ?"
            else:  # ÷
                if b == 0:
                    b = random.randint(1, 10)
                answer = round(a / b, 2) if a % b != 0 else a // b
                problem = f"({a}) ÷ ({b}) = ?"
            return jsonify({
                'problem': problem,
                'answer': answer,
                'hint': '같은 부호끼리는 더하고, 다른 부호끼리는 빼세요. 곱셈과 나눗셈은 부호 규칙을 기억하세요.'
            })
        elif problem_type == 'rational':
            # 유리수 문제
            num1 = random.randint(1, 9)
            den1 = random.randint(2, 9)
            num2 = random.randint(1, 9)
            den2 = random.randint(2, 9)
            op = random.choice(['+', '-'])
            if op == '+':
                lcm = den1 * den2 // math.gcd(den1, den2)
                answer_num = num1 * (lcm // den1) + num2 * (lcm // den2)
                answer = f"{answer_num}/{lcm}"
                problem = f"{num1}/{den1} + {num2}/{den2} = ?"
            else:
                lcm = den1 * den2 // math.gcd(den1, den2)
                answer_num = num1 * (lcm // den1) - num2 * (lcm // den2)
                answer = f"{answer_num}/{lcm}"
                problem = f"{num1}/{den1} - {num2}/{den2} = ?"
            return jsonify({
                'problem': problem,
                'answer': answer,
                'hint': '분모를 통분한 후 분자를 더하거나 빼세요.'
            })
        elif problem_type == 'expression':
            # 문자와 식 문제
            a = random.randint(1, 10)
            b = random.randint(-10, 10)
            c = random.randint(-10, 10)
            x = random.randint(1, 10)
            problem = f"{a}x + {b}에서 x = {x}일 때 식의 값은?"
            answer = a * x + b
            return jsonify({
                'problem': problem,
                'answer': answer,
                'hint': 'x에 주어진 값을 대입하여 계산하세요.'
            })
        elif problem_type == 'equation':
            # 일차방정식 문제
            a = random.randint(1, 10)
            b = random.randint(-20, 20)
            c = random.randint(-20, 20)
            answer = round((c - b) / a, 2) if a != 0 else 0
            problem = f"{a}x + {b} = {c}"
            return jsonify({
                'problem': problem,
                'answer': answer,
                'hint': '이항하여 x를 구하세요. 양변에서 b를 빼고 a로 나누세요.'
            })
        else:  # coordinate
            # 좌표평면 문제
            x1 = random.randint(-10, 10)
            y1 = random.randint(-10, 10)
            x2 = random.randint(-10, 10)
            y2 = random.randint(-10, 10)
            answer = round(math.sqrt((x2 - x1)**2 + (y2 - y1)**2), 2)
            problem = f"두 점 ({x1}, {y1})과 ({x2}, {y2}) 사이의 거리는?"
            return jsonify({
                'problem': problem,
                'answer': answer,
                'hint': '두 점 사이의 거리 공식: √{(x₂-x₁)² + (y₂-y₁)²}'
            })
    
    elif topic_name == 'grade1-2':
        problem_type = random.choice(['angle', 'polygon', 'solid', 'statistics'])
        if problem_type == 'angle':
            # 각 문제
            angle_type = random.choice(['complementary', 'supplementary', 'vertical'])
            if angle_type == 'complementary':
                angle1 = random.randint(10, 80)
                angle2 = 90 - angle1
                problem = f"두 각의 합이 90°일 때, 한 각이 {angle1}°이면 다른 각은?"
                answer = angle2
                hint = '두 각의 합이 90°일 때, 한 각을 보각이라고 합니다.'
            elif angle_type == 'supplementary':
                angle1 = random.randint(10, 170)
                angle2 = 180 - angle1
                problem = f"두 각의 합이 180°일 때, 한 각이 {angle1}°이면 다른 각은?"
                answer = angle2
                hint = '두 각의 합이 180°일 때, 한 각을 여각이라고 합니다.'
            else:  # vertical
                angle = random.randint(30, 150)
                problem = f"맞꼭지각의 크기가 {angle}°일 때, 다른 맞꼭지각의 크기는?"
                answer = angle
                hint = '맞꼭지각의 크기는 서로 같습니다.'
            return jsonify({
                'problem': problem,
                'answer': answer,
                'hint': hint
            })
        elif problem_type == 'polygon':
            # 평면도형 문제
            shape_type = random.choice(['triangle_area', 'rectangle_area', 'circle_area', 'polygon_angle'])
            if shape_type == 'triangle_area':
                base = random.randint(5, 20)
                height = random.randint(5, 20)
                answer = base * height / 2
                problem = f"밑변 {base}cm, 높이 {height}cm인 삼각형의 넓이는?"
                hint = '삼각형의 넓이 = (밑변 × 높이) ÷ 2'
            elif shape_type == 'rectangle_area':
                width = random.randint(5, 20)
                height = random.randint(5, 20)
                answer = width * height
                problem = f"가로 {width}cm, 세로 {height}cm인 직사각형의 넓이는?"
                hint = '직사각형의 넓이 = 가로 × 세로'
            elif shape_type == 'circle_area':
                radius = random.randint(3, 15)
                answer = round(3.14 * radius**2, 2)
                problem = f"반지름 {radius}cm인 원의 넓이는? (π = 3.14)"
                hint = '원의 넓이 = π × 반지름²'
            else:  # polygon_angle
                n = random.choice([3, 4, 5, 6])
                answer = (n - 2) * 180
                problem = f"{n}각형의 내각의 합은?"
                hint = 'n각형의 내각의 합 = (n - 2) × 180°'
            return jsonify({
                'problem': problem,
                'answer': answer,
                'hint': hint
            })
        elif problem_type == 'solid':
            # 입체도형 문제
            solid_type = random.choice(['cylinder_volume', 'cone_volume', 'sphere_volume'])
            if solid_type == 'cylinder_volume':
                r = random.randint(3, 10)
                h = random.randint(5, 15)
                answer = round(3.14 * r**2 * h, 2)
                problem = f"반지름 {r}cm, 높이 {h}cm인 원기둥의 부피는? (π = 3.14)"
                hint = '원기둥의 부피 = π × 반지름² × 높이'
            elif solid_type == 'cone_volume':
                r = random.randint(3, 10)
                h = random.randint(5, 15)
                answer = round(3.14 * r**2 * h / 3, 2)
                problem = f"반지름 {r}cm, 높이 {h}cm인 원뿔의 부피는? (π = 3.14)"
                hint = '원뿔의 부피 = (1/3) × π × 반지름² × 높이'
            else:  # sphere_volume
                r = random.randint(3, 10)
                answer = round(4 * 3.14 * r**3 / 3, 2)
                problem = f"반지름 {r}cm인 구의 부피는? (π = 3.14)"
                hint = '구의 부피 = (4/3) × π × 반지름³'
            return jsonify({
                'problem': problem,
                'answer': answer,
                'hint': hint
            })
        else:  # statistics
            # 통계 문제
            stat_type = random.choice(['mean', 'median', 'mode'])
            numbers = sorted([random.randint(1, 20) for _ in range(5)])
            if stat_type == 'mean':
                answer = round(sum(numbers) / len(numbers), 2)
                problem = f"다음 숫자들의 평균을 구하세요: {', '.join(map(str, numbers))}"
                hint = '평균 = 모든 값의 합 ÷ 개수'
            elif stat_type == 'median':
                answer = numbers[len(numbers)//2]
                problem = f"다음 숫자들의 중앙값을 구하세요: {', '.join(map(str, numbers))}"
                hint = '중앙값은 데이터를 크기 순으로 정렬했을 때 가운데 값입니다.'
            else:  # mode
                counter = Counter(numbers)
                answer = counter.most_common(1)[0][0]
                problem = f"다음 숫자들의 최빈값을 구하세요: {', '.join(map(str, numbers))}"
                hint = '최빈값은 가장 자주 나타나는 값입니다.'
            return jsonify({
                'problem': problem,
                'answer': answer,
                'hint': hint
            })
    
    elif topic_name == 'grade2-1':
        problem_type = random.choice(['repeating_decimal', 'polynomial', 'inequality', 'system'])
        if problem_type == 'repeating_decimal':
            # 순환소수 문제
            fraction_type = random.choice(['simple', 'convert'])
            if fraction_type == 'simple':
                num = random.randint(1, 9)
                den = random.choice([3, 7, 9, 11])
                answer = f"{num}/{den}"
                problem = f"{num}/{den}을 소수로 나타내면?"
                hint = '분자를 분모로 나누어 소수로 나타내세요.'
            else:
                decimal = random.choice(['0.3', '0.6', '0.142857'])
                if decimal == '0.3':
                    answer = '1/3'
                elif decimal == '0.6':
                    answer = '2/3'
                else:
                    answer = '1/7'
                problem = f"순환소수 {decimal}...을 분수로 나타내면?"
                hint = '순환소수를 x로 놓고 10의 거듭제곱을 곱하여 계산하세요.'
            return jsonify({
                'problem': problem,
                'answer': answer,
                'hint': hint
            })
        elif problem_type == 'polynomial':
            # 다항식 계산 문제
            poly_type = random.choice(['expand', 'factor'])
            if poly_type == 'expand':
                a = random.randint(1, 5)
                b = random.randint(-5, 5)
                c = random.randint(-5, 5)
                answer = f"{a*c}x² + {a*b + c}x + {b}"
                problem = f"(x + {b})({a}x + {c})를 전개하면?"
                hint = '분배법칙을 사용하여 전개하세요.'
            else:
                x1 = random.randint(-5, 5)
                x2 = random.randint(-5, 5)
                b = -(x1 + x2)
                c = x1 * x2
                answer = f"(x + {x1})(x + {x2})"
                problem = f"x² + {b}x + {c}를 인수분해하면?"
                hint = '두 수의 합이 b이고 곱이 c가 되는 두 수를 찾으세요.'
            return jsonify({
                'problem': problem,
                'answer': answer,
                'hint': hint
            })
        elif problem_type == 'inequality':
            # 일차부등식 문제
            a = random.randint(1, 10)
            b = random.randint(-20, 20)
            c = random.randint(-20, 20)
            op = random.choice(['>', '<', '≥', '≤'])
            if op == '>':
                answer = f"x > {(c - b) / a:.2f}" if (c - b) / a != int((c - b) / a) else f"x > {(c - b) // a}"
            elif op == '<':
                answer = f"x < {(c - b) / a:.2f}" if (c - b) / a != int((c - b) / a) else f"x < {(c - b) // a}"
            elif op == '≥':
                answer = f"x ≥ {(c - b) / a:.2f}" if (c - b) / a != int((c - b) / a) else f"x ≥ {(c - b) // a}"
            else:
                answer = f"x ≤ {(c - b) / a:.2f}" if (c - b) / a != int((c - b) / a) else f"x ≤ {(c - b) // a}"
            problem = f"{a}x + {b} {op} {c}"
            return jsonify({
                'problem': problem,
                'answer': answer,
                'hint': '이항하여 x를 구하세요. 음수로 나누거나 곱할 때는 부등호 방향이 바뀝니다.'
            })
        else:  # system
            # 연립일차방정식 문제
            x = random.randint(1, 10)
            y = random.randint(1, 10)
            a1 = random.randint(1, 5)
            b1 = random.randint(1, 5)
            c1 = a1 * x + b1 * y
            a2 = random.randint(1, 5)
            b2 = random.randint(1, 5)
            c2 = a2 * x + b2 * y
            problem = f"연립방정식 {{ {a1}x + {b1}y = {c1} }} 의 해를 구하세요. (x, y 순서로 답하세요)"
            problem += f"\n{{ {a2}x + {b2}y = {c2} }}"
            answer = f"({x}, {y})"
            return jsonify({
                'problem': problem,
                'answer': answer,
                'hint': '대입법 또는 가감법을 사용하여 풀어보세요.'
            })
    
    elif topic_name == 'grade2-2':
        problem_type = random.choice(['linear_function', 'similarity', 'pythagoras'])
        if problem_type == 'linear_function':
            # 일차함수 문제
            func_type = random.choice(['value', 'slope', 'intercept'])
            if func_type == 'value':
                a = random.randint(1, 5)
                b = random.randint(-5, 5)
                x = random.randint(-5, 5)
                answer = a * x + b
                problem = f"일차함수 y = {a}x + {b}에서 x = {x}일 때 y의 값은?"
                hint = 'x 값을 함수식에 대입하여 계산하세요.'
            elif func_type == 'slope':
                x1, y1 = random.randint(-5, 5), random.randint(-5, 5)
                x2, y2 = random.randint(-5, 5), random.randint(-5, 5)
                if x1 == x2:
                    x2 = x1 + 1
                answer = round((y2 - y1) / (x2 - x1), 2)
                problem = f"두 점 ({x1}, {y1}), ({x2}, {y2})를 지나는 일차함수의 기울기는?"
                hint = '기울기 = (y의 증가량) / (x의 증가량)'
            else:  # intercept
                a = random.randint(1, 5)
                b = random.randint(-5, 5)
                answer = b
                problem = f"일차함수 y = {a}x + {b}의 y절편은?"
                hint = 'y절편은 x = 0일 때의 y값입니다.'
            return jsonify({
                'problem': problem,
                'answer': answer,
                'hint': hint
            })
        elif problem_type == 'similarity':
            # 닮음 문제
            ratio = random.choice([2, 3, 4])
            side1 = random.randint(5, 15)
            side2 = side1 * ratio
            answer = side2
            problem = f"두 삼각형이 닮음이고 닮음비가 1:{ratio}일 때, 작은 삼각형의 한 변이 {side1}cm이면 대응하는 큰 삼각형의 변의 길이는?"
            return jsonify({
                'problem': problem,
                'answer': answer,
                'hint': '닮음비가 m:n이면 대응하는 변의 길이의 비도 m:n입니다.'
            })
        else:  # pythagoras
            # 피타고라스 정리 문제
            a = random.randint(3, 10)
            b = random.randint(3, 10)
            find_type = random.choice(['hypotenuse', 'leg'])
            if find_type == 'hypotenuse':
                c = round(math.sqrt(a**2 + b**2), 2)
                problem = f"직각삼각형의 두 변의 길이가 {a}와 {b}일 때, 빗변의 길이는?"
                answer = c
                hint = '피타고라스 정리: c² = a² + b²'
            else:
                c = random.randint(max(a, b) + 1, 15)
                leg = round(math.sqrt(c**2 - a**2), 2) if a < c else round(math.sqrt(c**2 - b**2), 2)
                problem = f"직각삼각형에서 빗변의 길이가 {c}이고 한 변의 길이가 {a}일 때, 다른 변의 길이는?"
                answer = leg
                hint = '피타고라스 정리: a² = c² - b²'
            return jsonify({
                'problem': problem,
                'answer': answer,
                'hint': hint
            })
    
    elif topic_name == 'grade3-1':
        problem_type = random.choice(['square_root', 'factorization', 'quadratic_equation', 'quadratic_function'])
        if problem_type == 'square_root':
            # 제곱근 문제
            num = random.choice([4, 9, 16, 25, 36, 49, 64, 81, 100])
            answer = int(math.sqrt(num))
            problem = f"√{num} = ?"
            return jsonify({
                'problem': problem,
                'answer': answer,
                'hint': '제곱근은 제곱하여 그 수가 되는 양수입니다.'
            })
        elif problem_type == 'factorization':
            # 인수분해 문제
            x1 = random.randint(-5, 5)
            x2 = random.randint(-5, 5)
            b = -(x1 + x2)
            c = x1 * x2
            answer = f"(x + {x1})(x + {x2})" if x1 > 0 else f"(x - {-x1})(x + {x2})" if x2 > 0 else f"(x - {-x1})(x - {-x2})"
            problem = f"x² + {b}x + {c}를 인수분해하면?"
            return jsonify({
                'problem': problem,
                'answer': answer,
                'hint': '두 수의 합이 b이고 곱이 c가 되는 두 수를 찾으세요.'
            })
        elif problem_type == 'quadratic_equation':
            # 이차방정식 문제
            x1 = random.randint(-5, 5)
            x2 = random.randint(-5, 5)
            b = -(x1 + x2)
            c = x1 * x2
            if x1 == x2:
                answer = x1
                problem = f"x² + {b}x + {c} = 0의 해는?"
            else:
                answer = f"{x1} 또는 {x2}"
                problem = f"x² + {b}x + {c} = 0의 해는?"
            return jsonify({
                'problem': problem,
                'answer': answer,
                'hint': '인수분해하거나 근의 공식을 사용하세요.'
            })
        else:  # quadratic_function
            # 이차함수 문제
            func_type = random.choice(['value', 'vertex'])
            if func_type == 'value':
                a = random.randint(1, 3)
                b = random.randint(-3, 3)
                c = random.randint(-3, 3)
                x = random.randint(-3, 3)
                answer = a * x**2 + b * x + c
                problem = f"이차함수 y = {a}x² + {b}x + {c}에서 x = {x}일 때 y의 값은?"
                hint = 'x 값을 함수식에 대입하여 계산하세요.'
            else:
                a = random.randint(1, 3)
                b = random.randint(-5, 5)
                c = random.randint(-5, 5)
                vertex_x = -b / (2 * a)
                vertex_y = c - b**2 / (4 * a)
                answer = f"({vertex_x:.1f}, {vertex_y:.1f})"
                problem = f"이차함수 y = {a}x² + {b}x + {c}의 꼭짓점의 좌표는?"
                hint = '꼭짓점의 x좌표는 -b/(2a)이고, 이를 대입하여 y좌표를 구하세요.'
            return jsonify({
                'problem': problem,
                'answer': answer,
                'hint': hint
            })
    
    elif topic_name == 'grade3-2':
        problem_type = random.choice(['trigonometry', 'circle', 'statistics'])
        if problem_type == 'trigonometry':
            # 삼각비 문제
            angle = random.choice([30, 45, 60])
            trig_type = random.choice(['sin', 'cos', 'tan'])
            if angle == 30:
                if trig_type == 'sin':
                    answer = '1/2'
                elif trig_type == 'cos':
                    answer = '√3/2'
                else:
                    answer = '1/√3'
            elif angle == 45:
                answer = '√2/2' if trig_type != 'tan' else '1'
            else:  # 60
                if trig_type == 'sin':
                    answer = '√3/2'
                elif trig_type == 'cos':
                    answer = '1/2'
                else:
                    answer = '√3'
            problem = f"{trig_type} {angle}° = ?"
            return jsonify({
                'problem': problem,
                'answer': answer,
                'hint': '특수각의 삼각비 값을 기억하세요.'
            })
        elif problem_type == 'circle':
            # 원의 성질 문제
            circle_type = random.choice(['circumference', 'area', 'sector'])
            r = random.randint(3, 10)
            if circle_type == 'circumference':
                answer = round(2 * 3.14 * r, 2)
                problem = f"반지름 {r}cm인 원의 둘레는? (π = 3.14)"
                hint = '원의 둘레 = 2πr'
            elif circle_type == 'area':
                answer = round(3.14 * r**2, 2)
                problem = f"반지름 {r}cm인 원의 넓이는? (π = 3.14)"
                hint = '원의 넓이 = πr²'
            else:  # sector
                angle = random.choice([60, 90, 120, 180])
                answer = round(3.14 * r**2 * angle / 360, 2)
                problem = f"반지름 {r}cm, 중심각 {angle}°인 부채꼴의 넓이는? (π = 3.14)"
                hint = '부채꼴의 넓이 = 원의 넓이 × (중심각 / 360°)'
            return jsonify({
                'problem': problem,
                'answer': answer,
                'hint': hint
            })
        else:  # statistics
            # 통계 문제
            stat_type = random.choice(['mean', 'variance'])
            numbers = [random.randint(1, 20) for _ in range(5)]
            if stat_type == 'mean':
                answer = round(sum(numbers) / len(numbers), 2)
                problem = f"다음 숫자들의 평균을 구하세요: {', '.join(map(str, numbers))}"
                hint = '평균 = 모든 값의 합 ÷ 개수'
            else:
                mean = sum(numbers) / len(numbers)
                variance = sum((x - mean)**2 for x in numbers) / len(numbers)
                answer = round(variance, 2)
                problem = f"다음 숫자들의 분산을 구하세요: {', '.join(map(str, numbers))}"
                hint = '분산 = 편차의 제곱의 평균'
            return jsonify({
                'problem': problem,
                'answer': answer,
                'hint': hint
            })
    
    return jsonify({'error': '문제를 생성할 수 없습니다.'}), 400

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
