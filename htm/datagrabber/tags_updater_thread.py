# -*- coding: utf-8 -*-
import threading
import Queue
from .insta_grabber import *
from ..config import *
import calendar
from ..db.models import *

class TagsUpdaterThread(threading.Thread):
    def __init__(self, areas_queue, db_lock):
        super(TagsUpdaterThread, self).__init__()
        self.queue = areas_queue
        self.db_lock = db_lock
        self.grabber = self.__get_grabber()
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        while not self.stopped():
            try:
                area = self.queue.get(timeout=1)
                if not self.__pass_everything:
                    print "Areas left: {0}".format(self.queue.qsize())
            except Queue.Empty:
                continue

            try:
                if not self.__pass_everything:
                    self.update_tags_for_area(area)
                self.queue.task_done()
            except:
                print "Area {0} is not processed".format(area.id)
                self.queue.put(area)
                if not self.__change_client():
                    self.__pass_everything = True
                    print "Instagram banned me :("
            finally:
                pass

    __pass_everything = False
    __current_client = 0

    def __get_grabber(self):
        return InstaGrabber(LOGINS[self.__current_client]['CLIENT_ID'], \
            LOGINS[self.__current_client]['CLIENT_SECRET'])

    def __change_client(self):
        self.__current_client += 1
        if len(LOGINS) <= self.__current_client:
            return False
        else:
            self.grabber = self.__get_grabber()
            return True

    def update_tags_for_area(self, area_hour):
        area = area_hour.area
        max_stamp = calendar.timegm(area_hour.max_stamp.timetuple())
        min_stamp = calendar.timegm(area_hour.min_stamp.timetuple())

        tags = self.grabber.find_tags((area.latitude, area.longitude), area.radius, \
            max_stamp, min_stamp)

        for tag_name in tags:
            self.db_lock.acquire()
            hashtag = Hashtag.get_or_create(name=tag_name)
            self.db_lock.release()
            HashtagFrequency.create(area_in_hour=area_hour, hashtag=hashtag, count=tags[tag_name])

        area_hour.processed = datetime.datetime.now()
        area_hour.save()

        print "+++ {2} tags for area {0} of {1} updated".format(area.id, area.location.name, area_hour.hashtag_counts.count())
