import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from googletrans import Translator
import threading

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文本翻译器")
        self.root.geometry("800x600")
        
        # 创建翻译器实例
        self.translator = Translator()
        
        # 创建界面元素
        self.create_widgets()
        
    def create_widgets(self):
        # 按钮框架
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        # 选择文件按钮
        self.select_btn = tk.Button(btn_frame, text="选择文件", command=self.select_file)
        self.select_btn.pack(side=tk.LEFT, padx=5)
        
        # 翻译按钮
        self.translate_btn = tk.Button(btn_frame, text="开始翻译", command=self.start_translation)
        self.translate_btn.pack(side=tk.LEFT, padx=5)
        
        # 保存按钮
        self.save_btn = tk.Button(btn_frame, text="保存翻译", command=self.save_translation)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # 文本显示区域
        text_frame = tk.Frame(self.root)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # 原文显示
        self.source_text = scrolledtext.ScrolledText(text_frame, height=15)
        self.source_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 翻译结果显示
        self.translated_text = scrolledtext.ScrolledText(text_frame, height=15)
        self.translated_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
    def select_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.source_text.delete(1.0, tk.END)
                    self.source_text.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("错误", f"读取文件时出错: {str(e)}")
                
    def start_translation(self):
        content = self.source_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("警告", "请先选择要翻译的文本文件！")
            return
            
        def translate():
            try:
                self.translate_btn.config(state=tk.DISABLED)
                result = self.translator.translate(content, dest='zh-cn')
                self.translated_text.delete(1.0, tk.END)
                self.translated_text.insert(tk.END, result.text)
            except Exception as e:
                messagebox.showerror("错误", f"翻译过程中出错: {str(e)}")
            finally:
                self.translate_btn.config(state=tk.NORMAL)
                
        # 使用线程避免界面卡顿
        threading.Thread(target=translate, daemon=True).start()
        
    def save_translation(self):
        translated_content = self.translated_text.get(1.0, tk.END).strip()
        if not translated_content:
            messagebox.showwarning("警告", "没有可保存的翻译内容！")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(translated_content)
                messagebox.showinfo("成功", "翻译结果已保存！")
            except Exception as e:
                messagebox.showerror("错误", f"保存文件时出错: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()