#!/usr/bin/python
"Scrappy collection of functions to compute personal infometrics"

import datetime
import itertools
import os
import subprocess
import sys

import config

def _run(cmd):
  return subprocess.Popen(cmd, shell=True,
      stdout=subprocess.PIPE, close_fds=True).stdout.read().rstrip()

def get_num_files(path):
  files = 
  return _run('find %s/. | wc -l' % path)

def get_num_files_done(path):
  return _run('find %s/. | grep done | wc -l' % path)

def get_dirsize(path):
  du = _run('du -s %s' % path)
  du = du.split()
  try:
    return du[0]
  except:
    return -1

def get_subdirs(parent_dir, ignore_dots=True):
  for sub in os.listdir(parent_dir):
    if ignore_dots and sub.startswith('.'):
      continue
    if os.path.isdir(os.path.join(parent_dir, sub)):
      yield sub

def get_nonlocal_dirsize(server, path):
  du = _run("ssh %s 'du -s %s'" % (server, path))
  du = du.split()
  try:
    return du[0]
  except:
    return -1

def get_lines_of_python(path, blacklist=[]):
  blacklist = ['grep -v "/%s/"' % b for b in blacklist]
  blacklist = ' | '.join(blacklist)
  all = _run('find %s/. | grep "py$" | %s | xargs wc -l' % (path, blacklist))
  try:
    all = all.split('\n')
    all = all[-1]
    all = all.split()
    all = all[0]
    return all
  except:
    return -1

def svn_dirstats(path):
  """Get count of how many files are unknown/modified/added but not
  committed."""
  counts = {}
  counts['X'] = 0
  counts['Performing'] = 0
  for line in _run('svn st %s' % path).split('\n'):
    try:
      fields = line.split()
      f = fields[0]
      counts[f] = counts.get(f, 0) + 1
    except:
      pass
  del counts['X']
  del counts['Performing']
  return counts


def parse_df(df_lines, blacklist):
  used = 0
  total = 0
  for line in df_lines.split('\n'):
    do_skip = False
    for skip in blacklist:
      if skip in line:
        do_skip = True
        break
    if do_skip:
      continue

    if not line.startswith('/dev/'):
      continue
    try:
      fields = line.split()
      total += int(fields[1])
      used += int(fields[2])
    except Exception, e:
      continue
  return (used, total)


def parse_uptime(text):
  """Return days of uptime."""
  try:
    fields = text.strip().split()
    return fields[2]
  except:
    return -1


def prefix_run(command, prefix):
  try:
    output = _run(command)
  except:
    sys.stderr.write('Problem with %s' % command)
    return

  for line in output.split('\n'):
    fields = line.split()
    try:
      yield '%s-%s' % (prefix, '_'.join(fields[0:-1])), fields[-1]
    except:
      pass

# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------

def count_media(dir_names):
  for dir, name in dir_names:
    num_files = get_num_files(dir)
    num_files_done = get_num_files_done(dir)
    if num_files:
      yield '%s-num' % name, num_files
    if num_files_done:
      yield '%s-numdone' % name, num_files_done
    yield '%s-size' % name, get_dirsize('%s/' % dir)


def code(code_dir, blacklist):
  loc_total = 0
  for project in get_subdirs(code_dir):
    path = os.path.join(code_dir, project)
    loc = int(get_lines_of_python(path, blacklist))
    if not loc:
      continue
    loc_total += int(loc)
    yield 'loc_python-%s' % project, loc
  yield 'loc_python-total', loc_total


def svn_stats(svn_dirs):
  for name, parent_dir in svn_dirs:
    for project in get_subdirs(parent_dir):
      path = os.path.join(parent_dir, project)
      for type, count in svn_dirstats(path).items():
        yield 'svn-%s_%s-%s' % (name, project, type), count


def disks(blacklist):
  used, total = parse_df(_run('df'), blacklist)
  yield 'disk-lak-total', total
  yield 'disk-lak-used', used
  yield 'disk-lak-free', total - used
  try:
    yield 'disk-lak-percent_used', 100*used/total
  except Exception, e:
    pass

def nonlocal_disks(server_names, blacklist):
  for server_name in server_names:
    used, total = parse_df(_run("ssh %s 'df'" % server_name), blacklist)
    if (used, total) == (0, 0):
      return
    yield 'disk-%s-total' % server_name, total
    yield 'disk-%s-used' % server_name, used
    yield 'disk-%s-free' % server_name, total - used
    try:
      yield 'disk-%s-percent_used' % server_name, 100*used/total
    except Exception, e:
      pass

def nonlocal_dir_sizes(server_dirs):
  for server, dirname in server_dirs:
    used = get_nonlocal_dirsize(server, dirname)
    yield 'disk-%s-used' % server, used

def miscellany(key_commands):
  for key, command in key_commands:
    for k, v in prefix_run(command, key):
      yield k, v

def uptime(uptime_hosts):
  for host in uptime_hosts:
    uptime = parse_uptime(_run("ssh %s 'uptime'" % host))
    yield 'uptime-%s' % host, uptime

# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------

def output_all():
  """Print all (name, val) pairs to stdout."""
  now = datetime.datetime.now()
  now = now.strftime('%Y%m%d')
  for k, v in itertools.chain(
      count_media(config.media_dirs),
      code(config.code_dir, config.code_blacklist_dirs),
      svn_stats(config.svn_dirs),
      disks(config.df_blacklist),
      nonlocal_disks(config.server_names, []),
      nonlocal_dir_sizes(config.nonlocal_dir_names),
      miscellany(config.other_commands),
      uptime(config.uptime_hosts),
      ):
    print now, k, v


if __name__ == '__main__':
  output_all()
