import re
import html


def display_progress_bar(current_iteration: int, total_iterations: int):
    """
    Displays a progress bar in the console.

    :param current_iteration: The current iteration number.
    :param total_iterations: The total number of iterations.
    """
    percentage = round(current_iteration / total_iterations * 100)
    print(f"\rProgress: [{'#' * percentage}{' ' * (100 - percentage)}] {percentage}%", end="")


def remove_text_in_parentheses(text: str) -> str:
    """
    Removes text enclosed in parentheses from the given string.

    :param text: The input string.
    :return: A string with text inside parentheses removed.
    """
    return re.sub(r'\([^)]*\)', '', text).strip()


def normalize_text(text: str) -> str:
    """
    Normalizes the given text by unescaping HTML entities, replacing non-breaking spaces, and removing extra
    whitespaces.

    :param text: The input string.
    :return: A normalized string.
    """
    # HTML unescape the text
    text = html.unescape(text)

    # Replace non-breaking spaces
    text = text.replace("\xa0", " ")

    # Remove extra whitespaces
    text = re.sub(r'\s+', " ", text).strip()

    return text


def exclude_degree_titles(education_list: list[str]) -> list[str]:
    """
    Filters out common degree titles from a list of education entries.

    :param education_list: A list of education entries.
    :return: A list with degree titles removed.
    """
    degrees = {"bsc", "msc", "phd", "bs", "ms", "ba", "ma", "beng", "meng", "dphil", "sb", "sm", "scd"}
    return [entry for entry in education_list if entry.replace(".", "").lower().strip() not in degrees]


def exclude_references(education_list: list[str]) -> list[str]:
    """
    Filters out entries that appear to be references (e.g., '[1]', '[2]') from a list of education entries.

    :param education_list: A list of education entries.
    :return: A list with reference entries removed.
    """
    return [entry for entry in education_list if re.match(r'\[\d+]', entry) is None]
