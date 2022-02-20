from datetime import datetime
from typing import Iterable, List
from multiprocessing import Pool, Manager, cpu_count


def get_words_of_length(word_list: Iterable[str], length: int) -> List[str]:
    return list(filter(lambda x: len(x) == length, word_list))


def get_words_of_length_smaller_than(word_list: Iterable[str], length: int) -> List[str]:
    return list(filter(lambda x: len(x) < length, word_list))


def add_new_composed_word(composed_word: str, word_list: List[str], composed_word_list: List[str]):
    if composed_word in word_list and composed_word not in composed_word_list:
        composed_word_list.append(composed_word)


def get_composed_words_of_length(word_list: Iterable[str], length: int):
    candidate_list = get_words_of_length(word_list, length)
    smaller_word_list = get_words_of_length_smaller_than(word_list, length - 1)
    composed_word_list: List[str] = []
    for index, smaller_word in enumerate(smaller_word_list):
        smaller_word_length = len(smaller_word)
        following_smaller_word_list = \
            [x for x in smaller_word_list[index + 1:] if len(x) == length - smaller_word_length]
        for following_smaller_word in following_smaller_word_list:
            add_new_composed_word(smaller_word + following_smaller_word, candidate_list, composed_word_list)
            add_new_composed_word(following_smaller_word + smaller_word, candidate_list, composed_word_list)
    return composed_word_list


def threaded_compose_word(
        index: int, length: int, smaller_word_list: List[str], candidate_list: List[str], composed_word_list: List[str]
):
    smaller_word = smaller_word_list[index]
    smaller_word_length = len(smaller_word)
    following_smaller_word_list = \
        [x for x in smaller_word_list[index + 1:] if len(x) == length - smaller_word_length]
    for following_smaller_word in following_smaller_word_list:
        add_new_composed_word(smaller_word + following_smaller_word, candidate_list, composed_word_list)
        add_new_composed_word(following_smaller_word + smaller_word, candidate_list, composed_word_list)


def get_composed_words_of_length_multi_thread(word_list: Iterable[str], length: int, nb_thread: int) -> List[str]:
    smaller_word_list = get_words_of_length_smaller_than(word_list, length - 1)
    candidate_list = get_words_of_length(word_list, length)
    manager = Manager()
    composed_word_list = manager.list([])
    with Pool(nb_thread) as pool:
        for index in range(len(smaller_word_list)):
            pool.apply_async(
                threaded_compose_word, (index, length, smaller_word_list, candidate_list, composed_word_list)
            )
        pool.close()
        pool.join()
    return composed_word_list


if __name__ == '__main__':
    # words = ["hot", "bird", "dog", "tailor", "writer", "hotdog", "or", "if", "tail"]
    word_file = open("dictionary_3k", "r").read()
    words = word_file.split("\n")

    start_time = datetime.now()

    composed_words = get_composed_words_of_length(words, 6)
    # 3k took 0:00.510005 0.5s
    # 58k took 1:04.978014 1m04s

    # composed_words = get_composed_words_of_length_multi_thread(words, 6, cpu_count() * 2)
    # 3k took 0:01.511999 1.5s
    # 58k took 0:18.606521 18s
    end_time = datetime.now()
    composed_words.sort()
    print("found", len(composed_words), "words")
    print(composed_words)
    print("took:", end_time - start_time)
