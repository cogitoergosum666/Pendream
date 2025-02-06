import tkinter as tk
from PIL import Image, ImageDraw


class HandwritingApp:
    def __init__(self):
        self.canvas_width = 400
        self.canvas_height = 300
        self.last_x = None  # Initialize to None
        self.last_y = None  # Initialize to None

    def paint(self, event):
        x, y = event.x, event.y
        if self.last_x is not None and self.last_y is not None:
            # Draw on the canvas
            self.canvas.create_line((self.last_x, self.last_y, x, y), fill="black", width=5)
            # Draw on the image
            self.draw.line((self.last_x, self.last_y, x, y), fill="black", width=5)
        self.last_x, self.last_y = x, y

    def reset(self, event):
        self.last_x = None
        self.last_y = None

    def save_image(self):
        # Save the image
        self.image.save("handwriting.png")
        print("Successfully saved!")

    def writing_board(self):
        # Destroy the previous instance of Tk if it exists
        if hasattr(self, 'root') and self.root.winfo_exists():
            self.root.destroy()

        # Create a new Tk instance
        self.root = tk.Tk()
        self.root.title("Answer")

        # Create the canvas
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        # Create the image object for drawing
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Bind mouse events
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

        # Add save button
        self.save_button = tk.Button(self.root, text="Save", command=self.save_image)
        self.save_button.pack()

        # Start the Tk main loop
        self.root.mainloop()




# class HandwritingApp:
#     def __init__(self, root = tk.Tk()):
#         self.root = tk.Tk()
#         self.root.title("Answer")

#         # 设置画布大小
#         self.canvas_width = 400
#         self.canvas_height = 300
#         self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="white")
#         self.canvas.pack()

#         # 创建图像对象，用于保存绘图内容
#         self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
#         self.draw = ImageDraw.Draw(self.image)

#         # 绑定鼠标事件
#         self.canvas.bind("<B1-Motion>", self.paint)  # 鼠标拖动绘图
#         self.canvas.bind("<ButtonRelease-1>", self.reset)  # 鼠标松开时停止绘图

#         # 设置起始点
#         self.last_x, self.last_y = None, None

#         # 添加保存按钮
#         self.save_button = tk.Button(root, text="save", command=self.save_image)
#         self.save_button.pack()

#     def paint(self, event):
#         x, y = event.x, event.y
#         if self.last_x is not None and self.last_y is not None:
#             # 在画布上绘制线条
#             self.canvas.create_line((self.last_x, self.last_y, x, y), fill="black", width=5)
#             # 同时在图像对象上绘制线条
#             self.draw.line((self.last_x, self.last_y, x, y), fill="black", width=5)
#         self.last_x, self.last_y = x, y

#     def reset(self, event):
#         self.last_x, self.last_y = None, None

#     def save_image(self):
#         # 保存图像为文件
#         self.image.save("handwriting.png")
#         print("Successfully saved!")

#     def writing_board(self):
#         '''
#         initate the writing board, save the image as handwriting.png when user click save
#         '''
#         self.root.mainloop()

#if __name__ == "__main__":
    # root = tk.Tk()
    # app = HandwritingApp(root)
    # root.mainloop()
    # app = HandwritingApp()
    # app.writing_board()