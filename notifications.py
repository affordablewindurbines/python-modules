# -*- coding: utf-8-*-
import Queue
import atexit
from modules import Gmail
from apscheduler.schedulers.background import BackgroundScheduler
import httplib
from datetime import datetime, timedelta
import logging
import json


class Notifier(object):

    class NotificationClient(object):

        def __init__(self, gather, timestamp):
            self.gather = gather
            self.timestamp = timestamp

        def run(self):
            self.timestamp = self.gather(self.timestamp)

    def __init__(self, profile):
        self._logger = logging.getLogger(__name__)
        self.q = Queue.Queue()
        self.profile = profile
        self.notifiers = []
        self.lastCheck = []

        if 'gmail_address' in profile and 'gmail_password' in profile:
            self.notifiers.append(self.NotificationClient(self.handleEmailNotifications,None))
        else:
            self._logger.warning('gmail_address or gmail_password not set ' +
                                 'in profile, Gmail notifier will not be used')

        self.notifiers.append(self.NotificationClient(self.checkForBuildFailures,None))

        sched = BackgroundScheduler(timezone="UTC", daemon=True)
        sched.start()
        sched.add_job(self.gather, 'interval', seconds=30)
        atexit.register(lambda: sched.shutdown(wait=False))

    def gather(self):
        [client.run() for client in self.notifiers]

    def handleEmailNotifications(self, lastDate):
        """Places new Gmail notifications in the Notifier's queue."""
        emails = Gmail.fetchUnreadEmails(self.profile, since=lastDate)
        if emails:
            lastDate = Gmail.getMostRecentDate(emails)

        def styleEmail(e):
            return "New email from %s." % Gmail.getSender(e)

        for e in emails:
            self.q.put(styleEmail(e))

        return lastDate

    def checkForBuildFailures(self, lastDate):
        print("Checking for build failures")
        teamCityAuth = "redacted"
        teamcityConnection = httplib.HTTPConnection("redacted-build.cloudapp.net", 80)
        teamcityConnection.connect()
        yesterday = datetime.today() - timedelta(1)
        teamcityConnection.request('GET', '/httpAuth/app/rest/buildTypes/id:Kno2_2_1aKno2ci/builds?sinceDate=' + yesterday.strftime('%Y%m%dT%H%M%S+0000') + '&locator=status:FAILURE,'
                                   'branch:(default:any)',
                                   None, {"Authorization": "Basic " + teamCityAuth, "Accept": "application/json"})
        teamCityResult = json.loads(teamcityConnection.getresponse().read())

        def announceFailure(e):
            print e
            return e

        for attribute, value in teamCityResult.iteritems():
            if attribute == "build":
                for each_dict in value[:100]:
                    buildId = each_dict.get("id")
                    buildType = each_dict.get("buildTypeId")
                    branchName = each_dict.get("branchName")
                    status = each_dict.get("status")
                    #if self.lastCheck.count(buildId) <= 0:
                        #self.q.put(announceFailure(branchName + " failed to build,"))
                    self.lastCheck.append(each_dict.get("id"))
        teamcityConnection.close()
        lastDate = yesterday
        self.q.put(announceFailure("boom"))
        return lastDate

    def getNotification(self):
        """Returns a notification. Note that this function is consuming."""
        try:
            notif = self.q.get(block=False)
            return notif
        except Queue.Empty:
            return None

    def getAllNotifications(self):
        """
            Return a list of notifications in chronological order.
            Note that this function is consuming, so consecutive calls
            will yield different results.
        """
        notifs = []

        notif = self.getNotification()
        while notif:
            notifs.append(notif)
            notif = self.getNotification()

        return notifs
