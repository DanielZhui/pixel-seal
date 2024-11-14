# 📸 Pixel Seal - Image Watermarking Service 🖋️

![Python](https://img.shields.io/badge/Python-3.9-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.85.0-009688.svg)
![License](https://img.shields.io/github/license/DanielZhui/pixel-seal)

Welcome to **Pixel Seal**, a user-friendly web application designed to help you effortlessly add customizable watermarks to your images. Enhance your photos with stylish watermarks and protect your visual content with ease! 🌟

## 🚀 Features

- **Easy Image Upload**: Seamlessly upload images in various formats.
- **Customizable Watermarks**: Personalize your watermark text, font style, size, color, opacity, density, rotation, and margin.
- **Real-time Preview**: Instantly preview the watermarked image before downloading.
- **Download Options**: Easily download your watermarked images in high quality.
- **Responsive Design**: Optimized for both desktop and mobile devices. 📱💻
- **User Information Modal**: Click the user icon in the header to view personal information.
- **GitHub Integration**: Access the project repository directly from the footer. 🐱‍💻
- **Secure Uploads**: Enforces file size limits and validates image formats.
- **Temporary File Cleanup**: Automatically cleans up temporary files to save storage space.

## 🎨 Screenshots

![Upload Page](https://github.com/yourusername/pixel-seal/raw/main/screenshots/upload.png)
*Upload your image and configure watermark settings.*

![Preview Page](https://github.com/yourusername/pixel-seal/raw/main/screenshots/preview.png)
*Preview and download your watermarked image.*

## 🛠️ Installation

### 🔧 Prerequisites

- **Python 3.9+**: Ensure you have Python installed. [Download Python](https://www.python.org/downloads/)
- **Git**: To clone the repository. [Download Git](https://git-scm.com/downloads)

### 📥 Clone the Repository

```bash
git clone https://github.com/DanielZhui/pixel-seal.git
cd pixel-seal
```

### 🐍 Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 📦 Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 🔄 Run the Application

```bash
uvicorn app.main:app --reload
```

The application will be accessible at `http://localhost:8000`.

## 🖥️ Usage

1. **Upload Image**: Navigate to the upload page and select an image from your device.
2. **Configure Watermark**: Enter your desired watermark text and adjust the settings (font, size, color, opacity, etc.).
3. **Add Watermark**: Click the "Add Watermark" button to process your image.
4. **Preview and Download**: After processing, preview the watermarked image and download it or view it in full size.
5. **View Personal Information**: Click the user icon in the header to view personal details.
6. **Visit GitHub Repository**: Click the GitHub icon in the footer to visit the project's repository.

## 🖥️ Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/) - A modern, fast web framework for building APIs with Python 3.7+.
- [Jinja2](https://jinja.palletsprojects.com/) - A full-featured template engine for Python.
- [Pillow](https://python-pillow.org/) - Python Imaging Library (PIL) fork for image processing.
- [Uvicorn](https://www.uvicorn.org/) - A lightning-fast ASGI server implementation, using uvloop and httptools.
- [Font Awesome](https://fontawesome.com/) - Icon library for web projects.

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. 🤗 Please feel free to submit issues and pull requests.

### 📝 Steps to Contribute

1. **Fork the Project**: Click the 🔼 button on the top right to fork the repository.
2. **Clone Your Fork**:

    ```bash
    git clone https://github.com/yourusername/pixel-seal.git
    cd pixel-seal
    ```

3. **Create a Branch**:

    ```bash
    git checkout -b feature/YourFeatureName
    ```

4. **Commit Your Changes**:

    ```bash
    git commit -m "Add some feature"
    ```

5. **Push to the Branch**:

    ```bash
    git push origin feature/YourFeatureName
    ```

6. **Open a Pull Request**: Navigate to the repository on GitHub and click the "Compare & pull request" button.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information. 📜

## 📫 Contact

- **Project Link**: [https://github.com/yourusername/pixel-seal](https://github.com/DanielZhui/pixel-seal)

## 🧰 Tools

- [Visual Studio Code](https://code.visualstudio.com/) - Code editor.
- [Docker](https://www.docker.com/) - For containerization.

---

Made with ❤️ by [Wollens](https://github.com/DanielZhui)
