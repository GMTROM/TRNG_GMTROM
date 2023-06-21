from math import fabs as fabs
from math import sqrt as sqrt
from scipy.special import erfc as erfc
import numpy as np
from scipy import stats


class StartUPTest:

    @staticmethod
    def run_all_tests(binary_data: str):
        # Run monobit_test
        p_value, result = StartUPTest.monobit_test(binary_data)
        if not result:
            return False

        # Run chi_square
        p_value, result, chi2_statistic = StartUPTest.chi_square(binary_data)
        if not result:
            return False

        # All tests passed
        return True

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
    def chi_square(binary_data: str):

        observed_frequencies = [binary_data.count(48), binary_data.count(49)]
        expected_probabilities = [0.5, 0.5]  # Assuming equal probability for each bit value
        total_observations = len(binary_data)
        expected_frequencies = np.array(expected_probabilities) * total_observations

        chi2_statistic, p_value = stats.chisquare(observed_frequencies, f_exp=expected_frequencies)

        return p_value, p_value >= 0.01, chi2_statistic