#/usr/bin/python3

import io
import sys

debug = False 
input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
stack = []
queue = []
tmp = 0
nline = 0
ncol = 0

def parse_block(block):
    fdata = {
        "정신나갈것같애": [push(tmp)],
        "정신나갈거같애": [read()],
        "정신나가서먹을것같애": [pop()],
        "정신나가서먹을거같애": [write(tmp)],
        "점심나갈것같애": [enqueue(tmp)],
        "점심나갈거같애": [tmp_dec()],
        "점심나가서먹을것같애": [dequeue()],
        "점심나가서먹을거같애": [tmp_inc()],
    }

    if debug:
        fdata['<'] = [enqueue(tmp)]
        fdata['>'] = [dequeue()]
        fdata['v'] = [push(tmp)]
        fdata['^'] = [pop()]
        fdata['+'] = [tmp_inc()]
        fdata['-'] = [tmp_dec()]
        fdata['p'] = [write(tmp)]
        fdata['r'] = [read()]
        fdata['l'] = [move_line()]
        fdata['.'] = [tmp_reset()]

    for k, v in fdata.copy().items():
        if "애" in k:
            fdata[k.replace("애", "아")] = v + [move_line()]
    
    for k, v in fdata.copy().items():
        fdata[k + '.'] = v + [tmp_reset()]
        if "정신" in k:
            fdata[k + '?'] = v + [stack_cmp()]
        elif "점심" in k:
            fdata[k + '?'] = v + [queue_cmp()]


    return fdata[block]

def interpret(lines):
    global ncol

    blocks = lines[:]
    if debug:
        blocks = list(map(lambda x: list(x.strip()), blocks))
    else:
        blocks = list(map(
            lambda x: x.strip().split(), 
            map(
                lambda x: 
                    x.replace('같아', '같아 ').replace('같애', '같애 ')
                    .replace(' .', '. ').replace(' ?', '? '),
                blocks
            )
        ))
    # print(blocks)

    while nline < len(blocks):
        fs = parse_block(blocks[nline][ncol])
        if len(blocks[nline]) - 1 == ncol and "move_line" not in str(fs):
            fs.append(next_line())
        if debug:
            print("l", nline, ncol)
        for f in fs:
            if debug:
                print(f)
            f()
        if debug:
            print("v", tmp, stack, queue)
        ncol += 1


def next_line():
    def inner():
        global nline, ncol
        nline += 1
        ncol = -1
    return inner

def move_line():
    def inner():
        global nline, ncol
        nline += stack.pop()
        ncol = -1
    return inner

def enqueue(x):
    def inner():
        queue.insert(0, x)
    return inner

def dequeue():
    def inner():
        global tmp
        tmp = queue.pop()
    return inner

def queue_cmp():
    def inner():
        global tmp
        enqueue(int(queue[-1] == tmp))()
    return inner

def push(x):
    def inner():
        stack.append(x)
    return inner

def pop():
    def inner():
        global tmp
        tmp = stack.pop()
    return inner

def stack_cmp():
    def inner():
        global tmp
        push(int(stack[-1] == tmp))()
    return inner

def tmp_dec():
    def inner():
        global tmp
        tmp -= 1
    return inner

def tmp_inc():
    def inner():
        global tmp
        tmp += 1
    return inner

def tmp_reset():
    def inner():
        global tmp
        tmp = 0
    return inner

def read():
    def inner():
        global tmp
        tmp = ord(input_stream.read(1))
    return inner

def write(code):
    def inner():
        sys.stdout.write(chr(code))
    return inner

def main():
    if not sys.argv[1]:
        print("파일안줘서정신나갈것같애")
        exit(1)
    
    f = None
    
    try:
        f = open(sys.argv[1], 'r')
    except FileNotFoundError:
        print("파일이없어정신나갈것같애")
        exit(1)
    
    interpret(f.readlines())
    

if __name__ == '__main__':
    main()