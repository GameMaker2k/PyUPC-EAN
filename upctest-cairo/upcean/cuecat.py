#!/usr/bin/python
#
# This code is public domain code.

import string, sys

seq = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-'

def decode(s):
    s = map(lambda x: string.index(seq, x), s)
    l = len(s) % 4
    if l:
        if l == 1: raise ValueError()
        l = 4-l
        s.extend([0]*l)
    r = ''
    while s:
        n = ((s[0] << 6 | s[1]) << 6 | s[2]) << 6 | s[3]
        r = r + chr((n >> 16) ^ 67) + chr((n >> 8 & 255) ^ 67) + chr((n & 255) ^ 67)
        s = s[4:]
    return l and r[:-l] or r

def cc(s):
    return string.join(map(lambda x: '%02d'%(ord(x) ^ 0x20), s), ' ')

def do(s):
    s = filter(lambda x: x and x[0] > ' ', string.split(s, '.'))
    s = map(decode, s)
    if len(s) == 3:
        print 'Serial: '+s[0]
        print 'Type: '+s[1]
        if s[1] == 'CC!':
            print 'Code: C 01 '+cc(s[2])
        else:
            print 'Code: '+s[2]
    else:
        for x in s: print x

if __name__ == '__main__':
    if len(sys.argv) > 1:
        do(sys.argv[1])
    else:
        while 1:
            try:
                s = raw_input('Scan/Enter> ')
            except EOFError:
                break
            if not s: break
            try:
                do(s)
            except ValueError:
                print 'Invalid input'