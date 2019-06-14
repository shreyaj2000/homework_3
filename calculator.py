def readNumber(line, index):
  number = 0
  while index < len(line) and line[index].isdigit():
    number = number * 10 + int(line[index])
    index += 1
  if index < len(line) and line[index] == '.':
    index += 1
    keta = 0.1
    while index < len(line) and line[index].isdigit():
      number += int(line[index]) * keta
      keta *= 0.1
      index += 1
  token = {'type': 'NUMBER', 'number': number}
  return token, index


def readPlus(line, index):
  token = {'type': 'PLUS'}
  return token, index + 1

def readMinus(line, index):
  token = {'type': 'MINUS'}
  return token, index + 1

def readMul(line, index):
  token = {'type': 'MUL'}
  return token, index + 1

def readDiv(line, index):
  token = {'type': 'DIV'}
  return token, index + 1

def readStart(line, index):
  token = {'type': 'START_BRACKET'}
  return token, index + 1

def readEnd(line, index):
  token = {'type': 'END_BRACKET'}
  return token, index + 1


def tokenize(line):
  tokens = []
  index = 0
  while index < len(line):
    if line[index].isdigit():
      (token, index) = readNumber(line, index)
    elif line[index] == '+':
      (token, index) = readPlus(line, index)
    elif line[index] == '-':
      (token, index) = readMinus(line, index)
    elif line[index] == '*':
      (token, index) = readMul(line, index)
    elif line[index] == '/':
      (token, index) = readDiv(line, index)
    elif line[index] == '(':
      (token, index) = readStart(line, index)
    elif line[index] == ')':
      (token, index) = readEnd(line, index)
    elif line[index] == ' ':
      index = index + 1
    else:
      print ('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)
  return tokens


def evaluate(tokens):

  tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
  answer = 0
  index = 1

  while index < len(tokens):

    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'MUL':
        temp = tokens[index-2]['number'] * tokens[index]['number']
        tokens[index-2]['number'] = temp
        del tokens[index-1:index+1]
        index -= 1
      elif tokens[index - 1]['type'] == 'DIV':
        temp = tokens[index-2]['number'] / tokens[index]['number']*1.0
        tokens[index-2]['number'] = temp
        del tokens[index-1:index+1]
        index -= 1
    index += 1

  index = 1

  while index < len(tokens):

    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'PLUS':
        answer += tokens[index]['number']
        del tokens[index-1:index]
      elif tokens[index - 1]['type'] == 'MINUS':
        answer -= tokens[index]['number']
        del tokens[index-1:index]

    index += 1

  return answer

def test(line):
  tokens = tokenize(line)
  actualAnswer = evaluate(tokens)
  expectedAnswer = eval(line)
  if abs(actualAnswer - expectedAnswer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expectedAnswer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


def runTest():
  print("==== Test started! ====")
  test("1+2")
  test("1.0+2.1-3")
  test("4+2*5")
  test("5-4/2")
  test("5*2*3")
  test("10/5/2")
  print("==== Test finished! ====\n")

runTest()

while True:
  print('> ', end="")
  line = input()
  tokens = tokenize(line)
  answer = evaluate(tokens)
  print("answer = %f\n" % answer)