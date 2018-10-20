#!/usr/bin/env python

# a -> replace '-' with '- ', replace '+' with '+ '
def a(x):
    return x.replace('-', '- ').replace('+', '+ ')

def subst(what, how, where):
    return where.replace(what, how)

def strip(s):
    return ' '.join(s.split())

def word(n, text):
    # Returns nth word in text starting from 1
    if not text:
        return ''
    words = text.split()
    if len(words)>n-1:
        return words[n-1]
    return ''

def words(ss):
    return len(ss.split()) if ss else 0

def wordlist(start, end, ss):
    if not ss:
        return ''
    # print('start={}, end={}, ss={}'.format(start,end,ss))
    return '' if end > len(ss.split()) or start > len(ss.split()) else ' '.join(ss.split()[start-1:end-1])

def b(s1, s2):
    if '+' in s1.split():
        return '{} +'.format(s2)
    if '-' in s1.split():
        return s2.split()[1:]
    if 'N' in s1.split():
        return s2
    return ''

'''
b=$(or
    $(if
        $(filter
            +,
            $(strip $(1))
        ),
        $(2) +
    ),
    $(if
        $(filter
            -,
            $(strip $(1))
        ),
        $(wordlist
            2,
            $(words $(2)),
            $(2)
        )
    ),
    $(if
        $(filter
            N,
            $(strip $(1))
        ),
        $(2)
    )
)
'''

'''
c=$(if
    $(word 1,$(1)),
    $(if
        $(word
            $(words $(1)),
            $(2)
        ),
        $(2),
        $(2) -
    ),
    - $(2)
)
'''

def c(s1, s2):
    if word(1, s1):
        if word(len(s1.split()), s2):
            return s2
        else:
            return '{} -'.format(s2)
    else:
        '- {}'.format(s2)

def filter_out(what, where):
    return ' '.join(filter(lambda a: a == what, where))

def mfilter(what, where):
    return ' '.join(filter(lambda a: a == what, where))

# d=$(if $(filter-out -,$(1)),,+)
def d(ss):
    return '' if filter_out('-', ss) else '+'

'''
e=$(call
        a,
        $(filter
            $(subst
                $(call a) ,
                ,
                $(strip $(1))$(strip $(2))
            )%,
            $(3)
        )
    )
'''

def e(s1, s2, s3):
    return a(
        mfilter(
            '{}%'.format(subst(
                ' ',
                '',
                '{}{}'.format(
                    strip(s1),
                    strip(s2)
                )
            )),
            s3
        )
    )

# g=$(call b,$(word 6,$(1)), $(2))
# i=$(or $(call g,$(1),$(2)),+)
# j=$(word $(words $(1)), $(2))

# f=$(wordlist 7,$(words $(1)),$(1))
def f(ss):
    return wordlist(7, words(ss), ss)

def g(s1, s2):
    arg1 = word(6, s1) if len(s1.split()) <= 6 else ''
    return b(arg1, s2)

'''
h=$(wordlist
    1,
    $(words
        $(wordlist
            2,
            $(words $(2)),
            $(2)
        )
    ),
    $(3)
) $(word 5,$(1)) $(wordlist
    $(words $(2) -),
    $(words $(3)),
    $(3)
)
'''

def h(s1, s2, s3):
    return '{} {} {}'.format(
        wordlist(
            1,
            words(
                wordlist(2, words(s2), s2)
            ),
            s3
        ),
        word(5, s1),
        wordlist(
            words(s2)+1,
            words(s3),
            s3
        )
    )

def i(s1, s2):
    res = [g(s1, s2), '+']
    for idx in range(0, len(res)):
        if res[idx]:
            return res[idx]
    return ''

# j=$(word $(words $(1)), $(2))
def j(s1, s2):
    return word(
        words(s1),
        s2
    )

'''
k=$(call
    l,
    $(call f, $(1)),
    $(call i, $(1), $(3)),
    $(call c,
        $(call g, $(1), $(3)),
        $(call h, $(1), $(3), $(4))
    ),
    $(5)
)
'''

def k(s1, s2, s3, s4, s5):
    return l(
        f(s1),
        i(s1, s3),
        c(
            g(s1, s3),
            h(s1, s3, s4)
        ),
        s5
    )

'''
l=$(if
        $(call
            d,
            $(call m,$(1))
        ),
        $(words $(filter +,$(3))),
        $(call
            k,
            $(call
                e,
                $(call m,$(1)),
                $(call j,$(2),$(3)),
                $(4)
            ),
            $(call
                m,
                $(1)
            ),
            $(2),
            $(3),
            $(4)
        )
    )
'''

def l(s1, s2, s3, s4):
    print('{} {} {} {}'.format(s1,s2,s3,s4))
    if d(m(s1)):
        return words(mfilter('+',s3))
    else:
        return k(
            e(
                m(s1),
                j(s2,s3),
                s4
            ),
            m(s1),
            s2,
            s3,
            s4
        )

# m=$(word 1,$(1)) $(or $(word 2,$(1)),+) $(or $(word 3,$(1)),-)
def m(ss):
    return '{} {} {}'.format(
        ss.split()[0] if ss.split() else '',
        '+' if not len(ss.split()) > 1 else word(2, ss),
        '-' if not len(ss.split()) > 2 else word(3, ss)
    )

if __name__ == '__main__':
    print(l(
        '+',
        '+',
        '-',
        '++--+++++ ++-+-+--+ +++---++- ++++-+-++ --+-++-++ --+++++-- -++-+--+- -+++---++ -+--+++-+ -+-++-+++ +-+-++++- +-++++-+- +---++--- +--++-+--'
    ))
