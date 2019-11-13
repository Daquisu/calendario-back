import os

def stop_cron():
    os.system('touch stop_.md')

if __name__ == '__main__':
    stop_cron()