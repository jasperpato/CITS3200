class Post:
    def __init__(self, date, subject, payload, verified):
        self.date = date    # datetime.datetime object
        self.subject = subject
        self.payload = payload
        self.verified = verified

    def __str__(self):
        return f'Date: {self.date}\nSubject: {self.subject}\nVerified: {self.verified}\n\n{self.payload}\n\n'