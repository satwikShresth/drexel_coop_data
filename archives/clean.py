from bs4 import BeautifulSoup

file_path = "./test/1.html"


def fileStrip(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    with open(file_path, "r", encoding="utf-8") as file:
        html_content_list = file.readlines()

    soup = BeautifulSoup(html_content, "html.parser")

    return_imgs = soup.find_all(
        "img", {"title": "Return", "name": "Return Button"})

    if len(return_imgs) >= 2:
        start_tag = return_imgs[0].sourceline
        end_tag = return_imgs[1].sourceline

        html_content_list = html_content_list[start_tag+1:end_tag-1]
        html_content_list = html_content_list

        # for idx,val in enumerate(html_content_list):
        #     if str(start_tag_replaced) in val:
        #         print(idx)
        #         html_content_list = html_content_list[idx:]

        # for idx,val in enumerate(html_content_list):
        #     if str(start_tag_replaced) in val:
        #         print(idx)
        #         html_content_list = html_content_list[:idx]

    html = '\n'.join(html_content_list)

    with open(file_path, "w+", encoding="utf-8") as file:
        file.write(BeautifulSoup(html.replace(
            "&nbsp;", "I"), "html.parser").getText())
