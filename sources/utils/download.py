from pathlib import Path
from typing import List, Tuple, Union

from bs4 import BeautifulSoup
from httpx import Response, get


DATASET_DIR = Path.cwd() / "datasets"
LETTERS_DIR = DATASET_DIR / "letters"


def _get_soup(web_link: Union[str, Response]) -> BeautifulSoup:
    if isinstance(web_link, str):
        return BeautifulSoup(get(web_link).text, features="html.parser")
    else:
        return BeautifulSoup(web_link.text, features="html.parser")


def download_letters(save_dataset: bool = True) -> List[Tuple[str, List[bytes]]]:
    letters = list()
    letter_index = 1

    if save_dataset:
        LETTERS_DIR.mkdir(parents=True, exist_ok=True)

    while True:
        base_link = f"http://webs2.uci.umk.pl/nct/en/archives/letters/2/{letter_index}/"
        response = get(base_link)
        if response.status_code != 200:
            break

        links_list = _get_soup(response).find_all("ul")[0].find_all("li")
        photo_link = f"{base_link}{links_list[1].find('a', href=True)['href']}"
        transcription_link = f"{base_link}{links_list[2].find('a', href=True)['href']}"

        transcription_lines = _get_soup(transcription_link).find_all("p")
        transcription_data = "\n".join([trs.text for trs in transcription_lines[2:]])

        if save_dataset:
            photo_file = LETTERS_DIR / f"{letter_index}.txt"
            photo_file.write_text(transcription_data)

        photo_data = list()
        while photo_link is not None:
            photo_soup = _get_soup(photo_link)
            photo_image_elem = photo_soup.find("img", id="obrazek_uchwyt")
            photo_image_link = f"{base_link}{photo_image_elem['src']}"
            photo_data += [(get(photo_image_link).content, photo_image_link.split(".")[-1])]
            photo_next = photo_soup.find("a", href=True, text="next")
            photo_link = f"{base_link}{photo_next['href']}" if photo_next is not None else None

        if save_dataset:
            for idx, (data, ext) in enumerate(photo_data):
                photo_file = LETTERS_DIR / f"{letter_index}-{idx+1}.{ext}"
                photo_file.write_bytes(data)

        letters += [(transcription_data, photo_data)]
        letter_index += 1

    print(f"Loaded {letter_index - 1} letter pages!")
    return letters
