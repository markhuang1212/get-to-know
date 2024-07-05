import json
from typing import Type

from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from langchain_core.tools import tool
from selenium import webdriver
from selenium.webdriver.common.by import By


@tool
def fetch_web(url: str):
    """Fetch text and links from a webpage. Call only one time per function call."""
    try:
        options = webdriver.ChromeOptions()
        # options.add_argument("user-data-dir=/home/admin/.config/google-chrome")
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(10)
        try:
            driver.get(url=url)
        except Exception as e:
            pass

        body = driver.find_element(By.TAG_NAME, "body")
        text = body.text
        link_elems = driver.find_elements(By.TAG_NAME, "a")
        links = [
            {"href": elem.get_attribute("href"), "text": elem.text}
            for elem in link_elems
        ]
        links = list(filter(lambda x: x["text"] != "" and x["href"] != "", links))

        driver.close()
        return json.dumps({"text": text, "links": links})
    except Exception as e:
        print(f"Error when executing function: {str(e)}")
        return json.dumps({"error": f"Error when executing function: {str(e)}"})


