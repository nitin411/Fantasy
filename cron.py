from crontab import CronTab

cron = CronTab(user='cron')
job = cron.new(command='python3 calculate_points.py')
job.minute.every(2)

cron.write()
