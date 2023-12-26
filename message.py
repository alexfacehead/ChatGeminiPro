class Message:
    def __init__(self, kind, content):
        self.kind = kind
        self.content = content

    def __str__(self):
        """
        Returns the string representation of the Message object.
        """
        kind_to_prefix = {
            'USER': 'USER: ',
            'SYSTEM': 'SYSTEM: ',
            'EXPERT_1': 'EXPERT 1: ',
            'EXPERT_2': 'EXPERT 2: ',
            'EXPERT_3': 'EXPERT 3: ',
        }
        return kind_to_prefix[self.kind] + self.content