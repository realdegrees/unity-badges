class Badge:
    def __init__(self, id: str, label: str):
        self.id = id
        self.label = label

    def create(self, owner: str, repo: str, args: dict) -> str:
        raise NotImplementedError("Subclasses should implement this method")