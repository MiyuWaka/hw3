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
      keta /= 10
      index += 1
  token = {'type': 'NUMBER', 'number': number}
  return token, index


def readPlus(line, index):
  token = {'type': 'PLUS'}
  return token, index + 1


def readMinus(line, index):
  token = {'type': 'MINUS'}
  return token, index + 1


def readTimes(line, index):
  token = {'type': 'TIMES'}
  return token, index + 1


def readDivided(line, index):
  token = {'type': 'DIVIDED'}
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
      (token, index) = readTimes(line, index)
    elif line[index] == '/':
      (token, index) = readDivided(line, index)
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)
  return tokens

#掛け算と割り算を先に計算する関数
#入力はtokens、出力は掛け算割り算の処理だけ終えたtokens
def MultiplicationAndDivision(tokens):
  value = 0
  #tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
  index = 1
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'TIMES':
        value = tokens[index-2]['number'] * tokens[index]['number']
        tokens[index-2] = {'type': 'NUMBER', 'number': value} 
        for i in range(index+1,len(tokens)):
          tokens[i-2] = tokens[i]
        del tokens[len(tokens)-2:len(tokens)]
        print(tokens)
      elif tokens[index - 1]['type'] == 'DIVIDED':
        value = tokens[index-2]['number'] / tokens[index]['number']
        tokens[index-2] = {'type': 'NUMBER', 'number': value} 
        for i in range(index+1,len(tokens)):
          tokens[i-2] = tokens[i]
        del tokens[len(tokens)-2:len(tokens)]
    index += 1
  return tokens


def evaluate(tokens):
  answer = 0
  tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
  index = 1
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'PLUS':
        answer += tokens[index]['number']
      elif tokens[index - 1]['type'] == 'MINUS':
        answer -= tokens[index]['number']
      else:
        print('Invalid syntax')
        exit(1)
    index += 1
  return answer


def test(line):
  tokens = tokenize(line)
  tokens = MultiplicationAndDivision(tokens)
  actualAnswer = evaluate(tokens)
  expectedAnswer = eval(line)
  if abs(actualAnswer - expectedAnswer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expectedAnswer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
  print("==== Test started! ====")
  test("3")
  test("1+2")
  test("1.0+2.1-3")
  test("1.5+6")
  test("1.0+2.1")
  test("5-3")
  test("6-10")
  test("-3+5")
  test("7.9-3")
  test("6.3-2.5")
  test("1.7-5.6")
  test("5*9")
  test("3.2*5")
  test("3.2*3.9")
  test("3*2+3")
  test("5*7-3")
  test("5+3*4")
  test("4-8*3")
  test("5/9")
  test("3.2/5")
  test("3.2/3.9")
  test("3/2+3")
  test("5/7-3")
  test("5+3/4")
  test("4-8/3")
  test("5*6/2")
  test("5.3*9.8/2.1")
  print("==== Test finished! ====\n")

runTest()

while True:
  print('> ', end="")
  line = input()
  tokens = tokenize(line)
  tokens = MultiplicationAndDivision(tokens)
  answer = evaluate(tokens)
  print("answer = %f\n" % answer)