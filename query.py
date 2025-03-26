from stack import Stack


def precedence(token):
    """ Precedence of supported operators """
    __precedence = {"&": 2, "|": 1}
    try:
        return __precedence[token]
    except:
        return -1


def infix_to_postfix(tokens):
    stack = Stack()
    postfix = list()

    for token in tokens:
        if token == '(':
            stack.push(token)
        elif token == ')':
            while (not stack.is_empty()) and stack.peek() != "(":
                key = stack.pop()
                postfix.append(key)
            if not stack.is_empty() and stack.peek() != "(":
                raise ValueError("Query isn't well formatted")
            else:
                stack.pop()
        elif token == "&" or token == "|":
            while not stack.is_empty() and (
                precedence(token) <= precedence(stack.peek())
            ):
                postfix.append(stack.pop())
            stack.push(token)
        else:
            postfix.append(token)

    while not stack.is_empty():
        postfix.append(stack.pop())

    return postfix
