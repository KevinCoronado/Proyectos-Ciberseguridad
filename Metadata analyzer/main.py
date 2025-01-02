from metadata_analyzer import extract_metadata
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import *


def browse_file():
    """Abre una ventana para seleccionar un archivo."""
    file_path = filedialog.askopenfilename(
        title="Seleccione un archivo",
        filetypes=[("Todos los archivos", "*.*")],
    )
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)


def process_file():
    """Procesa el archivo seleccionado y muestra su metadata en el cuadro de texto."""
    file_path = input_entry.get()  # Obtiene la ruta del archivo del cuadro de entrada
    if file_path:
        try:
            metadata = extract_metadata(file_path)
            #Limpia el cuadro de texto y muestra la metadata
            result_text.delete(1.0, tk.END)
            for key, value in metadata.items():
                result_text.insert(tk.END, f"{key}: {value}\n")
            result_label.config(text="¡Archivo procesado correctamente!")
        except Exception as e:
            result_label.config(text=f"Error al procesar: {e}")
    else:
        result_label.config(text="Por favor, seleccione un archivo primero.")


if __name__ == '__main__':
    #Titulo
    root = tk.Tk()
    root.title('Metadata Analyzer (PDF, JPEG, JPG, PNG, DOCX)')

    #Etiqueta de selección
    label = tk.Label(root, text="Seleccione un archivo:")
    label.grid(row=0, column=0, padx=10, pady=10)

    #Input
    input_entry = tk.Entry(root, width=50)
    input_entry.grid(row=0, column=1, padx=10, pady=10)

    #Boton seleccionar archivo
    browse_button = tk.Button(root, text="Seleccionar archivo", command=browse_file)
    browse_button.grid(row=0, column=2, padx=10, pady=10)

    #Boton
    process_button = tk.Button(root, text="Procesar archivo", command=process_file)
    process_button.grid(row=1, column=1, pady=10)

    #Etiqueta
    result_label = tk.Label(root, text="", fg="black")
    result_label.grid(row=2, column=0, columnspan=3, pady=10)

    #Resultados
    result_text = tk.Text(root, width=80, height=20, wrap=tk.WORD)
    result_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    #Iniciar el bucle de eventos
    root.mainloop()
