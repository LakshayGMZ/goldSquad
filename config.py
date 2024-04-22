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

    # ==========================
    # Message IDs

    def getMessageIds(self):
        return self.data["messageIds"]

    def addMessageIds(self, messageID: str):
        if messageID not in self.getMessageIds():
            self.getMessageIds().append(messageID)
            self._save_data()
            return True
        else:
            return False

    def removeMessageIds(self, messageID: str):
        if messageID in self.getMessageIds():
            self.getMessageIds().remove(messageID)
            self._save_data()
            return True
        else:
            return False

    def clearMessageIds(self):
        self.data["messageIds"] = []
        self._save_data()
        return True

    # ==========================
    # Lock Message Body

    def getLockedMessageBody(self):
        return self.data["lockMessageBody"]

    def setLockMessageBody(self, message: str):
        self.data["lockMessageBody"] = message
        self._save_data()
        return True

    # ==========================
    # Unlock Message Body

    def getUnlockedMessageBody(self):
        return self.data["unlockMessageBody"]

    def setUnlockMessageBody(self, message: str):
        self.data["unlockMessageBody"] = message
        self._save_data()
        return True

    # ==========================
    # Lock Time

    def getLockTime(self):
        return self.data["lockTime"]

    def setLockTime(self, lockTime: str):
        self.data["lockTime"] = lockTime
        self._save_data()
        return True

    # ==========================
    # Unlock Time

    def getUnlockTime(self):
        return self.data["unlockTime"]

    def setUnlockTime(self, unlockTime: str):
        self.data["unlockTime"] = unlockTime
        self._save_data()
        return True

    # ==========================
    # locked Channels' ids

    def getLockedChannels(self):
        return self.data["lockedChannels"]

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

