import praw
import re


def login():
    reddit = praw.Reddit(username='',
                         password='',
                         client_id='',
                         client_secret='',
                         user_agent='')

    return reddit


def convert_word(word):
    word = re.sub('[^a-z]+', '', word)  # get plain text
    
    # find the location of men in the word
    for i in range(len(word)):
        if word[i:i+3] == "men": break
        
    end = word[i+3:]
    start = word[:i]
    return ("Not just the "+start+"men"+end+" but the "+start+"women"+
          end+" and the "+start+"children"+end+" too!")


def is_same_joke(text):
    text = text.lower()
    return 'not just the' in text and 'but the' in text and 'and the' in text and 'too' in text


def joke_already_made(comment):
    if comment.is_root: 
        return is_same_joke(comment.body)

    if is_same_joke(comment.body):
        return True

    return joke_already_made(comment.parent())


def main():
    for comment in subreddit.stream.comments():
        # ignore comments from other bots, replying to all bot messages would be annoying
        if 'bot' in str(comment.author).lower(): continue

        comment_text = comment.body.lower()
        if 'men' in comment_text and not joke_already_made(comment):
            words = comment_text.replace('\n', ' ').split(' ')

            for word in words:
                if 'men' in word:
                    # ignore really long words that are most likely links and meta discussion
                    if len(word) > 20 or word == 'comment': continue
                    
                    reply_phrase = convert_word(word)
                    
                    # handle any api exceptions e.g. comment was deleted, connection timeout
                    try:
                        comment.reply(reply_phrase)
                    except praw.exceptions.APIException:
                        break

                    link = 'reddit.com' + comment.submission.permalink + comment.fullname[3:]
                    print('Replied to:           {}'.format(link))
                    break


subreddit = login().subreddit('prequelmemes')
main()
