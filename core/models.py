from django.db import models

class SiteSetting(models.Model):
    """
    Stores global site settings, such as site name, contact email, or announcements.
    """
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(blank=True)

    def __str__(self):
        return f"{self.key}: {self.value[:50]}"

class ContactMessage(models.Model):
    """
    Stores messages sent via the contact form.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} - {self.subject[:30]}"
