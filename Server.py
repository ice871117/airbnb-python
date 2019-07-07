# coding=utf-8
"""
The portal of this whole project
"""
import sys
import getopt
from SearchService import SearchService
from SearchService import Config
from LogHelper import Log
import os
import json
import time
import Utils
import signal
import io

MAIN_TAG = "main"
PID_FILE_NAME = "pid_file.txt"


def printHelp():
    print('''usage: python Server.py -c [config_path] [OPTION]...

config options:
  -c CONFIG              path to config file
  -s STORAGE_FILE        path to storage file
  -l LOG_FILE            path ot log file
  -d OPERATION           start | stop
  -v VERSION             show version of this software

General options:
  -h, --help             show this help message and exit
  --config-file=         specify the config file path
  --log-file=            specify the log file path
  --storage-file=        specify the storage file path
  --version              show version information
''')


def parseConfigFile(path):
    '''
    example for a valid config file, should be in json format

    {
        "start_hour":14,
        "start_minute":0,
        "counting_days":30,
        "room_limit":0,
        "smtp_host":"smtp.exmail.qq.com",
        "smtp_port":465,
        "email_receiver":"414191673@qq.com",
        "email_sender":"dataanalyzer@163.com",
        "sender_passwd":"***",
        "query":[
            "上海,徐汇区,中国",
            "上海,虹口区,中国",
            "上海,浦东新区,中国",
            "上海,普陀区,中国",
            "上海,长宁区,中国",
            "上海,闸北区,中国",
            "上海,杨浦区,中国",
            "上海,黄浦区,中国",
            "上海,卢湾区,中国",
            "上海,静安区,中国",
            "上海,宝山区,中国",
            "上海,闵行区,中国",
            "上海,嘉定区,中国",
            "上海,金山区,中国",
            "上海,松江区,中国",
            "上海,青浦区,中国",
            "上海,南汇区,中国",
            "上海,奉贤区,中国"
        ]
    }

    :param path:
    :return:
    '''
    try:
        f = open(path, "r", encoding='utf-8')
        jsonStr = f.read()
        configDict = json.loads(jsonStr.replace("\\n", ""))
        hour = configDict.get("start_hour")
        minute = configDict.get("start_minute")
        counting_days = configDict.get("counting_days")
        room_limit = configDict.get("room_limit")
        email_receiver = configDict.get("email_receiver")
        email_sender = configDict.get("email_sender")
        sender_passwd = configDict.get("sender_passwd")
        query = configDict.get("query")
        smtp_host = configDict.get("smtp_host")
        smtp_port = configDict.get("smtp_port")
        send_type = configDict.get("send_type")
        cities = dict()
        for item in query:
            splited = item.split(",")
            if len(splited) < 2:
                continue
            content = cities.get(splited[0])
            if not content:
                content = list()
                cities[splited[0]] = content
            content.append(splited)
        return Config(hour, minute, cities, email_receiver, email_sender, sender_passwd, room_limit,
                      countingDays=counting_days, smtpHost=smtp_host, smtpPort=smtp_port, sendType=send_type)
    except json.decoder.JSONDecodeError as e:
        Log.w(MAIN_TAG, "parseConfigFile() fail, ", e)
    return None

def freopen(f, mode, stream):
    oldf = open(f, mode)
    oldfd = oldf.fileno()
    newfd = stream.fileno()
    os.close(newfd)
    os.dup2(oldfd, newfd)

def daemon_start(pid_file):

    def handle_exit(signum, _):
        if signum == signal.SIGTERM:
            sys.exit(0)
        sys.exit(1)

    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    # fork only once because we are sure parent will exit
    pid = os.fork()
    assert pid != -1

    if pid > 0:
        # parent waits for its child
        time.sleep(5)
        sys.exit(0)

    # child signals its parent to exit
    ppid = os.getppid()
    pid = os.getpid()
    if write_pid_file(pid_file, pid) != 0:
        Log.e(MAIN_TAG, "write_pid_file() failed, pid = " + str(pid))
        os.kill(ppid, signal.SIGINT)
        sys.exit(1)

    os.setsid()
    signal.signal(signal.SIG_IGN, signal.SIGHUP)

    Log.d(MAIN_TAG, 'started')
    os.kill(ppid, signal.SIGTERM)

    sys.stdin.close()


