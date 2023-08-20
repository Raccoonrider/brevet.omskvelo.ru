import logging

from django.core.management.base import BaseCommand

from invisionboard_integration.producers import PostEventProducer

class Command(BaseCommand):
    producer = PostEventProducer()
    def handle(self, *args, **kwargs):
        logging.info('Starting BrevetBot...')
        try:
            self.producer.post_upcoming_events()
        except Exception:
            logging.exception("BrevetBot exception")
