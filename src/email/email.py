import os

from flask import current_app
from jinja2 import Template


class Email:
    '''Custom class to deal with HTML emails using jinja2'''
    
    TEMPLATES: str
    CONFIRM_EMAIL: str
    RESET_PASSWORD: str

    def __init__(self) -> None:
        self.TEMPLATES = current_app.config["EMAIL_TEMPLATES"]
        self.CONFIRM_EMAIL = os.path.join(self.TEMPLATES, "confirm_email.html")
        self.RESET_PASSWORD = os.path.join(self.TEMPLATES, "reset_password.html")

    @classmethod
    def render_message_body(self, template: str, **kwargs):
        with open(template, encoding='utf-8') as f:
            body = f.read()
        
        template: Template = Template(source=body)

        return template.render(**kwargs)

