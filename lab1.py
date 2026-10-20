priority = {
    '>=': 0,
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    'u-': 3,
}
operators = '>=+-*/()'

def lexer(exp):
    text = exp.replace(' ', '')
    tokens = []
    i = 0

    while i < len(text):
        if text[i:i+3] == 'min':
            tokens.append('min')
            i += 3
            continue

        if text[i:i+2] == '>=':
            tokens.append('>=')
            i += 2
            continue

        if text[i] == ',':
            tokens.append(',')
            i += 1
            continue

        unary_minus = (text[i] == '-' and
                       (i == 0 or text[i - 1] in '+-*/(,' or text[i - 2:i] == '>='))

        if text[i] in operators and not unary_minus:
            tokens.append(text[i])
            i += 1
            continue

        number = ''
        if unary_minus:
            number += '-'
            i += 1

        while i < len(text) and (text[i].isdigit() or text[i] == '.'):
            number += text[i]
            i += 1

        if number and number != '-':
            if '.' in number:
                tokens.append(float(number))
            else:
                tokens.append(int(number))
        elif not number:
            i += 1

    return tokens

def to_postfix(tokens):
    result = []
    stack = []

    for token in tokens:
        if type(token) in (int, float):
            result.append(token)
        elif token in ('(', 'min'):
            stack.append(token)
        elif token == ',':
            while stack and stack[-1] not in ('(', 'min'):
                result.append(stack.pop())
        elif token == ')':
            while stack and stack[-1] != '(':
                result.append(stack.pop())
            if stack and stack[-1] == '(':
                stack.pop()
            if stack and stack[-1] == 'min':
                result.append(stack.pop())
        elif token in priority:
            current_priority = priority[token]
            while stack and stack[-1] not in ('(', 'min'):
                top_op = stack[-1]
                top_priority = priority.get(top_op, 0)
                if top_priority >= current_priority:
                    result.append(stack.pop())
                else:
                    break
            stack.append(token)

    while stack:
        result.append(stack.pop())

    return (' '.join(str(x) for x in result))

def to_prefix(postfix):
    result = []
    elements = postfix.split()
    for i in elements:
        if i.replace('-', '', 1).replace('.', '', 1).isdigit():
            result.append(i)

        elif i == 'u-':
            a = result.pop()
            result.append(f'-{a}')

        elif str(i) in operators or i == 'min':
            b = result.pop()
            a = result.pop()
            result.append(f'{i} {a} {b}')

    return ' '.join(result)


def calculate(postfix):
    result = []
    elements = postfix.split()
    for i in elements:
        if i.replace('-', '', 1).replace('.', '', 1).isdigit():
            result.append(float(i) if "." in i else int(i))
        elif i == 'min':
            b = result.pop()
            a = result.pop()
            result.append(min(a, b))
        elif i in operators:
            b = result.pop()
            a = result.pop()
            if i == '+':
                result.append(a + b)
            elif i == '-':
                result.append(a - b)
            elif i == '*':
                result.append(a * b)
            elif i == '/':
                result.append(a / b)
            elif i == '>=':
                result.append(int(a >= b))

    return result[-1]

user_input = input('Введите выражение: ')

try:
    postfix = to_postfix(lexer(user_input))
    prefix = to_prefix(postfix)
    result = calculate(postfix)

    print(f'Результат: {result}')
    print(f'Префиксная запись: {prefix}')
    print(f'Постфиксная запись: {postfix}')

except (ValueError, IndexError, ZeroDivisionError):
    print('Ошибка: некорректное выражение!')