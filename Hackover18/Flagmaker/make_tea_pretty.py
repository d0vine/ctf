import sys
from collections import namedtuple

"""
a=$(subst -,- ,$(subst +,+ ,$(1)))
b=$(or $(if $(filter +,$(strip $(1))),$(2) +),$(if $(filter -,$(strip $(1))),$(wordlist 2,$(words $(2)),$(2))),$(if $(filter N,$(strip $(1))),$(2)))
c=$(if $(word 1,$(1)),$(if $(word $(words $(1)),$(2)),$(2),$(2) -),- $(2))
d=$(if $(filter-out -,$(1)),,+)
e=$(call a,$(filter $(subst $(call a) ,,$(strip $(1))$(strip $(2)))%,$(3)))
f=$(wordlist 7,$(words $(1)),$(1))
g=$(call b,$(word 6,$(1)), $(2))
h=$(wordlist 1,$(words $(wordlist 2,$(words $(2)),$(2))),$(3)) $(word 5,$(1)) $(wordlist $(words $(2) -),$(words $(3)),$(3))
i=$(or $(call g,$(1),$(2)),+)
j=$(word $(words $(1)), $(2))
k=$(call l,$(call f, $(1)),$(call i, $(1), $(3)),$(call c,$(call g, $(1), $(3)),$(call h, $(1), $(3), $(4))),$(5))
l=$(if $(call d,$(call m,$(1))),$(words $(filter +,$(3))),$(call k,$(call e, $(call m,$(1)), $(call j,$(2),$(3)),$(4)),$(call m,$(1)),$(2),$(3),$(4)))
m=$(word 1,$(1)) $(or $(word 2,$(1)),+) $(or $(word 3,$(1)),-)

n = +
o = +
p = -
q = ++--+++++ ++-+-+--+ +++---++- ++++-+-++ --+-++-++ --+++++-- -++-+--+- -+++---++ -+--+++-+ -+-++-+++ +-+-++++- +-++++-+- +---++--- +--++-+--
r = [-48, 2, -48, -8, -59, -18, 1, -59, 3, -5, -26, -57, 53, 3, -43, -3, -41, -20, 1, -64, -65, -45, -71, -47, -16, -47, -38, -3, 46, -63, -54, 1, -49, 4, -51, -45, -61, -46, -13, -4, -65, -48, -55, -51, -38, -64, -50, -5, -65, 2, -54, -56, -1, -50, -28]

flag: @echo $(call l, $(o), $(n), $(p), $(q)) | sha256sum | python -c "import sys; print ''.join([chr(ord(c) - d) for c,d in zip(sys.stdin.read(),$(r))])" | tee $@
"""

######  Helper functions (look like Make functions)


def word(n, text):
    # Returns nth word in text starting from 1
    n = int(n)
    wrds = text.split()
    if n-1 < len(wrds):
        return wrds[n-1]
    return ''


def wordlist(s, e, text):
    '''
    Return all words starting with s ending with e inclusive.
    :param s: start int
    :param e: end int
    :param text: words
    :return: words between word s and e, or empty if s is too big
    '''
    s = int(s)
    e = int(e)
    wrds = text.strip().split()
    if s>len(wrds) or s>e:
        return ''
    if e>len(wrds):
        return ' '.join(wrds[s-1:])
    return ' '.join(wrds[s-1:e])


def words(text):
    return len(text.strip().split())


def filter(*args):
    result = []
    text = args[-1]
    patterns = args[:-1]
    for w in text.split():
        for pattern in patterns:
            if pattern.replace('%', '') in w:  # BAD HAX! Use re here maybe.
                result.append(w)
                break
    return ' '.join(result)


def filter_out(*args):
    '''
    Returns all whitespace-separated words in text that do not match any of the pattern words, removing the words that do match one or more. This is the exact opposite of the filter function.
    :param args:
    :type args:
    :return:
    :rtype:
    '''
    result = []
    text = args[-1]
    patterns = args[:-1]
    for w in text.split():
        for pattern in patterns:
            if pattern.replace('%', '') not in w:  # BAD HAX! Use re here maybe.
                result.append(w)
                break
    return ' '.join(result)

