from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    poster_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    date = models.DateField()
    time = models.TimeField()
    hall = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.movie.title} - {self.date} {self.time}"
class Seat(models.Model):
    ROW_CHOICES = [(chr(i), chr(i)) for i in range(ord('A'), ord('J') + 1)]  # A–J
    NUMBER_CHOICES = [(i, str(i)) for i in range(1, 11)]  # 1–10

    row = models.CharField(max_length=1, choices=ROW_CHOICES)
    number = models.IntegerField(choices=NUMBER_CHOICES)

    def __str__(self):
        return f"{self.row}{self.number}"

class Booking(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user.username} on {self.showtime}"
