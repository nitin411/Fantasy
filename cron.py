from crontab import CronTab

cron = CronTab(user='cron')
job = cron.new(command='python calculate_points.py')
job.minute.every(1)

cron.write()