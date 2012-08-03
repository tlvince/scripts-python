#!/usr/bin/env python2
# Author: Rocco Rutte
# http://permalink.gmane.org/gmane.mail.mutt.user/33576

import subprocess, re

if __name__ == '__main__':
    mail_re = re.compile(r'^[^<]+<([^>]+)>.*')
    a, p = set(), subprocess.Popen(['gpg', '--with-colons', '--list-keys'],
                                   stdout=subprocess.PIPE)
    for line in p.stdout:
        if not line.startswith('uid:'): continue
        m = mail_re.match(line.split(':')[9])
        if not m: continue
        a.add(m.groups(0)[0])
    print 'group -group gpg -addr %s' % ' '.join(a)
