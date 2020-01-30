import sys, argparse, re


elements = [
  {'name': 'minute', 'max': 60, 'index': 0},
  {'name': 'hour', 'max': 24, 'index': 0},
  {'name': 'day of month', 'max': 31, 'index': 1},
  {'name': 'month', 'max': 12, 'index': 1},
  {'name': 'day of week', 'max': 7, 'index': 1},
  {'name': 'command'}
]


def expandArg(arg, position):
  if position == 5:
    return arg
  indexMax = elements[position]['max']
  indexStart = elements[position]['index']
  wildcard = re.match(re.compile(r'^\*$'), arg)
  interval = re.match(re.compile(r'^\*/(\d+)'), arg)
  numrange = re.match(re.compile(r'^(\d+)-(\d+)$'), arg)
  if wildcard:
    numlist = list(range(indexStart, indexMax + indexStart))
    return ' '.join(str(num) for num in numlist)
  elif interval:
    numlist = list(range(indexStart, indexMax + indexStart))
    filtered = [num for num in numlist if int(num) % int(interval.group(1)) == 0]
    return ' '.join(str(num) for num in list(filtered))
  elif numrange:
    numlist = list(range(int(numrange.group(1)), int(numrange.group(2)) + 1))
    return ' '.join(str(num) for num in numlist)
  else:
    return arg


def main():
  parser = argparse.ArgumentParser(description='Process some integers.')
  parser.add_argument('cronstring', nargs="*", help='full crontab string')
  args = parser.parse_args()
  argList = args.cronstring[0].split(' ',5)
  expanded = [expandArg(x, i) for i, x in enumerate(argList)]
  names = [x['name'] for x in elements]
  results = zip(names, expanded)
  for line in results:
    print("{:<14} {}".format(*line))


if __name__ == '__main__':
  main()


#TODO - README, tests


