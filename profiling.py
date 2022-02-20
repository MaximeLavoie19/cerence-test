from datetime import datetime
from multiprocessing import cpu_count
from typing import List
import matplotlib.pyplot as plt

from cerence_test import get_composed_words_of_length, get_composed_words_of_length_multi_thread


def profile_function(word_list: List[str], command, name) -> None:
    profile: List[float] = []
    x_list = []
    for length in range(0, len(word_list), 5000):
        x_list.append(length)
        start_time = datetime.now()
        command(word_list[:length])
        end_time = datetime.now()
        profile.append((end_time - start_time).total_seconds())
    plt.plot(x_list, profile, label=name)


if __name__ == '__main__':
    word_file = open("dictionary_58k", "r").read()
    words = word_file.split("\n")

    profile_function(words, lambda x: get_composed_words_of_length(x, 6), "single thread")
    profile_function(words, lambda x: get_composed_words_of_length_multi_thread(x, 6, cpu_count() * 2), "multi thread")
    plt.legend()
    plt.show()
