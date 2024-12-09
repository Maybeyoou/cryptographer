import os
from tkinter import Tk, filedialog, messagebox, Button, Label, Frame
from cryptography.fernet import Fernet

# Функция для генерации ключа и сохранения его в файл
def generate_key():
    key = Fernet.generate_key()
    key_file = filedialog.asksaveasfilename(
        title="Сохранить ключ как...",
        defaultextension=".key",
        filetypes=[("Key Files", "*.key")]
    )
    if key_file:
        with open(key_file, "wb") as file:
            file.write(key)
        messagebox.showinfo("Готово", f"Ключ сохранён: {key_file}")

# Функция для загрузки ключа из файла
def load_key():
    key_file = filedialog.askopenfilename(
        title="Выберите ключевой файл",
        filetypes=[("Key Files", "*.key")]
    )
    if key_file:
        with open(key_file, "rb") as file:
            return file.read()
    else:
        messagebox.showwarning("Ошибка", "Ключевой файл не выбран.")
        return None

# Функция для шифрования файла
def encrypt_file():
    key = load_key()
    if not key:
        return
    file_path = filedialog.askopenfilename(
        title="Выберите файл для шифрования"
    )
    if not file_path:
        messagebox.showwarning("Ошибка", "Файл не выбран.")
        return

    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        data = file.read()

    encrypted_data = fernet.encrypt(data)
    encrypted_file = file_path + ".encrypted"
    with open(encrypted_file, "wb") as file:
        file.write(encrypted_data)
    messagebox.showinfo("Готово", f"Файл зашифрован: {encrypted_file}")

# Функция для расшифровки файла
def decrypt_file():
    key = load_key()
    if not key:
        return
    file_path = filedialog.askopenfilename(
        title="Выберите файл для расшифровки",
        filetypes=[("Encrypted Files", "*.encrypted")]
    )
    if not file_path:
        messagebox.showwarning("Ошибка", "Файл не выбран.")
        return

    fernet = Fernet(key)
    try:
        with open(file_path, "rb") as file:
            encrypted_data = file.read()

        decrypted_data = fernet.decrypt(encrypted_data)
        decrypted_file = file_path.replace(".encrypted", "")
        with open(decrypted_file, "wb") as file:
            file.write(decrypted_data)
        messagebox.showinfo("Готово", f"Файл расшифрован: {decrypted_file}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось расшифровать файл: {e}")

# Основное окно
def main():
    root = Tk()
    root.title("Шифрование и расшифровка файлов")
    root.geometry("400x300")
    root.minsize(300, 250)

    # Основной фрейм для динамического размещения
    frame = Frame(root)
    frame.pack(expand=True, fill="both", padx=10, pady=10)

    Label(frame, text="Выберите действие", font=("Arial", 14)).pack(pady=10, anchor="center")

    Button(frame, text="Сгенерировать ключ", command=generate_key, width=30).pack(pady=5, anchor="center")
    Button(frame, text="Зашифровать файл", command=encrypt_file, width=30).pack(pady=5, anchor="center")
    Button(frame, text="Расшифровать файл", command=decrypt_file, width=30).pack(pady=5, anchor="center")

    Button(frame, text="Выход", command=root.quit, width=30).pack(pady=20, anchor="center")

    # Динамическое изменение размера окна
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    root.mainloop()

if __name__ == "__main__":
    main()
