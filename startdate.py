#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import time
import sopel.module

##############################################################################
#
#  functions and other stuff to calculate the stardate for a given date
#
#  by Tobias Diekershoff <tobias.diekershoff--at--gmx.net> 2009
#
#  IF YOU WISH TO USE THIS PIECE OF CODE, THEN PLEASE DO SO
#  BUT DON'T BLAME ME FOR ANYTHING THAT WENT WRONG WITH YOUR
#  PROGRAM AND/OR YOUR COMPUTER WHILE DOING SO!
#
##############################################################################

# version of this module
ver_major = 0
ver_minor = 1
ver_release = 2
version = "%d.%d-%d" % (ver_major, ver_minor, ver_release)

@sopel.module.commands('curstardate')
def curstardate(bot,trigger):
  bot.say(now_y2k())

def calc(daylength,yearlength,baseyear,second_of_day,day_of_year,year):
  """calculates the stardate from the set of daylength (in seconds), yearlength (in days)
  the baseyear (2323 for TNG and following series), the second of the day, the day of the
  year and the year itself."""
  daylength = daylength * 1.  # the the user don't have to apply the float
  yearlength = yearlength * 1.
  return "%d %03d.%02d" % (year-baseyear, day_of_year / yearlength * 1000, second_of_day / daylength * 100)

def from_earthdate(baseyear,day,month,year,hour,minute):
  """takes day,month,year,hour and minute and calculates the stardate for an earthling
  using 365.25 days per year and a daylength of 24*60*60 seconds."""
  d = day
  if (month > 1): d = d + 31
  if (month > 2): d = d + 28
  if (month > 3): d = d + 31
  if (month > 4): d = d + 30
  if (month > 5): d = d + 31
  if (month > 6): d = d + 30
  if (month > 7): d = d + 31
  if (month > 8): d = d + 31
  if (month > 9): d = d + 30
  if (month > 10): d = d + 31
  if (month > 11): d = d + 30
  return calc(24*60*60, 365.25, baseyear, ((hour*60)+minute)*60, d,year)

def now_from_earthdate ():
  """returns the current stardate on earth
  daylength 24*60*60 seconds, yearlength 365.25 days, baseyear 0"""
  d = int(time.strftime('%d'))
  m = int(time.strftime('%m'))
  y = int(time.strftime('%Y'))
  h = int(time.strftime('%H'))
  mi = int(time.strftime('%M'))
  return from_earthdate(0, d, m, y, h, mi)
def now():
  """short form for now_from_earthdate()
  returns the current stardate on earth
  daylength 24*60*60 seconds, yearlength 365.25 days, baseyear 0"""
  return now_from_earthdate()

def now_from_earthdate_y2k ():
  """returns the current stardate on earth
  daylength 24*60*60 seconds, yearlength 365.25 days, baseyear 2000"""
  d = int(time.strftime('%d'))
  m = int(time.strftime('%m'))
  y = int(time.strftime('%Y'))
  h = int(time.strftime('%H'))
  mi = int(time.strftime('%M'))
  return from_earthdate(2000, d, m, y, h, mi)
def now_y2k():
  """short form for now_from_earthdate()
  returns the current stardate on earth
  daylength 24*60*60 seconds, yearlength 365.25 days, baseyear 2000"""
  return now_from_earthdate_y2k()

# end of stardate.py
