__author__ = 'Engineer'

#: Commissioned

from Android import Activity, Phone

# constants
DISPLAY_NAME = 'display_name'
PHOTO_URI = 'photo_uri'
CONTACT_ID = 'contact_id'


class ContactList(object):
    mockup = False
    _id = 0

    def __init__(self):
        args = [Phone.CONTENT_URI, None, None, None, None]
        self.contacts = Activity.getContentResolver().query(*args)
        self.contacts_list = {}
        self.generate_list()

    def generate_list(self):
        if not self.contacts:
            return
        while self.contacts.moveToNext():
            number = self.contacts.getString(self.contacts.getColumnIndex(Phone.NUMBER))
            name = self.contacts.getString(self.contacts.getColumnIndex(DISPLAY_NAME))
            id = self.contacts.getString(self.contacts.getColumnIndex(CONTACT_ID))
            self.contacts_list[name] = [number, self._id, str(id)]
            self._id += 1
        self.contacts.close()