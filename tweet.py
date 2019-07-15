class Tweet:
    def __init__(self, tweepy_tweet, verbose):
        self.id = tweepy_tweet.id
        self.text = tweepy_tweet.full_text
        self.original = tweepy_tweet
        self.verbose = verbose

    def __str__(self):
        if self.verbose < 3:
            return self.text
        text = ""
        for k in vars(self):
            if k[0] == '_':
                continue
            if k == 'original':
                text += '{}\n'.format(vars(self)[k])
                continue
            text += "{} = {}\n".format(k, vars(self)[k])
        return text

    def hashtag_texts(self):
        return [ht['text'] for ht in self.original.entities['hashtags']]

    def author(self):
        return self.original.author

    def quoted_status_id(self):
        if 'quoted_status_id' in vars(self.original):
            return self.original.quoted_status_id
        return None

    def in_reply_id(self):
        return self.original.in_reply_to_status_id

    def is_retweet(self):
        """
        Checks if this tweet is a pure retweet. It is not clear if this doesn't
        maybe find commented retweets.
        """
        return 'retweeted_status' in vars(self.original) and self.original.retweeted_status

    def is_mention(self, bot):
        """
        Checks if the bot is included in the user mentions of this tweet.
        """
        for um in self.original.entities['user_mentions']:
            if um['screen_name'] == bot.screen_name:
                return True
        return False

    def is_explicit_mention(self, bot):
        """
        Checks if this tweet explicitly mentions the given bot.  This means
        that there hasn't only been a reply to something the bot tweeted or
        somthing that itself has mentioned the bot.
        
        We distinguish these by the display_text_range: If the bot's mention is
        within the displayed text, then we assume that the original author
        meant to explicitly include the bot.
        
        It is not clear yet how this behaves if someone explicitly mentions the
        bot in a tweet that would also have implicitly mentioned it.
        """
        for um in self.original.entities['user_mentions']:
            if um['screen_name'] == bot.screen_name:
                return (um['indices'][0] >= self.original.display_text_range[0]
                    and um['indices'][1] <= self.original.display_text_range[1])
        return False

    def has_hashtag(self, tag, **kwargs):
        """
        Checks if the given hashtag is in the tweet.
        """
        lowtag = tag.lower()
        alllower = ('case_sensitive' in kwargs and not kwargs['case_sensitive'])
        for ht in self.original.entities['hashtags']:
            if (
                (alllower and ht['text'].lower() == lowtag)
                or ht['text'] == tag
               ):
                return True
        return False