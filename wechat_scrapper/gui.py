import tkinter as tk
from tkinter import ttk, messagebox
from .scrapper import WechatScrapper


class WechatGUI:
    def __init__(self):
        self.scrapper = WechatScrapper(
            appmsg_token="your_appmsg_token", cookie="your_cookie"
        )
        self.root = tk.Tk()
        self.root.title("Wechat Scrapper GUI")
        self.create_widgets()

    def create_widgets(self):
        self.url_label = ttk.Label(self.root, text="Enter URL or Nickname:")
        self.url_label.pack(pady=5)

        self.url_entry = ttk.Entry(self.root, width=50)
        self.url_entry.pack(pady=5)

        self.mode_label = ttk.Label(self.root, text="Enter Mode (for download):")
        self.mode_label.pack(pady=5)

        self.mode_entry = ttk.Entry(self.root, width=10)
        self.mode_entry.pack(pady=5)

        self.result_label = ttk.Label(self.root, text="")
        self.result_label.pack(pady=5)

        self.download_button = ttk.Button(
            self.root, text="Download Article", command=self.download_article
        )
        self.download_button.pack(pady=5)

        self.info_button = ttk.Button(
            self.root, text="Get Article Info", command=self.get_article_info
        )
        self.info_button.pack(pady=5)

        self.account_button = ttk.Button(
            self.root,
            text="Get Public Account Info",
            command=self.get_public_account_info,
        )
        self.account_button.pack(pady=5)

    def download_article(self):
        url = self.url_entry.get()
        mode = int(self.mode_entry.get())
        result = self.scrapper.download_article(url, mode)
        self.result_label.config(text=result)

    def get_article_info(self):
        url = self.url_entry.get()
        result = self.scrapper.get_article_info(url)
        self.result_label.config(text=result)

    def get_public_account_info(self):
        nickname = self.url_entry.get()
        result = self.scrapper.get_public_account_info(nickname)
        self.result_label.config(text=result)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    gui = WechatGUI()
    gui.run()
