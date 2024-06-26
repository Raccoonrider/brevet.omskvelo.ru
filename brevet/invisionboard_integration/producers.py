import os
import json
import re
import logging
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from base64 import b64encode

from django.template.loader import render_to_string
from django.utils.timezone import now, timedelta
from django.contrib.sites.models import Site
from django.conf import settings

from brevet_database.models import Event, Result, DEFAULT_CLUB_ID

API_KEY = os.environ.get('INVISION_API_KEY')


class BaseProducer:
    site = Site.objects.get_current()

    def post(self, url:str, query:str):

        auth_str = b64encode(f"{API_KEY}:".encode('ascii'))

        request = Request(url=f"{url}?{query}", data=b'', method='POST')
        request.add_header("Authorization", "Basic %s" % auth_str.decode('ascii'))  
        request.add_header("Content-Length", "0")
        request.add_header("Host", settings.INVISIONBOARD_HOST)
        request.add_header("User-Agent", "HTTPie")

        try:
            return urlopen(request)
        except Exception:
            logging.exception("Could not POST data to forum")


class PostEventProducer(BaseProducer):
    def post_upcoming_events(self):
        upcoming_events = Event.objects.filter(
            finished=False, 
            club=DEFAULT_CLUB_ID,
            omskvelo_xref='',
            date__lt=now()+timedelta(days=14),
            date__gt=now()
            )
        for event in upcoming_events:
            response = self.post_event_topic(event)
            response_body = json.loads(response.read().decode())
            event.omskvelo_xref = response_body['url']
            event.save()

    def post_event_topic(self, event:Event):
        url = "https://" + settings.INVISIONBOARD_HOST + "/api/forums/topics"
        forum = 54
        template = "invisionboard_integration/forum_topic.html"

        title = str(event)
        context = {
            'site': self.site.name,
            'event': event
        }
        data = render_to_string(template, context)
        data = re.sub(" {2,}", "", data) # Remove extra spaces to avoid HTTP414 URL too long

        query = urlencode({
            'forum': forum,
            'title': title,
            'post': data,
            'author': settings.INVISIONBOARD_AUTHOR,
        })

        return self.post(url, query)
    

    def post_event_results(self, event:Event):
        url = "https://" + settings.INVISIONBOARD_HOST + "/api/forums/posts"
        template = "invisionboard_integration/forum_results.html"

        results = Result.objects.filter(event=event).order_by("randonneur__russian_surname","randonneur__russian_name")
        topic = event.omskvelo_xref.split("-")[0].replace("https://" + settings.INVISIONBOARD_HOST + "/topic/", "")
        context = {
            'site': self.site.name,
            'event': event,
            'results': results,
        }
        data = render_to_string(template, context)     
        data = re.sub(" {2,}", "", data) # Remove extra spaces to avoid HTTP414 URL too long

        query = urlencode({
            'topic': int(topic),
            'author': settings.INVISIONBOARD_AUTHOR,
            'post': data,
        })

        return self.post(url, query)


    def post_event_to_calendar(self, event:Event):
        url = "https://" + settings.INVISIONBOARD_HOST + "/api/calendar/events"
        calendar = 6
        template = "invisionboard_integration/forum_topic.html"

        title = str(event)
        context = {
            'site': self.site.name,
            'event': event
        }
        data = render_to_string(template, context)
        data = re.sub(" {2,}", "", data) # Remove extra spaces to avoid HTTP414 URL too long

        query = urlencode({
            'calendar': calendar,
            'title': title,
            'description': data,
            'start': event.date.isoformat(),
            'author': settings.INVISIONBOARD_AUTHOR,
        })

        return self.post(url, query)