import json


class DataStorage:
    def __init__(self, filename="config.json"):
        self.filename = filename
        self.data = self.load_data()

    def refresh(self):
        self.__init__(self.filename)

    def load_data(self):
        with open(self.filename, 'r') as file:
            return json.loads(file.read())

    def _save_data(self):
        with open(self.filename, 'w') as file:
            file.write(json.dumps(self.data, indent=4))

    def create_record(self, key, value):
        self.data[key] = value
        self._save_data()
        self.refresh()
        print(f"Record with key '{key}' created.")

    def getLockedChannels(self):
        return self.data["lockedChannels"]

    def getMessageBody(self):
        return self.data["messageBody"]

    def getLockTime(self):
        return self.data["lockTime"]

    def getUnlockTime(self):
        return self.data["unlockTime"]

    def addLockedChannels(self, channelID: str):
        if channelID not in self.getLockedChannels():
            self.getLockedChannels().append(channelID)
            self._save_data()

    def removeLockedChannels(self, channelID: str):
        if channelID in self.getLockedChannels():
            self.getLockedChannels().remove(channelID)
            self._save_data()

    def clearLockedChannels(self):
        self.data["lockedChannels"] = []
        self._save_data()

    def setMessageBody(self, message: str):
        self.data["messageBody"] = message
        self._save_data()

    def setLockTime(self, lockTime: str):
        self.data["lockTime"] = lockTime
        self._save_data()

    def setUnlockTime(self, unlockTime: str):
        self.data["unlockTime"] = unlockTime
        self._save_data()
