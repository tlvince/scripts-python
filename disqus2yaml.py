#!/usr/bin/env python2
# Copyright 2012 Tom Vincent <http://tlvince.com/contact>

'''Convert Disqus comments to yaml.

Uses the Disqus API to convert comments into Jekyll-compliant yaml files.
Formats the comment message as markdown using "html2text". Tries to create a
directory structure based on the threads pathname.

Note: this is messy, incomplete and far from robust.
'''

import os
import argparse
import collections

from urlparse import urlparse
from disqusapi import DisqusAPI
from html2text import html2text

def parse_args():
    '''Parse the command-line arguments.'''
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('secret_key',
        help='Disqus API secret key')
    parser.add_argument('public_key',
        help='Disqus API public key')
    parser.add_argument('forum',
        help='Disqus forum (short URL)')
    parser.add_argument('-o', '--output', default='.',
        help='Output directory')
    return parser.parse_args()

def main():
    '''Start execution of disqus2yaml.'''
    args = parse_args()

    disqus  = DisqusAPI(args.secret_key, args.public_key)
    disqus_threads = disqus.threads.list(forum=args.forum)
    posts   = disqus.posts.list(forum=args.forum)

    threads = {}
    for thread in disqus_threads:
        link = urlparse(thread['link'])
        out = args.output + link.path
        threads[thread['id']] = {'path': out}
        os.makedirs(out)

    for post in posts:
        meta = collections.OrderedDict()
        meta['name'] = post['author']['name']
        meta['date'] = post['createdAt']

        for i in ['email', 'url']:
            if i in post['author'] and post['author'][i] != '':
                meta[i] = post['author'][i]

        yaml = '\n'.join(['{0}: {1}'.format(k, v) for (k, v) in meta.items()])
        html = post['message'].encode('ascii', 'ignore')
        message = html2text(html).strip('\n\n')
        comment = '---\n{0}\n---\n\n{1}\n'.format(yaml, message)

        thread = post['thread']
        if thread in threads:
            path = threads[thread]['path']
            index = threads[thread]['count'] if 'count' in threads[thread] else 0
            output = os.path.join(path, '{0:02d}.mkd'.format(index))

            with open(output, mode='w') as comment_file:
                comment_file.write(comment)

            threads[thread]['count'] = index + 1

if __name__ == '__main__':
    main()

