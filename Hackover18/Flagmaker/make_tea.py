import sys

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
    # n = int(n)
    wrds = text.split()
    if n-1 < len(wrds):
        return ' '.join(wrds[n-1])
    return ''


def wordlist(s, e, text):
    # Return all words starting with s ending with e inclusive.
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
'''
def filter(pattern, text):
    return ' '.join([w for w in text.split() if w == pattern])

def filter_out(pattern, text):
    return ' '.join([w for w in text.split() if w != pattern])

'''
def filter_out(*args):
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
    return subst('-', '- ', subst('+', '+ ', p1))


def b(p1, p2):
    '''
    b =$(or
         $(if $(filter +, $(strip $(1))), $(2) +),
         $(if $(filter -, $(strip $(1))), $(wordlist 2, $(words $(2)), $(2))),
         $(if $(filter N, $(strip $(1))), $(2))
    )
    '''
    if filter('+', strip(p1)):
        return '{} +'.format(p2)
    elif filter('-', strip(p1)):
        return wordlist(2, words(p2), p2)
    elif filter('N', strip(p1)):
        return p2
    return ''


def c(p1, p2):
    # c=$(if $(word 1,$(1)),
    #       $(if $(word $(words $(1)),$(2)),$(2),$(2) -),
    #       - $(2)
    #     )
    if word(1, p1):
        if word(words(p1), p2):
            return p2
        return '{} -'.format(p2)
    return '- {}'.format(p2)


def d(p1):
    # d=$(if $(filter-out -,$(1)),,+)
    if filter_out('-', p1):
        return ''
    return '+'


def e(p1, p2, p3):
    # e=$(call a,
    #           $(filter $(subst $(call a) ,,$(strip $(1))$(strip $(2)))%,
    #                    $(3)))
    _p2 = p3
    _p1 = filter(
            subst(
                '{} '.format(a('')),
                '',
                '{}{}'.format(strip(p1), strip(p2))
            )+'%',
            _p2
        )
    return a(_p1)


def f(p1):
    # f=$(wordlist 7,$(words $(1)),$(1))
    return wordlist(7, words(p1), p1)


def g(p1, p2):
    # g=$(call b,$(word 6,$(1)), $(2))
    return b(word(6, p1), p2)


def h(p1, p2, p3):
    # h=$(wordlist 1,
#                  $(words
#                    $(wordlist 2,$(words $(2)),$(2))
#                    ),
#                  $(3)
#        ) $(word 5,$(1)) $(wordlist $(words $(2) -),$(words $(3)),$(3))
    r1 = wordlist(1, words(wordlist(2, words(p2), p2)), p3)
    r2 = word(5, p1)
    r3 = wordlist(words(p2+' -'), words(p3), p3)
    return '{} {} {}'.format(r1, r2, r3)


def i(p1, p2):
    # i=$(or $(call g,$(1),$(2)),+)
    r1 = g(p1, p2)
    if r1:
        return r1
    return '+'


def j(p1, p2):
    # j=$(word $(words $(1)), $(2))
    return word(words(p1), p2)

def k(p1, p2, p3, p4, p5):
    # k=$(call l,
    #       $(call f, $(1)),
    #       $(call i, $(1), $(3)),
    #       $(call c,
    #           $(call g, $(1), $(3)),
    #           $(call h, $(1), $(3), $(4))),
    #       $(5)
    #    )
    _p1 = f(p1)
    _p2 = i(p1, p3)
    _p3 = c(g(p1, p3),
            h(p1, p3, p4))
    _p4 = p5
    return l(_p1, _p2, _p3, _p4)

def l(p1, p2, p3, p4):
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
    print('{} {} {} {}'.format(p1,p2,p3,p4))
    if d(m(p1)):
        return words(filter('+', p3))
    _p1 = e(m(p1), j(p2,p3), p4)
    _p2 = m(p)
    _p3,_p4,_p5 = p2,p3,p4
    return k(_p1, _p2, _p3, _p4, _p5)


def m(p1):
    # m=$(word 1,$(1)) $(or $(word 2,$(1)),+) $(or $(word 3,$(1)),-)
    r1 = word(1, p1)
    t = word(2, p1)
    r2 = t if t else '+'
    t = word(3, p1)
    r3 = t if t else '-'
    return '{} {} {}'.format(r1, r2, r3)


n = '+'
o = '+'
p = '-'
q = '++--+++++ ++-+-+--+ +++---++- ++++-+-++ --+-++-++ --+++++-- -++-+--+- -+++---++ -+--+++-+ -+-++-+++ +-+-++++- +-++++-+- +---++--- +--++-+--'
r = [-48, 2, -48, -8, -59, -18, 1, -59, 3, -5, -26, -57, 53, 3, -43, -3, -41, -20, 1, -64, -65, -45, -71, -47, -16, -47,
     -38, -3, 46, -63, -54, 1, -49, 4, -51, -45, -61, -46, -13, -4, -65, -48, -55, -51, -38, -64, -50, -5, -65, 2, -54,
     -56, -1, -50, -28]

if __name__ == '__main__':
    # sys.setrecursionlimit(7500)
    # flag: @echo $(call l, $(o), $(n), $(p), $(q)) | sha256sum | python -c "import sys; print ''.join([chr(ord(c) - d) for c,d in zip(sys.stdin.read(),$(r))])" | tee $@
    r1 = l(o, n, p, q)
    from hashlib import sha256
    msg = sha256()
    msg.update(r1)
    r2 = msg.digest()
    print(''.join([chr(ord(c) - d) for c, d in zip(r2,r)]))

