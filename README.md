To use
 * Copy 'setting.ini-backup' and rename to 'setting.ini'
 * Modify setting.ini so that it fits to your system
 * Copy 'twitter.ini-backup' and rename to 'twitter.ini'
 * Run './main.py -i'
 * Get twitter PIN id, and type it after 'verifier :' text.
 * Make it run everyday using cron.

Note
 * If 'target\_dir' or 'target\_file' contains non-ascii character, it won't upload a media and make an error. I can't do anything about this since I'm using tweepy on Python 2.7.
