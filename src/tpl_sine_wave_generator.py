from math import pi, sin
import matplotlib.pyplot as plt
import struct
import numpy as np
# from array import array
import os

"""
Code used to generate a sine wave that changes linearly between 2 frequencies. 
Then the sine wave is saved in a template file for HEKA PatchMaster software. 

The parameters are:
- min and max frequency
- Total amplitude (in mV) and mean voltage (in mV) of the signal
- Duration in seconds
- Sampling rate
"""


def save_in_file(file_name, data):
    """
    Use to save the data in the template file.
    According to HEKA patchmaster documentation regarding template files:
    Data format: The file must contain one voltage value per
    stimulus point. The voltage value must be a ”short” (4 byte),
    binary IEEE-floating point format number. All values must be in
    volt, i.e., if a voltage of ”-80 mV” has to be output, then the required
    value is ”-0.080”.

    :param file_name: path + file_name of the file in which the data will be save.
    Data will be save in a binary format. The file should have .tpl extension to be used in Patchmaster
    See doc: http://www.heka.com/support/tutorials/tutorials_down/pm_tutorial_stimulustemplate.pdf
    :param data:
    :return:
    """
    f = open(file_name, 'wb')

    # '<' for little endian, see doc for other format
    # https://docs.python.org/3/library/struct.html#format-characters
    float_array = struct.pack('<' + ('f' * len(data)), *data)

    # another solution to encode the data, not tested
    # https://docs.python.org/3/library/array.html
    # float_array = array('f', data)

    f.write(float_array)
    f.close()


def generate_sin_wave(start_freq, end_freq, duration, n_steps, amplitude):
    """
    Generate a linearly increasing or decreasing sin wave.

    Inspired by:
https://stackoverflow.com/questions/19771328/sine-wave-that-exponentialy-changes-between-frequencies-f1-and-f2-at-given-time

    :param start_freq: Start frequency
    :param end_freq: End frequency (could be < or > to start freq)
    :param duration: Duration in seconds
    :param n_steps: Number of steps, aka number of values returned
    :param amplitude: Amplitude of the signal
    :return:
    """
    time_values = []
    y_values = []
    for i in range(n_steps):
        delta = i / float(n_steps)
        t = duration * delta
        phase = 2 * pi * t * (start_freq + (end_freq - start_freq) * delta / 2)
        time_values.append(t)
        y_values.append(amplitude * sin(phase))
    return time_values, y_values


def main():
    """
    Main function
    :return:
    """

    # path and file_name
    # f_path = "/media/julien/Not_today/hne_not_today/results_hne/laurent/"
    f_path = "/Users/pappyhammer/Documents/academique/these_inmed/patchmaster_tpl_github/results"
    file_name = os.path.join(f_path, "sin_wave_fct_current.tpl")

    # set to True to plot the sin wave
    plot_wave = True
    # parameters to set
    # how many to point to save by seconds. Should be the same as the frequency acquisition you will be using in
    # patchmaster
    sampling_rate = 10000
    # duration in seconds
    duration_sec = 30
    n_steps = duration_sec * sampling_rate
    # amplitude in mV
    amplitude = 0.05
    # Average voltage
    # then max value is mean_voltage + amplitude, and min is mean_voltage - amplitude
    mean_voltage = 0
    # for a linearly increasing frequency, min_freq should be superior to end_freq
    # for a linearly decreasing frequency, just do the opposite
    start_freq = 0
    end_freq = 15
    time_values, voltage_values = generate_sin_wave(start_freq, end_freq, duration=duration_sec,
                                                    n_steps=n_steps, amplitude=amplitude)
    # centering the values around the mean voltage defined
    voltage_values = [y - mean_voltage for y in voltage_values]

    # saving data in the file
    save_in_file(file_name, voltage_values)

    if plot_wave:
        plt.plot(time_values, voltage_values)
        plt.show()


if __name__ == "__main__":
    main()
