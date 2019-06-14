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


def readOpenBrackets(line, index):
  token = {'type': 'OPENBRACKETS'}
  return token, index + 1


def readCloseBrackets(line, index):
  token = {'type': 'CLOSEBRACKETS'}
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
    elif line[index] == '(':
      (token, index) = readOpenBrackets(line, index)
    elif line[index] == ')':
      (token, index) = readCloseBrackets(line, index)
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)
  return tokens

#一番内側の()の中を計算する関数
#入力はtokens、出力は()を計算し終えたtokens
def brackets(tokens):
  index = 0
  openindex = 1
  closeindex = 1
  while index < len(tokens):
    if tokens[index]['type'] == 'OPENBRACKETS':
      openindex = index
    if tokens[index]['type'] == 'CLOSEBRACKETS':
      closeindex = index
      break
    index += 1
  print(openindex)
  print(closeindex)
  tokens = MultiplicationAndDivision(tokens,openindex+1,closeindex)
  answer = evaluate(tokens,openindex+1,closeindex+1) 
  #print(answer)
  tokens[openindex] = {'type': 'NUMBER', 'number': answer}
  print(len(tokens))
  print(tokens)
  for i in range(closeindex+2,len(tokens)):
    tokens[i-(closeindex-openindex+1)] = tokens[i]
  del tokens[len(tokens)-(closeindex-openindex+1):len(tokens)]
  print(tokens)
  return tokens


#掛け算と割り算を先に計算する関数
#入力はtokens,開始index,終了index、出力は掛け算割り算の処理だけ終えたtokens
def MultiplicationAndDivision(tokens,sindex,cindex):  
  value = 0
  #tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
  while sindex < cindex:
    if tokens[sindex]['type'] == 'NUMBER':
      if tokens[sindex - 1]['type'] == 'TIMES':
        value = tokens[sindex-2]['number'] * tokens[sindex]['number']
        tokens[sindex-2] = {'type': 'NUMBER', 'number': value} 
        for i in range(sindex+1,cindex):
          tokens[i-2] = tokens[i]
        del tokens[cindex-2:cindex]
      elif tokens[sindex - 1]['type'] == 'DIVIDED':
        value = tokens[sindex-2]['number'] / tokens[sindex]['number']
        tokens[sindex-2] = {'type': 'NUMBER', 'number': value} 
        for i in range(sindex+1,cindex):
          tokens[i-2] = tokens[i]
        del tokens[cindex-2:cindex]
    sindex += 1
  return tokens


def evaluate(tokens,sindex,cindex):
  answer = 0
  tokens.insert(sindex, {'type': 'PLUS'}) # Insert a dummy '+' token
  #print(tokens)
  while sindex < cindex:
    if tokens[sindex]['type'] == 'NUMBER':
      if tokens[sindex - 1]['type'] == 'PLUS':
        answer += tokens[sindex]['number']
      elif tokens[sindex - 1]['type'] == 'MINUS':
        answer -= tokens[sindex]['number']
      else:
        print('Invalid syntax')
        exit(1)
    sindex += 1
  return answer


def test(line):
  tokens = tokenize(line)
  numbrackets =[v for v in tokens if v == {'type': 'CLOSEBRACKETS'}]
  for _ in range(len(numbrackets)):
    tokens = brackets(tokens)
  tokens = MultiplicationAndDivision(tokens,0,len(tokens))
  actualAnswer = evaluate(tokens,0,len(tokens)+1)
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
  print("==== Test finished! ====\n")

runTest()

while True:
  print('> ', end="")
  line = input()
  tokens = tokenize(line)
  #print(tokens)
  numbrackets =[v for v in tokens if v == {'type': 'CLOSEBRACKETS'}]
  #print("numbrackets = %f\n" % len(numbrackets))
  #print(len(numbrackets))
  for _ in range(len(numbrackets)):
    tokens = brackets(tokens)
  tokens = MultiplicationAndDivision(tokens,0,len(tokens))
  answer = evaluate(tokens,0,len(tokens)+1)
  print("answer = %f\n" % answer)