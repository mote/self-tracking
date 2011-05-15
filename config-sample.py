"Config parameters for personal informatics script."


df_blacklist = [
    '/home/mote/asdfa',
    '/home/mote/qwer',
    '/media/big',
    '/media/extra1',
    '/media/DINO',
    ]

media_dirs = [
    ('/mp3', 'mp3'),
    ('/digicam', 'digicam'),
    ('/mov', 'mov'),
    ('/tv', 'tv'),
    ('/home/mote', 'home/mote'),
    ('/home/mote/dls', 'home/mote/dls'),
    ]


code_dir = '/home/mote/dev/'
code_blacklist_dirs = [
    'lib',
    'libs',
    'others',
    'external',
    'svn'
    ]

svn_dirs = [
    ('code', '/home/mote/dev/'),
    ('general', '/home/mote/'),
    ]

server_names = [
    'ate',
    ]

nonlocal_dir_names = [
    ('motespace.com', '/home/mote/.'),
    ]

uptime_hosts = [
    'lak',
    'ate',
    'sen',
    'motespace.com',
    ]

other_commands = [
  ('buzz',       '/home/mote/dev/microblogs/get_current_buzz_counts.py'),
  ('corp_buzz',  '/home/mote/dev/microblogs/get_current_corp_buzz_counts.py'),
  ('twitter',    '/home/mote/dev/microblogs/get_current_twitter_counts.py'),
  ('music',      '/home/mote/dev/pyamarokdb/get_daily_info.py'),
  ('motespace',  '/home/mote/dev/apachelog/get_motespace_counts.py'),
  ('gmail',      '/home/mote/dev/email/get_gmail_counts.py'),
  ('load',       '/home/mote/dev/self_tracking/get_yesterdays_loads.py'),
  ('daytime',    '/home/mote/dev/self_tracking/sunrise_sunset.py'),
  ('bash',       '/home/mote/dev/self_tracking/parse_bashlog.py'),
  ('vim',        '/home/mote/dev/self_tracking/parse_vimlog.py'),
  ('cmds',       '/home/mote/dev/self_tracking/get_running.py'),
  ('gws_count',  '/home/mote/dev/webapi/gws_egosearch.py'),
  ]

