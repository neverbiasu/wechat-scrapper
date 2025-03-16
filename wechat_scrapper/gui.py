import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from .scrapper import WechatScrapper


class WechatGUI:
    def __init__(self, token="", cookie="", output_dir=None):
        self.token_var = tk.StringVar(value=token)
        self.cookie_var = tk.StringVar(value=cookie)
        self.output_dir = output_dir or os.getcwd()
        self.output_dir_var = tk.StringVar(value=self.output_dir)

        self.scrapper = None
        if token and cookie:
            self.scrapper = WechatScrapper(
                appmsg_token=token, cookie=cookie, output_dir=self.output_dir
            )

        self.root = tk.Tk()
        self.root.title("Wechat Scrapper GUI")
        self.create_widgets()

    def create_widgets(self):
        # 认证信息框架
        auth_frame = ttk.LabelFrame(self.root, text="认证信息")
        auth_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(auth_frame, text="Token:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5
        )
        token_entry = ttk.Entry(auth_frame, textvariable=self.token_var, width=50)
        token_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(auth_frame, text="Cookie:").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5
        )
        cookie_entry = ttk.Entry(auth_frame, textvariable=self.cookie_var, width=50)
        cookie_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        auth_button = ttk.Button(auth_frame, text="设置认证信息", command=self.set_auth)
        auth_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # 输出目录框架
        output_dir_frame = ttk.LabelFrame(self.root, text="输出设置")
        output_dir_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(output_dir_frame, text="输出目录:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5
        )
        output_entry = ttk.Entry(
            output_dir_frame, textvariable=self.output_dir_var, width=50
        )
        output_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        browse_button = ttk.Button(
            output_dir_frame, text="浏览...", command=self.browse_output_dir
        )
        browse_button.grid(row=0, column=2, padx=5, pady=5)

        # 操作框架
        action_frame = ttk.LabelFrame(self.root, text="操作")
        action_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(action_frame, text="URL 或 昵称:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.url_entry = ttk.Entry(action_frame, width=50)
        self.url_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(action_frame, text="模式 (下载用):").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.mode_entry = ttk.Entry(action_frame, width=10)
        self.mode_entry.insert(0, "4")  # 默认模式为4
        self.mode_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(action_frame, text="格式 (批量下载用):").grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.format_var = tk.StringVar(value="html")
        format_combo = ttk.Combobox(
            action_frame, textvariable=self.format_var, width=10
        )
        format_combo['values'] = ('html', 'pdf', 'markdown')
        format_combo.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        button_frame = ttk.Frame(action_frame)
        button_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.download_button = ttk.Button(
            button_frame,
            text="下载文章",
            command=self.download_article,
            state=tk.DISABLED,
        )
        self.download_button.pack(side=tk.LEFT, padx=5)

        self.batch_download_button = ttk.Button(
            button_frame,
            text="批量下载",
            command=self.batch_download,
            state=tk.DISABLED,
        )
        self.batch_download_button.pack(side=tk.LEFT, padx=5)

        self.info_button = ttk.Button(
            button_frame,
            text="获取文章信息",
            command=self.get_article_info,
            state=tk.DISABLED,
        )
        self.info_button.pack(side=tk.LEFT, padx=5)

        self.account_button = ttk.Button(
            button_frame,
            text="获取公众号信息",
            command=self.get_public_account_info,
            state=tk.DISABLED,
        )
        self.account_button.pack(side=tk.LEFT, padx=5)

        # 结果框架
        result_frame = ttk.LabelFrame(self.root, text="结果")
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.result_text = tk.Text(result_frame, wrap=tk.WORD, height=10)
        self.result_text.pack(fill="both", expand=True, padx=5, pady=5)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(self.result_text, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)

        if self.scrapper:
            self.enable_buttons()

    def browse_output_dir(self):
        """打开文件夹选择对话框"""
        directory = filedialog.askdirectory(initialdir=self.output_dir)
        if directory:  # 确保用户选择了目录
            self.output_dir = directory
            self.output_dir_var.set(directory)
            if self.scrapper:
                self.scrapper.output_dir = directory
                self.add_to_log(f"输出目录已设置为: {directory}")

    def set_auth(self):
        token = self.token_var.get()
        cookie = self.cookie_var.get()
        output_dir = self.output_dir_var.get()

        if not token or not cookie:
            messagebox.showerror("错误", "Token 和 Cookie 不能为空!")
            return

        try:
            self.output_dir = output_dir
            self.scrapper = WechatScrapper(
                appmsg_token=token, cookie=cookie, output_dir=output_dir
            )
            messagebox.showinfo("成功", "认证信息设置成功!")
            self.enable_buttons()
            self.add_to_log(f"已设置输出目录: {output_dir}")
        except Exception as e:
            messagebox.showerror("错误", f"认证信息设置失败: {str(e)}")

    def enable_buttons(self):
        self.download_button.config(state=tk.NORMAL)
        self.batch_download_button.config(state=tk.NORMAL)
        self.info_button.config(state=tk.NORMAL)
        self.account_button.config(state=tk.NORMAL)

    def add_to_log(self, message):
        """向日志文本框添加消息"""
        self.result_text.insert(tk.END, message + "\n")
        self.result_text.see(tk.END)  # 滚动到最新消息

    def download_article(self):
        if not self.scrapper:
            messagebox.showerror("错误", "请先设置认证信息!")
            return

        url = self.url_entry.get()
        if not url:
            messagebox.showerror("错误", "URL 不能为空!")
            return

        try:
            self.add_to_log(f"开始下载文章: {url}")
            mode = int(self.mode_entry.get())
            result = self.scrapper.download_article(url, mode)
            self.add_to_log(f"下载结果: {result}")
        except Exception as e:
            self.add_to_log(f"下载失败: {str(e)}")
            messagebox.showerror("错误", f"下载失败: {str(e)}")

    def batch_download(self):
        if not self.scrapper:
            messagebox.showerror("错误", "请先设置认证信息!")
            return

        nickname = self.url_entry.get()
        if not nickname:
            messagebox.showerror("错误", "公众号昵称不能为空!")
            return

        try:
            self.add_to_log(f"开始批量下载公众号 '{nickname}' 的文章...")
            format = self.format_var.get()
            result = self.scrapper.download_articles(nickname, format)
            self.add_to_log(f"批量下载结果: {result}")
        except Exception as e:
            self.add_to_log(f"批量下载失败: {str(e)}")
            messagebox.showerror("错误", f"批量下载失败: {str(e)}")

    def get_article_info(self):
        if not self.scrapper:
            messagebox.showerror("错误", "请先设置认证信息!")
            return

        url = self.url_entry.get()
        if not url:
            messagebox.showerror("错误", "URL 不能为空!")
            return

        try:
            result = self.scrapper.get_article_info(url)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, str(result))
        except Exception as e:
            messagebox.showerror("错误", f"获取文章信息失败: {str(e)}")

    def get_public_account_info(self):
        if not self.scrapper:
            messagebox.showerror("错误", "请先设置认证信息!")
            return

        nickname = self.url_entry.get()
        if not nickname:
            messagebox.showerror("错误", "公众号昵称不能为空!")
            return

        try:
            result = self.scrapper.get_public_account_info(nickname)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, str(result))
        except Exception as e:
            messagebox.showerror("错误", f"获取公众号信息失败: {str(e)}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    gui = WechatGUI()
    gui.run()