def daemon_stop(pid_file):
    import errno
    try:
        with open(pid_file) as f:
            buf = f.read()
            pid = Utils.to_str(buf)
            if not buf:
                Log.e(MAIN_TAG, 'not running')
    except IOError as e:
        Log.e(MAIN_TAG, "daemon_stop() fail", e)
        if e.errno == errno.ENOENT:
            # always exit 0 if we are sure daemon is not running
            Log.e(MAIN_TAG, 'not running')
            return
        sys.exit(1)
    pid = int(pid)
    if pid > 0:
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError as e:
            if e.errno == errno.ESRCH:
                Log.e(MAIN_TAG, 'not running')
                # always exit 0 if we are sure daemon is not running
                return
            Log.e(MAIN_TAG, "daemon_stop() fail", e)
            sys.exit(1)
    else:
        Log.e(MAIN_TAG, 'pid is not positive: ' + str(pid))

    # sleep for maximum 10s
    for i in range(0, 200):
        try:
            # query for the pid
            os.kill(pid, 0)
        except OSError as e:
            if e.errno == errno.ESRCH:
                break
        time.sleep(0.05)
    else:
        Log.e(MAIN_TAG, 'timed out when stopping pid ' + str(pid))
        sys.exit(1)
    Log.d(MAIN_TAG, 'stopped')
    os.unlink(pid_file)

def write_pid_file(pid_file, pid):
    import fcntl
    import stat

    try:
        fd = os.open(pid_file, os.O_RDWR | os.O_CREAT,
                     stat.S_IRUSR | stat.S_IWUSR)
    except OSError as e:
        Log.w(MAIN_TAG, "exception for write_pid_file()", e)
        return -1
    flags = fcntl.fcntl(fd, fcntl.F_GETFD)
    assert flags != -1
    flags |= fcntl.FD_CLOEXEC
    r = fcntl.fcntl(fd, fcntl.F_SETFD, flags)
    assert r != -1
    # There is no platform independent way to implement fcntl(fd, F_SETLK, &fl)
    # via fcntl.fcntl. So use lockf instead
    try:
        fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB, 0, 0, os.SEEK_SET)
    except IOError:
        r = os.read(fd, 32)
        if r:
            Log.e(MAIN_TAG, 'already started at pid %s' % Utils.to_str(r))
        else:
            Log.e(MAIN_TAG, 'already started')
        os.close(fd)
        return -1
    os.ftruncate(fd, 0)
    os.write(fd, Utils.to_bytes(str(pid)))
    return 0


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    configPath = None
    parentPath = os.environ.get('HOME')
    if not parentPath:
        print('can not fetch $HOME')
        parentPath = "."
    parentPath += "/airbnb"
    if not os.path.exists(parentPath):
        os.mkdir(parentPath, mode=0o755)

    pidFilePath = parentPath + "/" + PID_FILE_NAME
    logPath = parentPath + "/all_logs.log"
    storagePath = parentPath + "/rooms.db"
    shortopts = 'h:c:d:l:s:v'   # 命令行参数简写
    longopts = ['help', 'storage-file=', 'log-file=', 'version', 'config-file=']  # 完整体
    # 执行动作 start 后台运行，stop 结束后台已经运行的实例
    operation = None

    optlist, args = getopt.getopt(sys.argv[1:], shortopts, longopts)
    # 拿到命令行参数的key value
    for key, value in optlist:
        if key in ('-v', '--version'):
            print("version: airbnb fetcher 0.1")
            sys.exit(0)
        if key in ('-h', '--help'):
            printHelp()
            sys.exit(0)
        if key in ('-c', '--config-file'):
            configPath = value
        if key in ('-l', '--log-file'):
            logPath = value
        if key in ('-s', '--storage-file'):
            storagePath = value
        if key == '-d':
            operation = value

    # 配置日志模块
    Log.config(logPath, echo=True)
    if operation == "start":
        daemon_start(pidFilePath)
    elif operation == "stop":
        daemon_stop(pidFilePath)
        sys.exit(0)

    if not configPath:
        Log.e(MAIN_TAG, "config path not provided")
        sys.exit(0)
    config = parseConfigFile(configPath)
    if not config:
        sys.exit(0)
    config.localStoragePath = storagePath
    service = SearchService(config)
    service.start()

if __name__ == "__main__":
    main()
