from math import log as log
from numpy import zeros as zeros
from math import fabs as fabs
from math import floor as floor
from math import sqrt as sqrt
from scipy.special import erfc as erfc
from scipy.special import gammaincc as gammaincc


class TotOnline:

    @staticmethod
    def run_all_tests(binary_data: str):
        # Run total_failure_test
        p_value, result = TotOnline.total_failure_test(binary_data, 10)
        if not result:
            return False

        # Run monobit_test
        p_value, result = TotOnline.monobit_test(binary_data)
        if not result:
            return False

        # Run block_frequency_test
        p_value, result = TotOnline.block_frequency_test(binary_data, 128)
        if not result:
            return False

        # Run run_test
        p_value, result = TotOnline.run_test(binary_data)
        if not result:
            return False

        # Run longest_one_block_test
        p_value, result = TotOnline.longest_one_block_test(binary_data)
        if not result:
            return False

        # All tests passed
        return True

    @staticmethod
    def total_failure_test(binary_data: str, pattern_length=10):

        length_of_binary_data = len(binary_data)

        # Augment the n-bit sequence to create n overlapping m-bit sequences by appending m-1 bits
        # from the beginning of the sequence to the end of the sequence.
        binary_data += binary_data[:pattern_length + 1:]

        # Get max length one patterns for m, m-1, m-2
        max_pattern = ''
        for i in range(pattern_length + 2):
            max_pattern += '1'

        # Keep track of each pattern's frequency (how often it appears)
        vobs_01 = zeros(int(max_pattern[0:pattern_length:], 2) + 1)
        vobs_02 = zeros(int(max_pattern[0:pattern_length + 1:], 2) + 1)

        for i in range(length_of_binary_data):
            # Work out what pattern is observed
            vobs_01[int(binary_data[i:i + pattern_length:], 2)] += 1
            vobs_02[int(binary_data[i:i + pattern_length + 1:], 2)] += 1

        # Calculate the test statistics and p values
        vObs = [vobs_01, vobs_02]

        sums = zeros(2)
        for i in range(2):
            for j in range(len(vObs[i])):
                if vObs[i][j] > 0:
                    sums[i] += vObs[i][j] * log(vObs[i][j] / length_of_binary_data)
        sums /= length_of_binary_data
        ape = sums[0] - sums[1]

        xObs = 2.0 * length_of_binary_data * (log(2) - ape)

        p_value = gammaincc(pow(2, pattern_length - 1), xObs / 2.0)

        return p_value, (p_value >= 0.01)

    @staticmethod
    def monobit_test(binary_data: str):

        length_of_bit_string = len(binary_data)

        # Variable for S(n)
        count = 0
        # Iterate each bit in the string and compute for S(n)
        for bit in binary_data:
            if bit == 48:
                # If bit is 0, then -1 from the S(n)
                count -= 1
            elif bit == 49:
                # If bit is 1, then +1 to the S(n)
                count += 1

        # Compute the test statistic
        sObs = count / sqrt(length_of_bit_string)

        # Compute p-Value
        p_value = erfc(fabs(sObs) / sqrt(2))

        # return a p_value and randomness result
        return p_value, (p_value >= 0.01)

    @staticmethod
    def block_frequency_test(binary_data: str, block_size=128):

        length_of_bit_string = len(binary_data)

        if length_of_bit_string < block_size:
            block_size = length_of_bit_string

        # Compute the number of blocks based on the input given.  Discard the remainder
        number_of_blocks = floor(length_of_bit_string / block_size)

        if number_of_blocks == 1:
            # For block size M=1, this test degenerates to test 1, the Frequency (Monobit) test.
            return TotOnline.monobit_test(binary_data[0:block_size])

        # Initialized variables
        block_start = 0
        block_end = block_size
        proportion_sum = 0.0

        # Create a for loop to process each block
        for counter in range(number_of_blocks):
            # Partition the input sequence and get the data for block
            block_data = binary_data[block_start:block_end]

            # Determine the proportion 蟺i of ones in each M-bit
            one_count = 0
            for bit in block_data:
                if bit == 49:
                    one_count += 1
            # compute π
            pi = one_count / block_size

            # Compute Σ(πi -½)^2.
            proportion_sum += pow(pi - 0.5, 2.0)

            # Next Block
            block_start += block_size
            block_end += block_size

        # Compute 4M Σ(πi -½)^2.
        result = 4.0 * block_size * proportion_sum

        # Compute P-Value
        p_value = gammaincc(number_of_blocks / 2, result / 2)

        return p_value, (p_value >= 0.01)

    @staticmethod
    def run_test(binary_data: str):

        vObs = 0
        length_of_binary_data = len(binary_data)

        # Predefined tau = 2 / sqrt(n)
        tau = 2 / sqrt(length_of_binary_data)

        # Step 1 - Compute the pre-test proportion πof ones in the input sequence: π = Σjεj / n
        one_count = binary_data.count(49)

        pi = one_count / length_of_binary_data

        # Step 2 - If it can be shown that absolute value of (π - 0.5) is greater than or equal to tau
        # then the run test need not be performed.
        if abs(pi - 0.5) >= tau:
            return 0.0000
        else:
            # Step 3 - Compute vObs
            for item in range(1, length_of_binary_data):
                if binary_data[item] != binary_data[item - 1]:
                    vObs += 1
            vObs += 1

            # Step 4 - Compute p_value = erfc((|vObs − 2nπ * (1−π)|)/(2 * sqrt(2n) * π * (1−π)))
            p_value = erfc(abs(vObs - (2 * length_of_binary_data * pi * (1 - pi))) / (2 * sqrt(2 * length_of_binary_data) * pi * (1 - pi)))

        return p_value, (p_value > 0.01)

    @staticmethod
    def longest_one_block_test(binary_data: str):

        length_of_binary_data = len(binary_data)
        # print('Length of binary string: ', length_of_binary_data)

        # Initialized k, m. n, pi and v_values
        if length_of_binary_data < 128:
            # Not enough data to run this test
            return 0.00000, 'Error: Not enough data to run this test'
        elif length_of_binary_data < 6272:
            k = 3
            m = 8
            v_values = [1, 2, 3, 4]
            pi_values = [0.2148, 0.3672, 0.2305, 0.1875]
        elif length_of_binary_data < 750000:
            k = 5
            m = 128
            v_values = [4, 5, 6, 7, 8, 9]
            pi_values = [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
        else:
            # If length_of_bit_string > 750000
            k = 6
            m = 10000
            v_values = [10, 11, 12, 13, 14, 15, 16]
            pi_values = [0.0882, 0.2092, 0.2483, 0.1933, 0.1208, 0.0675, 0.0727]

        number_of_blocks = floor(length_of_binary_data / m)
        block_start = 0
        block_end = m
        xObs = 0
        # This will initialize an array with a number of 0 you specified.
        frequencies = zeros(k + 1)

        # print('Number of Blocks: ', number_of_blocks)

        for count in range(number_of_blocks):
            block_data = binary_data[block_start:block_end]
            max_run_count = 0
            run_count = 0

            # This will count the number of ones in the block
            for bit in block_data:
                if bit == 49:
                    run_count += 1
                    max_run_count = max(max_run_count, run_count)
                else:
                    max_run_count = max(max_run_count, run_count)
                    run_count = 0

            max(max_run_count, run_count)

            # print('Block Data: ', block_data, '. Run Count: ', max_run_count)
            if max_run_count < v_values[0]:
                frequencies[0] += 1
            for j in range(k):
                if max_run_count == v_values[j]:
                    frequencies[j] += 1
            if max_run_count > v_values[k - 1]:
                frequencies[k] += 1

            block_start += m
            block_end += m

        # print("Frequencies: ", frequencies)
        # Compute xObs
        for count in range(len(frequencies)):
            xObs += pow((frequencies[count] - (number_of_blocks * pi_values[count])), 2.0) / (
                    number_of_blocks * pi_values[count])

        p_value = gammaincc(float(k / 2), float(xObs / 2))

        return p_value, (p_value > 0.01)
