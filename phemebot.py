#!/usr/bin/env python3

import json
import time
import praw
import sys

r = praw.Reddit('PHEME content monitor. www.pheme.eu')

already_done = set([])
i = 0

username = None
if len(sys.argv) > 1:
    username, password = open(sys.argv[1], 'r').read().strip().split('\n')

while True:
    if username:
        r.login(username, password, disable_warning=True)
    else:
        r.login(disable_warning=True)
    subreddit = r.get_subreddit('all')
    
    try:
        while True:
            for submission in subreddit.get_new(limit=1000):
                op_text = submission.selftext.lower()
                has_praw = True
                #has_praw = any(string in op_text for string in prawWords)
                # Test if it contains a PRAW-related question
                if submission.id not in already_done and has_praw:
                    post = {}

                    for attrib in ('approved_by', 'archived', 'author', 'author_flair_css_class', 'author_flair_text', 'banned_by', 'clicked', 'created', 'created_utc', 'distinguished', 'domain', 'downs', 'edited', 'from_id', 'from_kind', 'fullname', 'gilded', 'has_fetched', 'hidden', 'id', 'json_dict', 'likes', 'link_flair_css_class', 'link_flair_text', 'locked', 'media', 'media_embed', 'mod_reports', 'name', 'num_comments', 'num_reports', 'over_18', 'permalink', 'removal_reason', 'report_reasons', 'score','secure_media', 'secure_media_embed', 'selftext', 'short_link', 'stickied', 'subreddit_id', 'suggested_sort', 'thumbnail', 'title', 'url', 'user_reports', 'visited'):
                        post[attrib] = eval("submission."+attrib)
                        pass
                    post['subreddit'] = str(submission.subreddit)
                    post['author'] = str(submission.author)
                    
                    msg = '%s %05d %s %20s %s\n' % (time.strftime('%c'), i, submission.short_link, submission.subreddit, submission.title)
                    i+=1 
                    sys.stderr.write(msg)
                    try:
                        sys.stdout.write(json.dumps(post) + "\n")
                    except Exception as e:
                        sys.stderr.write(str(e) + "\n")
                        sys.stderr.write(post)
                        sys.exit()
                    already_done.add(submission.id)
            time.sleep(10)
    except Exception as e:
        pass
        sys.stderr.write(str(e) + "\n")
        sys.stderr.write(post)
        if not username:
            sys.exit('No credentials specified, aborting')


