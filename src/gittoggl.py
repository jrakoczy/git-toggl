import indicator
import signal

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    indicator.run_application()
