from django.db import models



class Turn(models.Model):
    year = models.IntegerField()
    is_autumn = models.BooleanField(default=False)
    # yes I know its dumb, but allows us to easily identify when retreats can move
    is_retreat_turn = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)