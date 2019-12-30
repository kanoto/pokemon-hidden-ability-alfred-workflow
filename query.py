#!/usr/bin/python
# encoding: utf-8

import sys

# Workflow3 supports Alfred 3's new features. The `Workflow` class
# is also compatible with Alfred 2.
from workflow.workflow3 import Workflow3

f = './ポケモン剣盾(ソードシールド)夢特性一覧.md'

def parentheses_remover(s):
    s = s.strip()
    nobk = True
    while nobk:
        nobk = False
        if s.startswith('['):
            s = s[1:s.rfind(']')]
            nobk = True
        if s.startswith('![img]('):
            s = s[len('![img]('):s.rfind(')')]
            nobk = True
        if not nobk:
            break
    return s


def read_md(f = f):
    with open(f, 'r') as fin:
        s = fin.read()
    l = s.split('\n')[2:]
    l = [ i.split('|')[1:-1] for i in l ]
    l = [ [j.strip() for j in i] for i in l ]
    l = [ [parentheses_remover(j) for j in i] for i in l ]
    return l

def get_dict():
    l = read_md()
    d = {}
    for i in l:
        if len(i) == 0:
            continue
        key = int(i[0]) if len(i[0])>0 else i[2]
        d[key] = (i[2],i[3],i[1])
    return d



def main(wf):
    # The Workflow3 instance will be passed to the function
    # you call from `Workflow3.run`.
    # Not super useful, as the `wf` object created in
    # the `if __name__ ...` clause below is global...
    #
    # Your imports go here if you want to catch import errors, which
    # is not a bad idea, or if the modules/packages are in a directory
    # added via `Workflow3(libraries=...)`
    # import somemodule
    # import anothermodule

    # Get args from Workflow3, already in normalized Unicode.
    # This is also necessary for "magic" arguments to work.
    args = wf.args
    # print(args)
    indx = int(args[0])

    # Do stuff here ...
    d = get_dict()

    # Add an item to Alfred feedback
    wf.add_item(u'{}'.format(d[indx][1].decode('utf-8')), u'{}'.format(d[indx][0].decode('utf-8')))
    # wf.add_item(u'Item title', u'Item subtitle {}'.format(indx))

    # Send output to Alfred. You can only call this once.
    # Well, you *can* call it multiple times, but subsequent calls
    # are ignored (otherwise the JSON sent to Alfred would be invalid).
    wf.send_feedback()


if __name__ == '__main__':
    # Create a global `Workflow3` object
    wf = Workflow3()
    # Call your entry function via `Workflow3.run()` to enable its
    # helper functions, like exception catching, ARGV normalization,
    # magic arguments etc.
    sys.exit(wf.run(main))