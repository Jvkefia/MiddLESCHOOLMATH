from flask import Flask, render_template, request, jsonify
import random
import math

app = Flask(__name__)

# 중학교 수학 주제별 데이터
MATH_TOPICS = {
    'algebra': {
        'name': '대수',
        'description': '일차방정식, 이차방정식, 인수분해 등을 학습합니다.',
        'lessons': [
            {'title': '일차방정식', 'content': '일차방정식은 ax + b = 0 형태의 방정식입니다.'},
            {'title': '이차방정식', 'content': '이차방정식은 ax² + bx + c = 0 형태의 방정식입니다.'},
            {'title': '인수분해', 'content': '인수분해는 다항식을 곱셈의 형태로 나타내는 것입니다.'},
        ]
    },
    'geometry': {
        'name': '기하',
        'description': '도형의 성질, 피타고라스 정리, 원의 성질 등을 학습합니다.',
        'lessons': [
            {'title': '피타고라스 정리', 'content': '직각삼각형에서 빗변의 제곱은 다른 두 변의 제곱의 합과 같습니다.'},
            {'title': '원의 성질', 'content': '원의 중심에서 원 위의 한 점까지의 거리는 모두 같습니다.'},
            {'title': '도형의 닮음', 'content': '닮은 도형은 모양이 같고 크기만 다른 도형입니다.'},
        ]
    },
    'statistics': {
        'name': '통계',
        'description': '평균, 중앙값, 최빈값, 그래프 등을 학습합니다.',
        'lessons': [
            {'title': '평균, 중앙값, 최빈값', 'content': '평균은 모든 값의 합을 개수로 나눈 값입니다.'},
            {'title': '그래프', 'content': '데이터를 시각적으로 표현하는 방법입니다.'},
            {'title': '확률', 'content': '확률은 어떤 사건이 일어날 가능성을 수로 나타낸 것입니다.'},
        ]
    },
    'function': {
        'name': '함수',
        'description': '일차함수, 이차함수, 함수의 그래프 등을 학습합니다.',
        'lessons': [
            {'title': '일차함수', 'content': '일차함수는 y = ax + b 형태의 함수입니다.'},
            {'title': '이차함수', 'content': '이차함수는 y = ax² + bx + c 형태의 함수입니다.'},
            {'title': '함수의 그래프', 'content': '함수를 좌표평면에 나타낸 것입니다.'},
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
    """주제별 문제 생성 API"""
    if topic_name == 'algebra':
        problem_type = random.choice(['linear', 'quadratic', 'factor'])
        if problem_type == 'linear':
            a = random.randint(1, 10)
            b = random.randint(-10, 10)
            answer = -b / a if a != 0 else 0
            problem = f"{a}x + {b} = 0"
            return jsonify({
                'problem': problem,
                'answer': round(answer, 2),
                'hint': '일차방정식은 ax + b = 0 형태입니다. x를 구하려면 양변에서 b를 빼고 a로 나누세요.'
            })
        elif problem_type == 'quadratic':
            a = random.randint(1, 5)
            b = random.randint(-5, 5)
            c = random.randint(-5, 5)
            problem = f"{a}x² + {b}x + {c} = 0"
            discriminant = b**2 - 4*a*c
            if discriminant >= 0:
                answer1 = (-b + math.sqrt(discriminant)) / (2*a)
                answer2 = (-b - math.sqrt(discriminant)) / (2*a)
                return jsonify({
                    'problem': problem,
                    'answer': [round(answer1, 2), round(answer2, 2)],
                    'hint': '이차방정식의 근의 공식을 사용하세요: x = (-b ± √(b²-4ac)) / 2a'
                })
        else:
            # 인수분해 문제
            x1 = random.randint(-5, 5)
            x2 = random.randint(-5, 5)
            a = 1
            b = -(x1 + x2)
            c = x1 * x2
            problem = f"x² + {b}x + {c}를 인수분해하세요"
            return jsonify({
                'problem': problem,
                'answer': f"(x - {x1})(x - {x2})",
                'hint': '두 수의 합이 b이고 곱이 c가 되는 두 수를 찾으세요.'
            })
    
    elif topic_name == 'geometry':
        problem_type = random.choice(['pythagoras', 'area', 'perimeter'])
        if problem_type == 'pythagoras':
            a = random.randint(3, 8)
            b = random.randint(3, 8)
            c = round(math.sqrt(a**2 + b**2), 2)
            problem = f"직각삼각형의 두 변의 길이가 {a}와 {b}일 때, 빗변의 길이는?"
            return jsonify({
                'problem': problem,
                'answer': c,
                'hint': '피타고라스 정리: c² = a² + b²'
            })
        elif problem_type == 'area':
            shape = random.choice(['rectangle', 'circle'])
            if shape == 'rectangle':
                width = random.randint(5, 15)
                height = random.randint(5, 15)
                problem = f"가로 {width}cm, 세로 {height}cm인 직사각형의 넓이는?"
                return jsonify({
                    'problem': problem,
                    'answer': width * height,
                    'hint': '직사각형의 넓이 = 가로 × 세로'
                })
            else:
                radius = random.randint(3, 10)
                problem = f"반지름이 {radius}cm인 원의 넓이는? (π = 3.14)"
                return jsonify({
                    'problem': problem,
                    'answer': round(3.14 * radius**2, 2),
                    'hint': '원의 넓이 = π × r²'
                })
    
    elif topic_name == 'statistics':
        problem_type = random.choice(['mean', 'median', 'mode'])
        numbers = sorted([random.randint(1, 20) for _ in range(5)])
        if problem_type == 'mean':
            problem = f"다음 숫자들의 평균을 구하세요: {', '.join(map(str, numbers))}"
            return jsonify({
                'problem': problem,
                'answer': round(sum(numbers) / len(numbers), 2),
                'hint': '평균 = 모든 값의 합 ÷ 개수'
            })
        elif problem_type == 'median':
            problem = f"다음 숫자들의 중앙값을 구하세요: {', '.join(map(str, numbers))}"
            return jsonify({
                'problem': problem,
                'answer': numbers[len(numbers)//2],
                'hint': '중앙값은 데이터를 크기 순으로 정렬했을 때 가운데 값입니다.'
            })
        else:
            # 최빈값
            from collections import Counter
            counter = Counter(numbers)
            mode_value = counter.most_common(1)[0][0]
            problem = f"다음 숫자들의 최빈값을 구하세요: {', '.join(map(str, numbers))}"
            return jsonify({
                'problem': problem,
                'answer': mode_value,
                'hint': '최빈값은 가장 자주 나타나는 값입니다.'
            })
    
    elif topic_name == 'function':
        problem_type = random.choice(['linear', 'quadratic'])
        if problem_type == 'linear':
            a = random.randint(1, 5)
            b = random.randint(-5, 5)
            x = random.randint(-5, 5)
            problem = f"일차함수 y = {a}x + {b}에서 x = {x}일 때 y의 값은?"
            return jsonify({
                'problem': problem,
                'answer': a * x + b,
                'hint': 'x 값을 함수식에 대입하여 계산하세요.'
            })
        else:
            a = random.randint(1, 3)
            b = random.randint(-3, 3)
            c = random.randint(-3, 3)
            x = random.randint(-3, 3)
            problem = f"이차함수 y = {a}x² + {b}x + {c}에서 x = {x}일 때 y의 값은?"
            return jsonify({
                'problem': problem,
                'answer': a * x**2 + b * x + c,
                'hint': 'x 값을 함수식에 대입하여 계산하세요.'
            })
    
    return jsonify({'error': '문제를 생성할 수 없습니다.'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