def strip(text):
    return text.strip()


def subst(frm, to, text):
    return text.replace(frm, to)


########### Make to Python


def a(p1):  # a=$(subst -,- ,$(subst +,+ ,$(1)))
    '''
    Adds a space after every - and +
    :param p1: text
    :return: p1 with spaces after every - and +
    '''
    return subst('-', '- ', subst('+', '+ ', p1))


def b(p1, p2):
    '''
    returns:
    p2 +    if + in p1,
    p2[1:]  if - in p1,
    p2      if N in p1,
    ''      otherwise
    :param p1: text
    :param p2: text
    :return: some variant of p2, as above
    '''
    # b =$(or
    #      $(if $(filter +, $(strip $(1))), $(2) +),
    #      $(if $(filter -, $(strip $(1))), $(wordlist 2, $(words $(2)), $(2))),
    #      $(if $(filter N, $(strip $(1))), $(2))
    # )
    if filter('+', strip(p1)):
        return '{} +'.format(p2)
    elif filter('-', strip(p1)):
        return wordlist('2', words(p2), p2)
    elif filter('N', strip(p1)):
        return p2
    return ''


def c(p1, p2):

    # c=$(if $(word 1,$(1)),
    #       $(if $(word $(words $(1)),$(2)),$(2),$(2) -),
    #       - $(2)
    #     )
    if word('1', p1):
        if word(words(p1), p2):
            return p2
        return '{} -'.format(p2)
    return '- {}'.format(p2)


def d(p1):
    '''
    If p1 consists solely of - signs then returns + else returns empty
    :param p1: text
    :return: empty or +
    '''
    # d=$(if $(filter-out -,$(1)),,+)
    if filter_out('-', p1):
        return ''
    return '+'


def e(p1, p2, p3):
    '''
    Returns a(words in p3 beginning in p1p2 where p1p2 are stripped and contain no spaces)
    :param p1: text
    :param p2: text
    :param p3: text
    :return:
    '''
    # e=$(call a,
    #           $(filter $(subst $(call a) ,,$(strip $(1))$(strip $(2)))%,
    #                    $(3)))
    result = []
    suf = (strip(p1)+strip(p2)).replace(' ', '')
    for wrd in p3.strip().split():
        if wrd.startswith(suf):
            result.append(wrd)
    return a(' '.join(result))


def f(p1):
    '''
    returns everything from word 7, or nothing if p1 has < 7 words
    :param p1: text
    :return: words, as above
    '''
    # f=$(wordlist 7,$(words $(1)),$(1))
    return wordlist('7', words(p1), p1)


def g(p1, p2):
    '''
    Returns b(p1[5], p2)
    Where b returns some modified version of p2, either 'p2 +', 'p2[1:]', 'p2', or ''
    :param p1: text with 5th word usually in {+,-,N}
    :param p2: text
    :return: as above
    '''
    # g=$(call b,$(word 6,$(1)), $(2))
    return b(word('6', p1), p2)


def h(p1, p2, p3):
    # h=$(wordlist 1,
#                  $(words
#                    $(wordlist 2,$(words $(2)),$(2))
#                    ),
#                  $(3)
#        ) $(word 5,$(1)) $(wordlist $(words $(2) -),$(words $(3)),$(3))
    r1 = wordlist('1', words(wordlist('2', words(p2), p2)), p3)
    r2 = word('5', p1)
    r3 = wordlist(words(p2+' -'), words(p3), p3)
    return '{} {} {}'.format(r1, r2, r3)


def i(p1, p2):
    '''
    Returns g(p1, p2) or +
    g gives a slightly modified p2, adds + if p1[5] is +, removes first el if p1[5] is -, p2 if it's N, otherwise ''
    :param p1: text with 5th element usually in {+,-,N}
    :param p2:
    :return: the modified g, or +
    '''
    # i=$(or $(call g,$(1),$(2)),+)
    r1 = g(p1, p2)
    if r1:
        return r1
    return '+'


