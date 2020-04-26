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
    METERS = [
        ('2/4', '2/4'), ('3/4', '3/4'), ('4/4', '4/4'),
    ]
    meter = models.CharField(choices=METERS, default='4/4', max_length=3)
    data = models.TextField(blank=True)
    file = models.FileField(upload_to=user_directory_path, blank=True)

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
    order = models.DecimalField(default=1, max_digits=10, decimal_places=1)
    PITCHES = [
        ('C3', 1), ('D3', 2), ('E3', 3), ('F3', 4),
        ('G3', 5), ('A3', 6), ('B3', 7), ('C4', 8),
        ('D4', 9), ('E4', 10), ('F4', 11), ('G4', 12),
        ('A4', 13), ('B4', 14), ('C5', 15), ('D5', 16),
        ('E5', 17), ('F5', 18), ('G5', 19), ('A5', 20),
        ('B5', 21), ('C6', 22),
    ]
    pitch = models.CharField(choices=PITCHES, default=8, max_length=2)
    DURATIONS = [
        ('4', 4),
        ('3', 3),
        ('2', 2),
        ('1.5', 1.5),
        ('1', 1),
        ('0.75', 0.75),
        ('0.5', 0.5),
        ('0.375', 0.375),
        ('0.25', 0.25),
    ]
    duration = models.CharField(choices=DURATIONS, max_length=5, default=1)
    ACCIDENTALS = [
        ('double-flat', 'double-flat'),
        ('flat', 'flat'),
        ('natural', 'natural'),
        ('sharp', 'sharp'),
        ('double-sharp', 'double-sharp'),
        (' ', ' '),
    ]
    accidental = models.CharField(
        max_length=12, choices=ACCIDENTALS, default=' '
    )
