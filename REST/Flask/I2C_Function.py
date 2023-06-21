import os
import time
import json
from flask import jsonify
from smbus import SMBus
from StartUpTest import StartUPTest
from TotOnline import TotOnline

def read_data(num_numbers, bits_per_number):
    addr = 0x8
    bus = SMBus(1)

    # Calculate the total number of bytes required to accommodate the desired number of bits
    total_bytes = (num_numbers * bits_per_number + 7) // 8

    # Define the filename
    filename = f'{num_numbers}numbers_{bits_per_number}bits.bin'

    try:
        with open(filename, 'wb') as file:
            bytes_received = 0
            while bytes_received < total_bytes:
                # Read a byte from the serial port
                data = bus.read_byte(addr)
                file.write(bytes([data]))
                bytes_received += 1
                time.sleep(0.0000001)

        return filename

    except IOError as e:
        return False

def convert_to_hex(binary_filename, num_numbers, bits_per_number):
    with open(binary_filename, 'r') as f:
        # Read the contents of the file
        binary_content = f.read()

    # Calculate the number of bits per chunk
    bits_per_chunk = len(binary_content) // num_numbers

    # Divide the binary content into equal chunks
    binary_chunks = [binary_content[i * bits_per_chunk:(i + 1) * bits_per_chunk] for i in range(num_numbers)]

    # Calculate the number of hexadecimal digits per chunk
    hex_digits_per_chunk = (bits_per_chunk + 3) // 4  # Round up to the nearest integer

    # Convert each binary chunk to a hexadecimal string with leading zeros
    hex_chunks = [format(int(chunk, 2), f'0{hex_digits_per_chunk}X') for chunk in binary_chunks]

    # Write the hex chunks to the file with separators and newlines
    hex_filename = f'{num_numbers}numbers_{bits_per_number}bits.txt'
    with open(hex_filename, 'w') as f:
        for i in range(num_numbers):
            hex_number = hex_chunks[i]
            # write the separator between numbers except for the last one
            if i != num_numbers - 1:
                hex_number += ';'
            f.write(hex_number)

    return hex_filename


def convert_to_binary(filename, num_numbers, bits_per_number):
    with open(filename, 'rb') as f:
        # Read the contents of the file as bytes
        content = f.read()

    # Convert the bytes to a string of binary digits
    binary_str = ''.join(format(byte, '08b') for byte in content)

    # Truncate the binary string to the desired length
    truncated_binary_str = binary_str[:num_numbers * bits_per_number]

    # Write the truncated binary string back to the file with separators
    binary_filename = f'{num_numbers}numbers_{bits_per_number}bits_binary.txt'
    with open(binary_filename, 'w') as f:
        for i in range(0, len(truncated_binary_str), bits_per_number):
            binary_number = truncated_binary_str[i:i+bits_per_number]
            f.write(binary_number)

    return binary_filename


def process_data_in_chunks(data, chunk_size=1000000):
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    return chunks

def perform_startup_tests(filename):
    with open(filename, 'rb') as f:
        # Read the contents of the file as bytes
        content = f.read()

        #print("Run all StartUPTests")
        binary_chunks = process_data_in_chunks(content)
        first_chunk = binary_chunks[0]
        result = StartUPTest.run_all_tests(first_chunk)
        #print(result)
        return result
        
def perform_tot_online_tests(filename):
    with open(filename, 'rb') as f:
        # Read the contents of the file as bytes
        content = f.read()

        #print("Run all TotOnline tests")
        binary_chunks = process_data_in_chunks(content)
        first_chunk = binary_chunks[0]
        result = TotOnline.run_all_tests(first_chunk)
        #print(result)
        return result

def analyze_data(num_numbers, bits_per_number, startup):

    if startup:
        filename = read_data(10, 80000)
        if not filename:
            return False
        binary_filename = convert_to_binary(filename, 10, 80000)
        perform_startup_tests(binary_filename)
        perform_tot_online_tests(binary_filename)
        os.unlink(filename)
        os.unlink(binary_filename)
        return True
    else:
        filename = read_data(10, 20000)
        if not filename:
            return False
        binary_filename = convert_to_binary(filename, 10, 20000)
        result = perform_tot_online_tests(binary_filename)
        os.unlink(filename)
        os.unlink(binary_filename)
        if result:
            filename = read_data(num_numbers, bits_per_number)
            binary_filename = convert_to_binary(filename, num_numbers, bits_per_number)
            hex_filename = convert_to_hex(binary_filename, num_numbers, bits_per_number)            
            # Read the hex numbers from the file
            with open(hex_filename, 'rb') as f:
                hex_numbers_bytes = f.read()
                # Decode the bytes to a string
                hex_numbers_str = hex_numbers_bytes.decode('utf-8')
                # Split the semicolon-separated string into a list of hex numbers
                hex_numbers = hex_numbers_str.split(';')
                # Remove any empty strings
                hex_numbers = [hex_num for hex_num in hex_numbers if hex_num]
                # Create the JSON object with the specified structure
                #data = {'randomNumbers': hex_numbers}
                data = hex_numbers
                # Delete the temporary files
                os.unlink(filename)
                os.unlink(binary_filename)
                os.unlink(hex_filename)   
                # Return the JSON object using Flask's jsonify function
                #return jsonify(data)
                return json.dumps(data)            
                
        else:
            return 400

# Teste den Code
#result = analyze_data(8, 8, startup=True)
#print(result)
#result = analyze_data(1, 7200000, startup=False)
#result = analyze_data(10, 100, startup=False)
#print(result)

