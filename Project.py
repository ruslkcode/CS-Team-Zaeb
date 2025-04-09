from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import struct
import numpy as np

class ImageProcessor:
    def __init__(self):
        self.window = Tk()
        self.window.title("Matrix Image Processor")
        self.window.geometry("800x600")
        
        # Variables
        self.original_image = None
        self.processed_image = None
        self.original_matrix = None
        self.processed_matrix = None
        self.display_scale = 1.0
        
        # Create GUI
        self.create_gui()
    
    def create_gui(self):
        # Main frame
        main_frame = Frame(self.window, padx=10, pady=10)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Control buttons
        control_frame = Frame(main_frame)
        control_frame.pack(fill=X, pady=5)
        
        Button(control_frame, text="Load Image", command=self.load_image).pack(side=LEFT, padx=5)
        Button(control_frame, text="Save Image", command=self.save_image).pack(side=LEFT, padx=5)
        
        # Transform buttons
        transform_frame = Frame(main_frame)
        transform_frame.pack(fill=X, pady=5)
        
        Button(transform_frame, text="Rotate 90°", command=lambda: self.rotate_image(90)).pack(side=LEFT, padx=5)
        Button(transform_frame, text="Rotate 180°", command=lambda: self.rotate_image(180)).pack(side=LEFT, padx=5)
        Button(transform_frame, text="Rotate 270°", command=lambda: self.rotate_image(270)).pack(side=LEFT, padx=5)
        Button(transform_frame, text="Flip Horizontal", command=self.flip_horizontal).pack(side=LEFT, padx=5)
        Button(transform_frame, text="Flip Vertical", command=self.flip_vertical).pack(side=LEFT, padx=5)
        
        # Image display
        self.image_frame = Frame(main_frame)
        self.image_frame.pack(fill=BOTH, expand=True)
        
        # Original image label
        self.original_label = Label(self.image_frame)
        self.original_label.pack(side=LEFT, padx=5)
        
        # Processed image label
        self.processed_label = Label(self.image_frame)
        self.processed_label.pack(side=LEFT, padx=5)
        
        # Status label
        self.status_label = Label(main_frame, text="Ready to load image", bd=1, relief=SUNKEN, anchor=W)
        self.status_label.pack(side=BOTTOM, fill=X)
    
    def update_status(self, message):
        self.status_label.config(text=message)
        self.window.update_idletasks()
    
    def load_image(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Image files", "*.bmp;*.jpg;*.png")]
            )
            if file_path:
                self.update_status("Loading image...")
                # Load image using Pillow
                self.original_image = Image.open(file_path).convert('L')  # Convert to grayscale
                self.processed_image = self.original_image.copy()
                
                # Convert to matrix
                self.original_matrix = self.image_to_matrix(self.original_image)
                self.processed_matrix = [row[:] for row in self.original_matrix]
                
                self.display_images()
                self.update_status(f"Image loaded: {os.path.basename(file_path)}")
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def image_to_matrix(self, image):
        """Convert PIL Image to matrix"""
        width, height = image.size
        matrix = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(image.getpixel((x, y)))
            matrix.append(row)
        return matrix
    
    def matrix_to_image(self, matrix):
        """Convert matrix to PIL Image"""
        height = len(matrix)
        width = len(matrix[0])
        image = Image.new('L', (width, height))
        for y in range(height):
            for x in range(width):
                image.putpixel((x, y), matrix[y][x])
        return image
    
    def save_image(self):
        if self.processed_image:
            try:
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".bmp",
                    filetypes=[("Bitmap files", "*.bmp")]
                )
                if file_path:
                    self.update_status("Saving image...")
                    self.processed_image.save(file_path)
                    self.update_status(f"Image saved: {os.path.basename(file_path)}")
                    messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                self.update_status(f"Error saving image: {str(e)}")
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
    
    def rotate_image(self, angle):
        if not self.processed_matrix:
            return
        
        try:
            self.update_status(f"Rotating image {angle}°...")
            height = len(self.processed_matrix)
            width = len(self.processed_matrix[0])
            
            if angle == 90:
                new_matrix = [[0 for _ in range(height)] for _ in range(width)]
                for y in range(height):
                    for x in range(width):
                        new_matrix[x][height - 1 - y] = self.processed_matrix[y][x]
            elif angle == 180:
                new_matrix = [[0 for _ in range(width)] for _ in range(height)]
                for y in range(height):
                    for x in range(width):
                        new_matrix[height - 1 - y][width - 1 - x] = self.processed_matrix[y][x]
            elif angle == 270:
                new_matrix = [[0 for _ in range(height)] for _ in range(width)]
                for y in range(height):
                    for x in range(width):
                        new_matrix[width - 1 - x][y] = self.processed_matrix[y][x]
            
            self.processed_matrix = new_matrix
            self.processed_image = self.matrix_to_image(self.processed_matrix)
            self.display_images()
            self.update_status(f"Image rotated {angle}°")
        except Exception as e:
            self.update_status(f"Error rotating image: {str(e)}")
            messagebox.showerror("Error", f"Failed to rotate image: {str(e)}")
    
    def flip_horizontal(self):
        if not self.processed_matrix:
            return
        
        try:
            self.update_status("Flipping image horizontally...")
            height = len(self.processed_matrix)
            width = len(self.processed_matrix[0])
            
            new_matrix = [[0 for _ in range(width)] for _ in range(height)]
            for y in range(height):
                for x in range(width):
                    new_matrix[y][width - 1 - x] = self.processed_matrix[y][x]
            
            self.processed_matrix = new_matrix
            self.processed_image = self.matrix_to_image(self.processed_matrix)
            self.display_images()
            self.update_status("Image flipped horizontally")
        except Exception as e:
            self.update_status(f"Error flipping image: {str(e)}")
            messagebox.showerror("Error", f"Failed to flip image: {str(e)}")
    
    def flip_vertical(self):
        if not self.processed_matrix:
            return
        
        try:
            self.update_status("Flipping image vertically...")
            height = len(self.processed_matrix)
            width = len(self.processed_matrix[0])
            
            new_matrix = [[0 for _ in range(width)] for _ in range(height)]
            for y in range(height):
                for x in range(width):
                    new_matrix[height - 1 - y][x] = self.processed_matrix[y][x]
            
            self.processed_matrix = new_matrix
            self.processed_image = self.matrix_to_image(self.processed_matrix)
            self.display_images()
            self.update_status("Image flipped vertically")
        except Exception as e:
            self.update_status(f"Error flipping image: {str(e)}")
            messagebox.showerror("Error", f"Failed to flip image: {str(e)}")
    
    def display_images(self):
        try:
            # Resize images for display
            display_size = (300, 300)
            original_display = self.original_image.resize(display_size, Image.Resampling.LANCZOS)
            processed_display = self.processed_image.resize(display_size, Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            original_photo = ImageTk.PhotoImage(original_display)
            processed_photo = ImageTk.PhotoImage(processed_display)
            
            # Update labels
            self.original_label.config(image=original_photo)
            self.original_label.image = original_photo
            self.processed_label.config(image=processed_photo)
            self.processed_label.image = processed_photo
        except Exception as e:
            self.update_status(f"Error displaying images: {str(e)}")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ImageProcessor()
    app.run()
