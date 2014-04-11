import datetime


class TimeFormatter(object):

    @staticmethod
    def time_ago(timestamp):
        current_ts = datetime.datetime.now()

        post_ts = datetime.datetime.fromtimestamp(timestamp)
        delta = current_ts - post_ts
        minutes = delta.seconds / 60
        if minutes > 0:
            return "{} minut{} ago".format(minutes, "es" if minutes != 1 else "e")
        else:
            return "{} second{} ago".format(delta.seconds, "s" if delta.seconds != 1 else "")