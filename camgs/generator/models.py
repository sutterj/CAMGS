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
    user = models.ForeignKey(CustomUser,
                             default=None,
                             on_delete=models.CASCADE)
    title = models.CharField(default='untitled', max_length=250)
    composer = models.CharField(default='none', max_length=250)
    tempo = models.IntegerField(default=120)
    beatunit = models.CharField(max_length=4, default=4)
    CUT = '2'
    COMMON = '4'
    EIGHT = '8'
    SIXTEEN = '16'
    DIVISIONS = [
        (CUT, '2'),
        (COMMON, '4'),
        (EIGHT, '8'),
        (SIXTEEN, '16'),
    ]
    division = models.CharField(max_length=2,
                                choices=DIVISIONS,
                                default=COMMON)
    data = models.TextField(blank=True)
    file = models.FileField(upload_to=user_directory_path, blank=True)

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.user = user
        slug = "%s" % (self.title)
        unique_slugify(self, slug)
        super(Composition, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug


class NoteObject(models.Model):
    id = models.AutoField(primary_key=True)
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE)
    WHOLE = 4
    DOTHALF = 3
    HALF = 2
    DOTQUARTER = 1.5
    QUARTER = 1
    DOTEIGHTH = 0.75
    EIGHTH = 0.5
    DOTSIXTEENTH = 0.375
    SIXTEENTH = 0.25
    DURATIONS = [
        (WHOLE, '16'),
        (DOTHALF, '12'),
        (HALF, '8'),
        (DOTQUARTER, '6'),
        (QUARTER, '4'),
        (DOTEIGHTH, '3'),
        (EIGHTH, '2'),
        (DOTSIXTEENTH, '1.5'),
        (SIXTEENTH, '1'),
    ]
    duration = models.DecimalField(max_digits=5,
                                   decimal_places=3,
                                   choices=DURATIONS,
                                   default=QUARTER)
    PITCHES = [
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
        ('G', 'G'),
        ('A', 'A'),
        ('B', 'B'),
    ]
    pitch = models.CharField(max_length=1,
                             choices=PITCHES,
                             default='C')
    ACCIDENTALS = [
        ('double-flat', 'double-flat'),
        ('flat', 'flat'),
        ('natural', 'natural'),
        ('sharp', 'sharp'),
        ('double-sharp', 'double-sharp'),
        ('', 'none'),
    ]
    accidental = models.CharField(max_length=12,
                                  choices=ACCIDENTALS,
                                  default='',
                                  blank=True)
    OCTAVES = [
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
    ]
    octave = models.IntegerField(choices=OCTAVES, default='4')
