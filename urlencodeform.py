from urllib import parse

class UrlEncodeForm():
    def __init__(self):
        self.form_fields = []
        return
    
    def get_content_type(self):
        return 'application/x-www-form-urlencoded'

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        self.form_fields.append((name, value))
        return
    def convert_to_dict(self):
        """Convert form fields list to a dictionary."""
        self.form_dict = dict(self.form_fields)
        return

    def make_result(self):
        self.form_data = parse.urlencode(self.form_fields).encode()
