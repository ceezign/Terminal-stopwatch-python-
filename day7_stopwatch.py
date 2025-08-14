import time
import csv
import threading
from datetime import datetime

# Stopwatch state
start_time = None
laps = []
paused = False
pause_start = None
total_paused_time = 0
running = False
stop_display = False


def format_time(seconds):
    """Format seconds into MM:SS.ss"""
    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:05.2f}"


def display_timer():
    """Continuously update elapsed time while running"""
    global stop_display
    while not stop_display:
        if running and not paused:
            elapsed = time.time() - start_time - total_paused_time
            print(f"\rElapsed Time: {format_time(elapsed)}", end="")
        time.sleep(0.1)


def start_stopwatch():
    global start_time, laps, paused, pause_start, total_paused_time, running
    start_time = time.time()
    laps = []
    paused = False
    pause_start = None
    total_paused_time = 0
    running = True
    print("\nStopwatch started!")


def record_lap():
    if start_time is None:
        print("\nStopwatch not started yet!")
        return

    total_elapsed = time.time() - start_time - total_paused_time
    lap_time = total_elapsed if not laps else total_elapsed - sum(laps)
    laps.append(lap_time)
    print(f"\nLap {len(laps)}: {format_time(lap_time)} | Total: {format_time(total_elapsed)}")


def pause_stopwatch():
    global paused, pause_start
    if not paused:
        pause_start = time.time()
        paused = True
        print("\nStopwatch paused.")
    else:
        print("\nAlready paused.")


def resume_stopwatch():
    global paused, total_paused_time, pause_start
    if paused:
        total_paused_time += time.time() - pause_start
        paused = False
        print("\nStopwatch resumed.")
    else:
        print("\nStopwatch is not paused.")


def stop_stopwatch():
    global running
    running = False
    if start_time is None:
        print("\nStopwatch not started yet!")
        return

    total_time = time.time() - start_time - total_paused_time
    if not laps:
        print(f"\nTotal time: {format_time(total_time)} (No laps recorded)")
        return

    fastest = min(laps)
    slowest = max(laps)
    avg = sum(laps) / len(laps)

    print("\n===== Summary =====")
    print(f"Total Time: {format_time(total_time)}")
    print(f"Number of Laps: {len(laps)}")
    print(f"Fastest Lap: {format_time(fastest)}")
    print(f"Slowest Lap: {format_time(slowest)}")
    print(f"Average Lap: {format_time(avg)}")

    save_to_csv(total_time, fastest, slowest, avg)


def save_to_csv(total_time, fastest, slowest, avg):
    """Optional: Save stopwatch session to CSV"""
    filename = "stopwatch_sessions.csv"
    now = datetime.now()
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            now.date(),
            now.strftime("%H:%M:%S"),
            format_time(total_time),
            len(laps),
            format_time(fastest),
            format_time(slowest),
            format_time(avg)
        ])
    print(f"Session saved to {filename}")


def reset_stopwatch():
    global start_time, laps, paused, pause_start, total_paused_time, running
    start_time = None
    laps = []
    paused = False
    pause_start = None
    total_paused_time = 0
    running = False
    print("\nStopwatch reset!")


# Start display thread
threading.Thread(target=display_timer, daemon=True).start()

print("Commands: start, lap, pause, resume, stop, reset, quit")
while True:
    cmd = input("\n> ").strip().lower()

    if cmd == "start":
        start_stopwatch()
    elif cmd == "lap":
        record_lap()
    elif cmd == "pause":
        pause_stopwatch()
    elif cmd == "resume":
        resume_stopwatch()
    elif cmd == "stop":
        stop_stopwatch()
    elif cmd == "reset":
        reset_stopwatch()
    elif cmd == "quit":
        stop_display = True
        print("\nGoodbye!")
        break
    else:
        print("Unknown command. Try again.")