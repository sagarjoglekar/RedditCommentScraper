#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
"""
Description:
    1. Scrape all comments from a given reddit thread
    2. Extract top level comments
    3. Save to a csv file

Author:
    Copyright (c) Ian Hussey 2016 (ian.hussey@ugent.be) 
    Released under the MIT liscence.

Known issues:
    None. 

Notes:
    1. Although the script only uses publiclly available information, 
    PRAW's call to the reddit API requires a reddit login (see line 46).
    2. Reddit API limits number of calls (1 per second IIRC). 
    For a large thread (e.g., 1000s of comments) script execution time may therefore be c.1 hour.
    3. Because of this bottleneck, the entire data object is written to a pickle before anything is discarded. 
    This speeds up testing etc.
    4. Does not extract comment creation date (or other properties), which might be useful. 
"""

# Dependencies
import praw
import csv
import os
import sys

# Set encoding to utf-8 rather than ascii, as is default for python 2.
# This avoids ascii errors on csv write.
reload(sys)
sys.setdefaultencoding('utf-8') 

# Change directory to that of the current script
absolute_path = os.path.abspath(__file__)
directory_name = os.path.dirname(absolute_path)
os.chdir(directory_name)

# Acquire comments via reddit API
r = praw.Reddit('Comment Scraper 1.0 by u/_Daimon_ see '
    'https://praw.readthedocs.org/en/latest/'
    'pages/comment_parsing.html')
r.login('USERNAME', 'PASSWORD', disable_warning=True) # change these to your login details
submission = r.get_submission(submission_id='4e8oip') # unique ID for the submission
submission.replace_more_comments(limit=None, threshold=0)  # all comments, not just first page

# Save object to pickle
output = open('scraped_data.pkl', 'wb')
pickle.dump(submission, output, -1)
output.close()

## Load object from pickle
#pkl_file = open('scraped_data.pkl', 'rb')
#submission = pickle.load(pkl_file)
##pprint.pprint(submission)
#pkl_file.close()

# Extract first level comments only
forest_comments = submission.comments  # get comments tree
already_done = set()
top_level_comments = []
for comment in forest_comments: 
    if not hasattr(comment, 'body'):  # only comments with body text
        continue
    if comment.is_root:  # only first level comments
        if comment.id not in already_done:
            already_done.add(comment.id)  # add it to the list of checked comments
            top_level_comments.append([comment.body])  # append to list for saving
            #print(comment.body)

# Save comments to disk
with open("output.csv", "wb") as output:
    writer = csv.writer(output)
    writer.writerows(top_level_comments)
