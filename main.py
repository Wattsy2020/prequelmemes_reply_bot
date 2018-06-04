import praw
import time


def login():
    reddit = praw.Reddit(username='',
                         password='',
                         client_id='',
                         client_secret='',
                         user_agent='')

    return reddit

def convert_word(word):
    # find the location of men in the word
    for i in range(len(word)):
        if word[i:i+3] == "men": break
        
    end = word[i+3:]
    start = word[:i]
    return ("Not just the "+start+"men"+end+" but the "+start+"women"+
          end+" and the "+start+"children"+end+" too!")


def main():
    for comment in subreddit.stream.comments():
        # ignore the bots own comments
        if comment.author == 'InclusiveMemer': continue
        # ignore comments from other bots, replying to all bot messages would be annoying
        if 'bot' in str(comment.author).lower(): continue

        comment_text = comment.body.lower()
        if 'men' in comment_text:
            words = comment_text.split(' ')

            for word in words:
                if 'men' in word:
                    # ignore really long words, most likely links
                    if len(word) > 20: break
                    
                    reply_phrase = convert_word(word)

                    # if someone already made the same joke don't repeat it
                    if reply_phrase in comment_text: break
                    
                    # if ratelimited wait and then rety
                    try:
                        comment.reply(reply_phrase)
                    except praw.exceptions.APIException:
                        time.sleep(600)
                        comment.reply(reply_phrase)

                    link = 'reddit.com' + comment.submission.permalink + comment.fullname[3:]
                    print('Replied to:           {}'.format(link))
                    break


subreddit = login().subreddit('prequelmemes')
main()
