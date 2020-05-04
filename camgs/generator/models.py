from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from crum import get_current_user
import re


def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/<username>/<filename>
    return '{0}/{1}'.format(instance.user.username, filename)


# Method from https://djangosnippets.org/snippets/690/
def _slug_strip(value, separator='-'):
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
    return value


# Method from https://djangosnippets.org/snippets/690/
def unique_slugify(instance, value, slug_field_name='slug', queryset=None,
                   slug_separator='-'):
    slug_field = instance._meta.get_field(slug_field_name)
    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '%s%s' % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len-len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1
    setattr(instance, slug_field.attname, slug)


class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Composition(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(unique=True, blank=True)
    user = models.ForeignKey(
        CustomUser, default=None, on_delete=models.CASCADE
    )
    title = models.CharField(default='untitled', max_length=250)
    composer = models.CharField(default='none', max_length=250)
    tempo = models.IntegerField(default=120)
    BASE_DURATIONS = [('2', 2), ('4', 4), ('8', 8), ('16', 16)]
    base_duration = models.CharField(
        choices=BASE_DURATIONS, default='4', max_length=2
    )
    bar_beat = models.CharField(default='4', max_length=2)
    ENHARMONICS = [('sharp', 'sharp'), ('flat', 'flat')]
    enharmonic = models.CharField(
        choices=ENHARMONICS, default='sharp', max_length=5
    )

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.user = user
        slug = '%s' % (self.title)
        unique_slugify(self, slug)
        super(Composition, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug


class NoteObject(models.Model):
    id = models.AutoField(primary_key=True)
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE)
    order = models.DecimalField(
        unique=True, default=1, max_digits=10, decimal_places=1
    )
    PITCHES = [
        ('rest', 'rest'), ('C6', 'C6'),
        ('B5', 'B5'), ('A#5', 'A#5'), ('A5', 'A5'), ('G#5', 'G#5'),
        ('G5', 'G5'), ('F#5', 'F#5'), ('F5', 'F5'), ('E5', 'E5'),
        ('D#5', 'D#5'), ('D5', 'D5'), ('C#5', 'C#5'), ('C5', 'C5'),
        ('B4', 'B4'), ('A#4', 'A#4'), ('A4', 'A4'), ('G#4', 'G#4'),
        ('G4', 'G4'), ('F#4', 'F#4'), ('F4', 'F4'), ('E4', 'E4'),
        ('D#4', 'D#4'), ('D4', 'D4'), ('C#4', 'C#4'), ('C4', 'C4'),
        ('B3', 'B3'), ('A#3', 'A#3'), ('A3', 'A3'), ('G#3', 'G#3'),
        ('G3', 'G3'), ('F#3', 'F#3'), ('F3', 'F3'), ('E3', 'E3'),
        ('D#3', 'D#3'), ('D3', 'D3'), ('C#3', 'C#3'), ('C3', 'C3')
    ]
    pitch = models.CharField(choices=PITCHES, default='C4', max_length=4)
    DURATIONS = [
        ('4', 4),
        ('3', 3),
        ('2', 2),
        ('1.5', 1.5),
        ('1', 1),
        ('0.75', 0.75),
        ('0.5', 0.5),
        ('0.375', 0.375),
        ('0.25', 0.25)
    ]
    duration = models.CharField(choices=DURATIONS, max_length=5, default=1)
