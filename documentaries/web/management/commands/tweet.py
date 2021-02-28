import os
import tweepy
from django.core.management.base import BaseCommand, CommandError
from web.models import Documentary

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        twitter_auth_keys = {
            "consumer_key": os.getenv("CONSUMER_KEY"),
            "consumer_secret": os.getenv("CONSUMER_SECRET"),
            "access_token": os.getenv("ACCESS_TOKEN"),
            "access_token_secret": os.getenv("ACCESS_TOKEN_SECRET")
        }
        auth = tweepy.OAuthHandler(
            twitter_auth_keys['consumer_key'],
            twitter_auth_keys['consumer_secret']
        )
        auth.set_access_token(
            twitter_auth_keys['access_token'],
            twitter_auth_keys['access_token_secret']
        )
        api = tweepy.API(auth)

        documentaries = Documentary.objects.filter(tweeted=False).all()[:10]
        for documentary in documentaries:
            urls = "\n".join([s.url for s in documentary.sites.all()])
            tags = [f"#{t}" for t in documentary.tags]
            hashtags = " ".join(tags)
            tweet = f"""Have you see this documentary: '{documentary.title}'
see it: {urls}
{hashtags} #documentaries"""
            self.stdout.write(self.style.SUCCESS(tweet[:280]))
            try:
                api.update_status(tweet[:280])
                documentary.tweeted = True
                documentary.save()
            except tweepy.TweepError as error:
                print(str(error))