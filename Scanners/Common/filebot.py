import json, xattr

from os.path import *
from datetime import *


#####################################################################################################################


def getxattr(file, key):
  # try xattr
  value = xattr.getxattr(file, key)
  if value:
    return value

  # try plain file xattr store
  return getxattr_plain_file('.xattr', file, key)


def getxattr_plain_file(store, file, name):
  if not isabs(store):
    store = join(dirname(file), store)

  xattr_file = join(store, basename(file), name)

  if not isfile(xattr_file):
    return None

  fd = open(xattr_file, "rb")
  buffer = fd.read()
  fd.close()
  return buffer.decode('utf-8')


def xattr_metadata(file): 
  value = getxattr(file, 'net.filebot.metadata')
#  return json.loads(value) if value else None
   return json.loads(value)

def xattr_filename(file):
  return getxattr(file, 'net.filebot.filename')


#####################################################################################################################


def movie_id(attr):
  imdb_id = attr.get('imdbId')
  if imdb_id > 0:
    return u"tt%07d" % imdb_id

  tmdb_id = attr.get('tmdbId')
  if tmdb_id > 0:
    return u"%01d" % tmdb_id

  return None


def movie_guid(attr):
  imdb_id = attr.get('imdbId')
  if imdb_id > 0:
    return u"tt%07d" % imdb_id

  tmdb_id = attr.get('tmdbId')
  if tmdb_id > 0:
    return u"com.plexapp.agents.themoviedb://%s?lang=%s" % (tmdb_id, movie_language(attr))

  return None


def movie_name(attr):     return attr.get('name')
def movie_year(attr):     return attr.get('year')
def movie_language(attr): return attr.get('language')

def movie_part_index(attr): return attr.get('partIndex')
def movie_part_count(attr): return attr.get('partCount')


#####################################################################################################################


def series_id(attr):
  series_id = attr_get(attr, 'seriesInfo', 'id')
  if series_id > 0:
    db = attr_get(attr, 'seriesInfo', 'database')
    return u"%s_%s" % (db, series_id)

  return None


def series_guid(attr):
  series_id = attr_get(attr, 'seriesInfo', 'id')
  if series_id > 0:
    db = attr_get(attr, 'seriesInfo', 'database')
    lang = series_language(attr)
    if db == 'TheTVDB':
      return u"com.plexapp.agents.thetvdb://%s?lang=%s" % (series_id, lang)
    elif db == 'TheMovieDB::TV':
      return u"com.plexapp.agents.themoviedb://%s?lang=%s" % (series_id, lang)
    elif db == 'AniDB':
      return u"com.plexapp.agents.hama://%s?lang=%s" % (series_id, lang)
    else:
      return u"%s://%s" % (db.lower(), series_id)

  return None


def list_episodes(attr):
  # check for single episode
  if series_name(attr):
    return [attr]

  # check for multi episode
  episodes = attr_get(attr, 'episodes')
  if episodes:
    return episodes

  return []


def series_name(attr): return attr_get(attr, 'seriesName')
def series_year(attr): return attr_get(attr, 'seriesInfo', 'startDate', 'year')


def series_language(attr):      return attr_get(attr, 'seriesInfo', 'language')
def series_date(attr):          return attr_date(attr_get(attr, 'seriesInfo', 'startDate'))
def series_certification(attr): return attr_get(attr, 'seriesInfo', 'certification')
def series_network(attr):       return attr_get(attr, 'seriesInfo', 'network')
def series_runtime(attr):       return attr_get(attr, 'seriesInfo', 'runtime')
def series_rating(attr):        return attr_get(attr, 'seriesInfo', 'rating')
def series_genres(attr):        return attr_get(attr, 'seriesInfo', 'genres')


def episode_number(attr):          return attr.get('episode')
def episode_season_number(attr):   return attr.get('season')
def episode_special_number(attr):  return attr.get('special')
def episode_title(attr):           return attr.get('title')
def episode_absolute_number(attr): return attr.get('absolute')
def episode_date(attr):            return attr_date(attr_get(attr, 'airdate'))


def attr_get(attr, *keys):
  for k in keys:
    attr = attr.get(k)
    if attr is None:
      return None
  return attr


def attr_date(attr):
  if attr is not None:
    return datetime(year=attr['year'], month=attr['month'], day=attr['day'])
  return None
