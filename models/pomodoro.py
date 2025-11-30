from threading import RLock, Thread
import time

class PomodoroTimer():
    DEFAULTS = {"work": 25, "small_break": 5, "long_break": 15, "break_interval": 4}

    def __init__(self, work=25, small_break=5, long_break=15, break_interval=4):
        self.work = work
        self.small_break = small_break
        self.long_break = long_break
        self.break_interval = break_interval

        self.state = "Work"  # Work, smallBreak, longBreak
        self.short_break_count = 0
        self.time_left = self.work * 60
        self.running = False
        self.lock = RLock()  # Reentrant lock for thread safety
        self.timer_thread = None  # Track the timer thread
        
    def update_durations(self, work=None, small_break=None, long_break=None):
        with self.lock:
            if work is not None:
                self.work = work
            if small_break is not None:
                self.small_break = small_break
            if long_break is not None:
                self.long_break = long_break
            # Update time_left to reflect new duration for current state if timer is not running
            if not self.running:
                if self.state == "Work":
                    self.time_left = self.work * 60
                elif self.state == "smallBreak":
                    self.time_left = self.small_break * 60
                elif self.state == "longBreak":
                    self.time_left = self.long_break * 60
            
    def get_current_duration(self):
        with self.lock:
            if self.state == "Work": return self.work
            elif self.state == "smallBreak": return self.small_break
            elif self.state == "longBreak": return self.long_break
            
    def next_state(self):
        with self.lock:
            if self.state == "Work":
                self.short_break_count += 1
                if self.short_break_count >= self.break_interval:
                    self.state = "longBreak"
                    self.short_break_count = 0
                    self.time_left = self.long_break * 60
                else:
                    self.state = "smallBreak"
                    self.time_left = self.small_break * 60
            else:
                self.state = "Work"
                self.time_left = self.work * 60   
             
    def prev_state(self):
        with self.lock: 
            if self.state=="Work":
                if self.short_break_count == 0:
                    self.state="longBreak"
                    self.short_break_count = self.break_interval
                    self.time_left = self.long_break * 60
                else:
                    self.state="smallBreak"
                    self.short_break_count -= 1
                    self.time_left = self.small_break * 60
            else:
                self.state="Work"
                self.time_left = self.work * 60
    def start(self):
        with self.lock:
            if self.running: 
                return
            self.running = True
        self.timer_thread = Thread(target=self._run_timer, daemon=True)
        self.timer_thread.start()
        
    def stop(self):
        with self.lock:
            self.running = False
        # Give the thread a moment to exit (it checks the flag after sleep)
        if self.timer_thread and self.timer_thread.is_alive():
            time.sleep(0.1)  # Brief wait for thread to exit
    def reset_durations(self):
        with self.lock:
            self.work = self.DEFAULTS["work"]
            self.small_break = self.DEFAULTS["small_break"]
            self.long_break = self.DEFAULTS["long_break"]
            self.break_interval = self.DEFAULTS["break_interval"]
            self.reset_timer()

    def reset_timer(self):
        with self.lock:
            # Stop the timer first
            self.running = False
            # Reset time to the initial value of the current stage
            if self.state == "Work":
                self.time_left = self.work * 60
            elif self.state == "smallBreak":
                self.time_left = self.small_break * 60
            elif self.state == "longBreak":
                self.time_left = self.long_break * 60
            
    def _run_timer(self):
        while True:
            with self.lock:
                if not self.running: 
                    break
                if self.time_left <= 0:
                    self.running = False
                    # Inline next_state logic to avoid nested lock acquisition
                    if self.state == "Work":
                        self.short_break_count += 1
                        if self.short_break_count >= self.break_interval:
                            self.state = "longBreak"
                            self.short_break_count = 0
                            self.time_left = self.long_break * 60
                        else:
                            self.state = "smallBreak"
                            self.time_left = self.small_break * 60
                    else:
                        self.state = "Work"
                        self.time_left = self.work * 60
                    break
                self.time_left -= 1
            time.sleep(1)

    def get_state(self):
        with self.lock:
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            label = (
            "Work" if self.state == "Work" else
            "Small Break" if self.state == "smallBreak" else
            "Long Break"
            )
            return {
                "state": self.state,
                "stateLabel": label,
                "minutes": minutes,
                "seconds": seconds,
                "running": self.running
            }
        
