import subprocess

def read_ltc_timecode(audio_device):
    command = ["arecord", "-D", audio_device, "-f", "dat", "-r", "48000", "-c", "2"]
    ltcdump_command = ["ltcdump", "-"]

    arecord_process = subprocess.Popen(command, stdout=subprocess.PIPE)
    ltcdump_process = subprocess.Popen(
        ["stdbuf", "-o0"] + ltcdump_command,
        stdin=arecord_process.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    while True:
        ltc_line = ltcdump_process.stdout.readline().strip()

        if ltcdump_process.poll() is not None:
            break  # Process has exited

        if (
            ltc_line
            and not ltc_line.startswith("#")
            and "User bits" not in ltc_line
        ):
            ltc_parts = ltc_line.split("|")
            if len(ltc_parts) > 0:
                ltc_timecode = ltc_parts[0].strip().split()[1]
                yield ltc_timecode