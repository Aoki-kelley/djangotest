import djcelery

djcelery.setup_loader()

# 导入应用中任务文件
CELERY_IMPORTS = (
    'user.tasks',
)

# 有些情况下可以防止死锁
CELERYD_FORCE_EXECV = True

# 设置并发的worker数量
CELERYD_CONCURRENCY = 4

# 设置失败允许重试
CELERYD_ACKS_LATE = False

# 每个worker最多执行100个任务被销毁，可以防止内存泄漏
CELERYD_MAX_TASKS_PER_CHILD = 100

# 单个任务的最大运行时间，超时会被杀死
CELERYD_TASK_TIME_LIMIT = 12 * 30
