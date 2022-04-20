class Test:
    def __init__(self):
        self._attr = "original value"
        # This will trigger an error...
        # self.attr = "new value"

    @property
    def attr(self):
        return self._attr


test = Test()
print(test.attr)
print(test.attr())


def save(self, *args, **kwargs):
    if not self.id and not self.picture:
        print('coucou')
        return

    thumb = self.thumb
    picname, picext = os.path.splitext(self.picture.path)
    picname = picname + '_thumb'
    picpath = picname + picext
    print('picture path:', self.picture.path)
    print('picpath:', picpath)

    thumb._path = picpath
    self._thumb = thumb
    super(Photo, self).save(*args, **kwargs)

