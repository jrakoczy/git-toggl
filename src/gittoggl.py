import indicator
import signal

SETTINGS_FILE = 'settings.yaml'

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    indicator.run_application()
