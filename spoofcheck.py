import time
import etw
import psutil

def get_me_my_parent(x):
    _etwData = x[1]
    _realParentPid = int(_etwData['EventHeader']['ProcessId']) # PID that generated this event 
    _parentPid = int(_etwData['ParentProcessID'])
    _pid = int(_etwData['ProcessID'])

    # Check parent pid with pid that causes this event (In other words, the original parent).
    _isSpoofed = _realParentPid != _parentPid

    if _isSpoofed:
            process_name = ""
            fake_parent_process_name = ""
            real_parent_process_name = ""

            for proc in psutil.process_iter():
                if proc.pid == _pid:
                    process_name = proc.name()
                elif proc.pid == _parentPid:
                    fake_parent_process_name = proc.name()
                elif proc.pid == _realParentPid:
                    real_parent_process_name = proc.name()

            print("Spoofed parent process detected!!!\n\t{0}({1}) is detected with parent {2}({3}) but originally from parent {4}({5}).".format(process_name, _pid, fake_parent_process_name, _parentPid, real_parent_process_name, _realParentPid))

def main_function():
    # define capture provider info
    providers = [etw.ProviderInfo('Microsoft-Windows-Kernel-Process', etw.GUID("{22FB2CD6-0E7B-422B-A0C7-2FAD1FD0E716}"))]
    
    # create instance of ETW class
    job = etw.ETW(providers=providers, event_callback=lambda x: get_me_my_parent(x), task_name_filters="PROCESSSTART")
    
    # start capture
    job.start()

    try:
        while True:
            pass
    except(KeyboardInterrupt):
        job.stop()
        print("ETW monitoring stopped.")

if __name__ == '__main__':
    main_function()
