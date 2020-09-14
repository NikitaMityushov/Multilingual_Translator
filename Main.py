import requests
from bs4 import BeautifulSoup
import sys


AVAIL_LANG = ["arabic", "german", "english", "spanish", "french", "hebrew", "japanese", "dutch", "polish", "portuguese",
              "romanian", "russian", "turkish"]
available_languages_for_menu = '''Hello, you're welcome to the translator. Translator supports: 
1. Arabic
2. German
3. English
4. Spanish
5. French
6. Hebrew
7. Japanese
8. Dutch
9. Polish
10. Portuguese
11. Romanian
12. Russian
13. Turkish"'''
# create http session
session = requests.Session()
# arguments from command line
args = sys.argv


def menu():
    num_of_input_lang = input(available_languages_for_menu + "\nType the number of your language:")
    input_lang = __return_language(num_of_input_lang)
    num_of_output_lang = input("Type the number of language you want to translate to: ")
    output_lang = __return_language(num_of_output_lang)
    chosen_word = input("Type the word you want to translate:").lower().replace(" ", "+")
    return input_lang, output_lang, chosen_word


def __return_language(num_of_lang):
    if num_of_lang == "0":
        return "all"
    elif num_of_lang == "1":
        return "arabic"
    elif num_of_lang == "2":
        return "german"
    elif num_of_lang == "3":
        return "english"
    elif num_of_lang == "4":
        return "spanish"
    elif num_of_lang == "5":
        return "french"
    elif num_of_lang == "6":
        return "hebrew"
    elif num_of_lang == "7":
        return "japanese"
    elif num_of_lang == "8":
        return "dutch"
    elif num_of_lang == "9":
        return "polish"
    elif num_of_lang == "10":
        return "portuguese"
    elif num_of_lang == "11":
        return "romanian"
    elif num_of_lang == "12":
        return "russian"
    elif num_of_lang == "13":
        return "turkish"
    else:
        return "No such lang"


def process_the_request(URL):
    response = session.get(URL, headers={'User-Agent': 'Mozilla/5.0'})

    if int(response.status_code) < 400:
        soup = BeautifulSoup(response.content, 'html.parser')
        print(f"{response.status_code} OK")

        words = [i.text.strip('\n " "') for i in soup.find_all('a', {'class': "translation"})]
        phrases_list = [(i.text.strip('\n " " []')) for i in soup.select("#examples-content .text")]
        return words, phrases_list

    else:
        return response.status_code, "File not found"


def print_the_results(trans_content, exam_content, out_lang):
    result1 = f"\nContext examples:\n\n{out_lang.capitalize()} Translations:"

    for word in trans_content:
        result1 += "\n" + word
    print(result1)

    result2 = f"\n{out_lang.capitalize()} Examples:"

    for i in range(0, len(exam_content), 2):
        result2 += "\n" + exam_content[i] + "\n" + exam_content[i + 1] + "\n\n"

    print(result2)


def process_ALL_request(input_lang, chosen_word):
    result_string = ""

    for output_lang in AVAIL_LANG:
        if input_lang != output_lang:
            URL = f"https://context.reverso.net/translation/{input_lang}-{output_lang}/{chosen_word}"
            response = session.get(URL, headers={'User-Agent': 'Mozilla/5.0'})

            if int(response.status_code) < 400:
                soup = BeautifulSoup(response.content, 'html.parser')
                words = [i.text.strip('\n " "') for i in soup.find_all('a', {'class': "translation"})]
                phrases_list = [(i.text.strip('\n " " []')) for i in soup.select("#examples-content .text")]
                result_string += f"\n\n{output_lang.capitalize()} Translations:\n{words[1]}\n\n{output_lang.capitalize()} Examples:\n{phrases_list[0]}\n{phrases_list[1]}"
            else:
                raise TypeError

    __save_to_file(chosen_word, result_string.strip())
    print(result_string.strip())


def __save_to_file(chosen_word, result_string):
    with open(f"{chosen_word}.txt", "w", encoding="utf-8") as file:
        file.write(result_string)


def load_from_file():
    pass


def __check_is_valid_lang(input_lang, output_lang):
    if input_lang not in AVAIL_LANG:
        raise ValueError(print(f"Sorry, the program doesn't support {input_lang}"))
    elif output_lang not in AVAIL_LANG and output_lang != "all":
        raise ValueError(print(f"Sorry, the program doesn't support {output_lang}"))


# Entry point of the program
def main():
    if len(args) > 3:
        try:
            input_lang = args[1].lower()
            output_lang = args[2].lower()
            __check_is_valid_lang(input_lang, output_lang)
            chosen_word = ""
            for word in args[3: len(args)]:
                chosen_word += word + "+"

            chosen_word = chosen_word.strip("+ " "")

            if output_lang == "all":
                process_ALL_request(input_lang, chosen_word)
            else:

                URL = f"https://context.reverso.net/translation/{input_lang}-{output_lang}/{chosen_word}"

                trans_content, exam_content = process_the_request(URL)

                print_the_results(trans_content, exam_content, output_lang)
        except ValueError:
            pass
        except TypeError:
            print(f"Sorry, unable to find {chosen_word}")
        except ConnectionAbortedError:
            print("Something wrong with your internet connection")

    else:
        try:
            input_lang, output_lang, chosen_word = menu()
            __check_is_valid_lang(input_lang, output_lang)
            if output_lang == "all":
                process_ALL_request(input_lang, chosen_word)
            else:

                URL = f"https://context.reverso.net/translation/{input_lang}-{output_lang}/{chosen_word}"

                trans_content, exam_content = process_the_request(URL)

                print_the_results(trans_content, exam_content, output_lang)
        except ValueError:
            pass
        except TypeError:
            print(f"Sorry, unable to find {chosen_word}")
        except ConnectionAbortedError:
            print("Something wrong with your internet connection")


# start the program
main()