def j(p1, p2):
    # j=$(word $(words $(1)), $(2))
    return word(words(p1), p2)

queue = []
FuncExec = namedtuple('FuncExec', ['func', 'args'])

def k(p1, p3, p4):
    p5 = q  # remove clunky transportation to global variable
    # k=$(call l,
    #       $(call f, $(1)),
    #       $(call i, $(1), $(3)),
    #       $(call c,
    #           $(call g, $(1), $(3)),
    #           $(call h, $(1), $(3), $(4))),
    #       $(5)
    #    )
    _p1 = f(p1)
    _p2 = i(p1, p3)  # modified p3, + if '' returned
    _p3 = c(g(p1, p3),
            h(p1, p3, p4))
    return FuncExec(l, (_p1, _p2, _p3))


def l(p1='+', p2='+', p3='-'):
    p4 = q  # remove clunky transportation to global variable
    # l=$(if $(call d,$(call m,$(1))),
    #        $(words $(filter +, $(3))),
    #        $(call k, $(call e,
    #                           $(call m, $(1)),
    #                           $(call j, $(2),$(3)),
    #                           $(4)),
    #                  $(call m, $(1)),
    #                  $(2),
    #                  $(3),
    #                  $(4))
    # )
    if d(m(p1)):
        # This passes if p1 < 3 words or the first 3 words are not - - -
        # Basically this fails iff ''.join(p1.strip().split()[:3]) != '---'
        res = words(filter('+', p3))
        print('res: {}'.format(res))
        return res
    _p1 = e(m(p1), j(p2, p3), p4)
    # _p2 = m(p1)  # Gets ignored in k()
    _p3, _p4, _p5 = p2, p3, p4
    return FuncExec(k, (_p1, _p3, _p4))
    # return k(_p1, _p3, _p4)


def m(p1):
    '''
    Returns first 3 words from p1 if they exist
    Otherwise returns empty for word1, + for word2, - for word3 wherever they don't exist
    :param p1: text
    :return: As above
    '''
    # m=$(word 1,$(1)) $(or $(word 2,$(1)),+) $(or $(word 3,$(1)),-)
    r1 = word('1', p1)
    t = word('2', p1)
    r2 = t if t else '+'
    t = word('3', p1)
    r3 = t if t else '-'
    return ' '.join([r1, r2, r3])


n = '+'
o = '+'
p = '-'
global q
q = '++--+++++ ++-+-+--+ +++---++- ++++-+-++ --+-++-++ --+++++-- -++-+--+- -+++---++ -+--+++-+ -+-++-+++ +-+-++++- +-++++-+- +---++--- +--++-+--'
r = [-48, 2, -48, -8, -59, -18, 1, -59, 3, -5, -26, -57, 53, 3, -43, -3, -41, -20, 1, -64, -65, -45, -71, -47, -16, -47,
     -38, -3, 46, -63, -54, 1, -49, 4, -51, -45, -61, -46, -13, -4, -65, -48, -55, -51, -38, -64, -50, -5, -65, 2, -54,
     -56, -1, -50, -28]

if __name__ == '__main__':
    # flag: @echo $(call l, $(o), $(n), $(p), $(q)) | sha256sum | python -c "import sys; print ''.join([chr(ord(c) - d) for c,d in zip(sys.stdin.read(),$(r))])" | tee $@
    queue.append(FuncExec(l, (o, n, p)))

    res = None
    while True:
        func_exec = queue.pop()
        res = func_exec.func(*func_exec.args)
        if type(res) == FuncExec:
            queue.append(res)
        else:
            break
    # r1 = l(o, n, p)
    from hashlib import sha256
    msg = sha256()
    msg.update(res)
    r2 = msg.digest()
    print(''.join([chr(ord(c) - d) for c, d in zip(r2, r)]))

