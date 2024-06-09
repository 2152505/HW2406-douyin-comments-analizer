class Response():
    def __init__(self, status, content, error=""):
        self.status = status
        self.content = content
        self.error = error

    def is_error(self):
        return self.status == "error"

    def to_dict(self):
        return {
            "status": self.status,
            "content": self.content,
            "error": self.error
        }
