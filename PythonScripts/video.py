import os

class Video(object):
    def __init__(self, videofile):
        self.videofile = videofile
        self.videopath = os.path.dirname(os.path.abspath(videofile))
        self.videoname = videofile[len(self.videopath)+1:]

    def name(self):
        return self.videoname

    def file(self):
        return self.videofile

    def path(self):
        return self.videopath

    def isEmpty(self):
        if self.videofile == '':
            return True
        return False

    def isInvalid(self):
        if self.videofile[-3:] not in ['mp4', 'avi']:
            return True
        return False
