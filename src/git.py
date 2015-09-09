import subprocess
import textwrap

PIPE = subprocess.PIPE


def set_api_key(git_dir, handle, key):    
    set_key_command = [ 'git', '-C', git_dir, 'config', 'toggl.key.' + handle, key ] 
    _execute_git_command(set_key_command)   


def set_pid(git_dir, pid):
    set_pid_command = [ 'git', '-C', git_dir, 'config', 'toggl.pid', pid ]
    _execute_git_command(set_pid_command)


def commit(git_dir, subject, time, handles):
    git_add_command = [ 'git', '-C', git_dir, 'add', '.' ] 

    body = textwrap.dedent("""
    Time_spent: %s
    Committers: %s """ % (time, handles))
                                                    
    git_commit_command = [ 'git', '-C', git_dir, 'commit', \
                         '-m', subject, \
                         '-m', body ] 

    _execute_git_command(git_add_command)
    _execute_git_command(git_commit_command) 


def show(git_dir, sha):
    git_show_command = [ 'git', '-C', git_dir, 'log', sha, '-n', '1', '--pretty=format:%b' ]
    
    return _execute_git_command(git_show_command)


def _execute_git_command(command):
    process = subprocess.Popen(command, stdout=PIPE, stderr=PIPE)
    stdoutput, stderroutput = process.communicate()
    return stdoutput
    
