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

    def getLockedMessageBody(self):
        return self.data["lockMessageBody"]

    def getUnlockedMessageBody(self):
        return self.data["unlockMessageBody"]

    def getLockTime(self):
        return self.data["lockTime"]

    def getUnlockTime(self):
        return self.data["unlockTime"]

    def addLockedChannels(self, channelID: str):
        if channelID not in self.getLockedChannels():
            self.getLockedChannels().append(channelID)
            self._save_data()
            return True
        else:
            return False

    def removeLockedChannels(self, channelID: str):
        if channelID in self.getLockedChannels():
            self.getLockedChannels().remove(channelID)
            self._save_data()
            return True
        else:
            return False

    def clearLockedChannels(self):
        self.data["lockedChannels"] = []
        self._save_data()
        return True

    def setLockMessageBody(self, message: str):
        self.data["lockMessageBody"] = message
        self._save_data()
        return True

    def setUnlockMessageBody(self, message: str):
        self.data["unlockMessageBody"] = message
        self._save_data()
        return True

    def setLockTime(self, lockTime: str):
        self.data["lockTime"] = lockTime
        self._save_data()
        return True

    def setUnlockTime(self, unlockTime: str):
        self.data["unlockTime"] = unlockTime
        self._save_data()
        return True
