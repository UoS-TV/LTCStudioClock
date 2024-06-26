import socket
import struct
import time
from datetime import datetime, time, timedelta
from threading import Thread
import subprocess

# Function to serve modified NTP time
def serve_modified_ntp(server_socket, public_ntp_server, ltc_reader):
    while True:
        # Receive NTP request from client
        request_data, client_address = server_socket.recvfrom(48)
        print("Received NTP request from:", client_address)

        # Receive NTP response from public NTP server
        public_ntp_response = get_public_ntp_response(public_ntp_server)

        if public_ntp_response:
            # Extract timestamp from public NTP response
            public_timestamp = extract_timestamp(public_ntp_response)

            # Get LTC timecode
            ltc_timecode = ltc_reader.get_latest_timecode()

            # Modify timestamp with LTC timecode
            modified_timestamp = modify_timestamp(public_timestamp, ltc_timecode)

            # Construct modified NTP packet
            modified_ntp_packet = construct_modified_ntp_packet(modified_timestamp)
            
            # Check if modified packet is successfully constructed
            if modified_ntp_packet is not None:

                # Send modified NTP packet to client
                server_socket.sendto(modified_ntp_packet, client_address)
                print("Sent modified NTP response to:", client_address)
            else:
                print("Failed to construct modified NTP packet. Unable to send response.")

        else:
            print("Failed to receive NTP response from public server.")


# Function to retrieve public NTP response
def get_public_ntp_response(public_ntp_server):
    try:
        # Send NTP request to public NTP server
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.settimeout(5)  # Timeout for response
        client.sendto(b'\x1b' + 47 * b'\0', (public_ntp_server, 123))
        
        # Receive NTP response
        response_data, server_address = client.recvfrom(1024)
        return response_data
    except Exception as e:
        print("Failed to receive NTP response from public server:", e)
        return None
    finally:
        client.close()

# Function to extract timestamp from NTP response
def extract_timestamp(ntp_response):
    try:
        # Extract the 8-byte timestamp from the NTP response
        return struct.unpack("!Q", ntp_response[40:48])[0]
    except Exception as e:
        print("Failed to extract timestamp from public NTP response:", e)
        return None

def modify_timestamp(timestamp, ltc_timecode):
    try:
        # Convert NTP timestamp to datetime object
        ntp_time = datetime(1900, 1, 1) + timedelta(seconds=timestamp / (2 ** 32))

        # Parse LTC timecode to extract hours, minutes, seconds, and frames
        hours, minutes, seconds, frames = map(int, ltc_timecode.split(':'))

        # Create a time object representing LTC time
        ltc_time = time(hours, minutes, seconds, frames * 10000)  # Convert frames to microseconds

        # Combine date from NTP timestamp with time from LTC timecode
        modified_time = datetime.combine(ntp_time.date(), ltc_time)
        
        print("Modified Time:", modified_time)
        
        return modified_time
        
    except Exception as e:
        print("Failed to modify timestamp with LTC timecode:", e)
        return None

def construct_modified_ntp_packet(modified_timestamp):
    # Set the NTP packet fields
    leap_indicator = 0  # No leap second warning
    version_number = 4  # NTP version 4
    mode = 4  # Server mode

    stratum = 1  # Stratum level (we can set this to any value for testing)
    poll = 4  # Max polling interval
    precision = -6  # Clock precision (about 15.26 microseconds)

    root_delay = 0
    root_dispersion = 0
    reference_identifier = b"LTC"
    
    transmit_timestamp = int((modified_timestamp - datetime(1900, 1, 1)).total_seconds())
    print('Transmit Timestamp', transmit_timestamp)

    # Pack the fields into a binary NTP packet
    ntp_packet = struct.pack("!B B B b I I I I 4s", (leap_indicator << 6 | version_number << 3 | mode),
                             stratum, poll, precision,
                             int(root_delay), int(root_dispersion), int(transmit_timestamp), 0,
                             reference_identifier)

    return ntp_packet

# Example function to read LTC timecode from ltcdump output
class LTCReader:
    def __init__(self, audio_device):
        self.audio_device = audio_device
        self.latest_timecode = None
        self._running = True
        self.thread = Thread(target=self._read_ltc_timecode)
        self.thread.start()

    def _read_ltc_timecode(self):
        command = ["arecord", "-D", self.audio_device, "-f", "dat", "-r", "48000", "-c", "2"]
        ltcdump_command = ["ltcdump", "-"]

        arecord_process = subprocess.Popen(command, stdout=subprocess.PIPE)
        ltcdump_process = subprocess.Popen(
            ["stdbuf", "-o0"] + ltcdump_command,
            stdin=arecord_process.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        while self._running:
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
                    self.latest_timecode = ltc_timecode

    def get_latest_timecode(self):
        return self.latest_timecode

    def stop(self):
        self._running = False

# Initialize UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('0.0.0.0', 123))  # Bind to NTP port
print("NTP server listening on port 123...")

# Define public NTP server address
public_ntp_server = '0.pool.ntp.org'

# Start LTC timecode reader
ltc_reader = LTCReader("hw:3,0")  # Change "hw:3,0" to your audio device

# Start serving modified NTP time
serve_modified_ntp(server_socket, public_ntp_server, ltc_reader)
