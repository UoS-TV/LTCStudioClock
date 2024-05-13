# import subprocess

# audio_device = "hw:3,0" 

# # Define individual shell commands in the pipeline
# arecord_command = ["arecord", "-D", audio_device, "-f", "dat", "-r", "48000", "-c", "2"]
# ltcdump_command = ["ltcdump", "-"]

# # Create subprocesses for each command
# arecord_process = subprocess.Popen(arecord_command, stdout=subprocess.PIPE)
# ltcdump_process = subprocess.Popen(ltcdump_command, stdin=arecord_process.stdout, stdout=subprocess.PIPE)

# # Continuous loop to read LTC timecode
# while True:
#     # Read LTC timecode from ltcdump process output
#     ltc_timecode = ltcdump_process.stdout.readline().strip().decode()
#     print(ltc_timecode)


# import time

# # Function to convert LTC timecode to NTP format
# def ltc_to_ntp(ltc_timecode):
#     # Parse LTC timecode
#     hours, minutes, seconds, frames = map(int, ltc_timecode.split(':'))

#     # Calculate total frames
#     total_frames = (hours * 3600 + minutes * 60 + seconds) * 25 + frames

#     # Get current date from system clock
#     current_date = time.strftime("%Y-%m-%d", time.localtime())

#     # Convert frames to seconds and add offset for current date (NTP epoch)
#     ntp_time = total_frames / 25 + time.mktime(time.strptime(current_date, "%Y-%m-%d")) - time.mktime(time.strptime("1900-01-01", "%Y-%m-%d"))

#     return ntp_time

# # Test the function
# ltc_timecode = "01:23:45:67"  # Example LTC timecode
# ntp_time = ltc_to_ntp(ltc_timecode)
# print("NTP time:", ntp_time)



# import subprocess

# audio_device = "hw:3,0"

# # import subprocess

# # Define the commands
# arecord_command = ["arecord", "-D", audio_device, "-f", "dat", "-r", "48000", "-c", "2"]
# ltcdump_command = ["ltcdump", "-"]

# # Start the processes with line buffering enabled
# arecord_process = subprocess.Popen(arecord_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, text=True)
# ltcdump_process = subprocess.Popen(ltcdump_command, stdin=arecord_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=1)

# # Continuously read and display the output of ltcdump_process
# while True:
#     output = ltcdump_process.stdout.readline()
#     if output == '' and ltcdump_process.poll() is not None:
#         break
#     if output:
#         print(output.strip())

# # Wait for the processes to finish
# arecord_process.wait()
# ltcdump_process.wait()

# import ltc_reader
# import threading
# import time

# def get_timecode():
#     while True:
#         print("time to print")
#         timecode = ltc_reader.print_tc([])  # Call decode_ltc function to get the timecode
#         print("Timecode:", timecode)
#         time.sleep(10)

# if __name__ == "__main__":
#     read_thread = threading.Thread(ltc_reader.start_read_ltc())  # Start capturing LTC
#     timer_thread = threading.Thread(target=get_timecode)
#     read_thread.start()
#     timer_thread.start()  # Start the timer to get the timecode every 10 seconds

# import subprocess

# # Define the command as a list of arguments
# reader_command = ["/home/pi/ltc-test/.venv/bin/python3", "-c", "import ltc_reader;ltc_reader.start_read_ltc()"]

# # Start the subprocess
# process = subprocess.Popen(reader_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, text=True)

# # Continuously read from the stdout of the subprocess
# while True:
#     # Read a line from the stdout of the subprocess
#     line = process.stdout.readline()
#     print(line)
#     # Check if the line is empty, indicating end of file
#     if not line:
#         break
    
#     # Print the line (you can process it further if needed)
#     print("Output from subprocess:", line.strip())

import subprocess

def extract_frames(timecode):
    # Split the timecode string into its components
    components = timecode.split(':')
    
    # Extract the last two components representing frames
    frames = components[-1]
    
    return frames

def process_timecode(timecode):
    frames = extract_frames(timecode)
    print("Frames:", frames)

def main():
    # Start the LTC reader subprocess with shell redirection
    ltc_process = subprocess.Popen(['python3', '-m', 'ltc_reader_script.py'], stdout=subprocess.PIPE)

    try:
        for line in iter(ltc_process.stdout.readline, b''):
            # Decode the line from bytes to string and remove trailing newline
            timecode = line.decode().strip()
            process_timecode(timecode)
    finally:
        # Close the LTC reader subprocess
        ltc_process.kill()

if __name__ == "__main__":
    main()








