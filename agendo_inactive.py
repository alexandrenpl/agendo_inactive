import pandas as pd
from datetime import datetime, timedelta
from tkinter import Tk, filedialog, simpledialog, messagebox
import tkinter as tk
import os
# ============================
# Dados embutidos (versao 1)
# ============================

DEFAULT_RESOURCE_FILTERS = [
    "[Lisbon] 3i Marianas SDC", "[Lisbon] IVIS Lumina", "[Lisbon] Leica DM2500",
    "[Lisbon] Leica SP8 MP", "[Lisbon] Nikon Eclipse Ti", "[Lisbon] Visitech VT-iSIM",
    "[Lisbon] ZEISS Axio Zoom.V16", "[Lisbon] ZEISS Axioscan 7", "[Lisbon] ZEISS Axiovert 200M",
    "[Lisbon] ZEISS Cell Observer", "[Lisbon] ZEISS Cell Observer SD", 
    "[Lisbon] ZEISS Celldiscoverer 7 with LSM 900", "[Lisbon] ZEISS Lightsheet Z.1",
    "[Lisbon] ZEISS LSM 880 with Airyscan", "[Lisbon] ZEISS LSM 980 with Airyscan 2",
    "[Lisbon] ZEISS LSM 980-32 Processing PC", "[Lisbon] ZEISS LSM 980-32 with Airyscan 2",
    "[Oeiras] 3i Marianas SDC", "[Oeiras] 3i Marianas SDC II + TIRF (BSL2)",
    "[Oeiras] Agilent Cytation 5", "[Oeiras] Amira Workstation", "[Oeiras] Andor Dragonfly SDC",
    "[Oeiras] Andor Spinning Disk W1", "[Oeiras] Deltavision OMX-SIM",
    "[Oeiras] Leica Spinning Disk Confocal", "[Oeiras] Miltenyi UltraMicroscope Blaze",
    "[Oeiras] Nikon HTM-HCS", "[Oeiras] Prairie Multiphoton",
    "[Oeiras] ZEISS Axio Imager with Apotome 2", "[Oeiras] ZEISS Lightsheet Z.1",
    "[Oeiras] ZEISS LSM 900 with Airyscan 2", "[Oeiras] ZEISS LSM 980 with Airyscan 2",
    "[Oeiras] ZEISS Stereo Lumar.V12"
]

DEFAULT_NAMES_TO_EXCLUDE = [
    ("Aida", "Lima"), ("Alexandre", "Lopes"), ("Ana", "Nascimento"), ("António", "Temudo"),
    ("Beatriz", "Barbosa"), ("Diogo", "Coutinho"), ("Gabriel ", "Martins"), ("José", "Rino"),
    ("Manuel", "Tanqueiro"), ("Patrícia", "Rodrigues"), ("Paulo", "Almeida")
]

resource_filters = DEFAULT_RESOURCE_FILTERS.copy()
names_to_exclude = DEFAULT_NAMES_TO_EXCLUDE.copy()

# ============================
# Função principal
# ============================

def analisar_inactivos(file_path, months, recursos):
    df = pd.read_csv(file_path)
    df["last_activity"] = pd.to_datetime(df["last_activity"], errors='coerce')
    cutoff_date = datetime.now() - timedelta(days=months * 30)

    resultados = {}

    for recurso in recursos:
        filtro = df[(df["resource_name"] == recurso) &
                    (df["last_activity"].isna() | (df["last_activity"] < cutoff_date))]

        inactivos = filtro[["first_name", "last_name", "username", "last_activity"]].drop_duplicates()
        inactivos = inactivos[~inactivos[["first_name", "last_name"]].apply(tuple, axis=1).isin(names_to_exclude)]

        if not inactivos.empty:
            inactivos = inactivos.sort_values(by="last_activity", ascending=False)
            texto = f"Inactive users for '{recurso}' (>{months} months):\n"
            for _, row in inactivos.iterrows():
                nome = f"{row['first_name']} {row['last_name']} {row['username']}"
                ultima = row['last_activity']
                ultima_txt = "Never used" if pd.isna(ultima) else ultima.strftime("%Y-%m-%d")
                if pd.isna(ultima):
                    texto += f" - {nome} [NEVER USED]\n"
                else:
                    texto += f" - {nome} (last used: {ultima_txt})\n"
            texto += f"Total: {len(inactivos)} user(s)\n"
        else:
            texto = f"No inactive users for '{recurso}'.\n"

        resultados[recurso] = texto

    return resultados

# ============================
# Interface Tkinter
# ============================


def abrir_interface():
    global var_recursos, scroll_frame
    def selecionar_ficheiro():
        caminho = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if caminho:
            entry_ficheiro.delete(0, tk.END)
            entry_ficheiro.insert(0, caminho)

    def editar_lista(lista_original, titulo, tipo):
        popup = tk.Toplevel(root)
        popup.title(titulo)
        txt = tk.Text(popup, width=80, height=20)
        txt.pack(padx=10, pady=10)
        for item in lista_original:
            txt.insert(tk.END, ",".join(item) if isinstance(item, tuple) else item)
            txt.insert(tk.END, "\n")

        def guardar():
            linhas = txt.get("1.0", tk.END).strip().split("\n")
            if tipo == "equip":
                global resource_filters, var_recursos
                resource_filters = [l.strip() for l in linhas if l.strip()]
                # Limpar e atualizar os checkboxes
                for widget in scroll_frame.winfo_children():
                    widget.destroy()
                var_recursos.clear()
                for r in resource_filters:
                    var = tk.BooleanVar(value=True)
                    tk.Checkbutton(scroll_frame, text=r, variable=var).pack(anchor="w")
                    var_recursos.append(var)
            elif tipo == "excluir":
                global names_to_exclude
                names_to_exclude = []
                for linha in linhas:
                    partes = linha.strip().split(",", 1)
                    if len(partes) == 2:
                        names_to_exclude.append((partes[0], partes[1]))
            popup.destroy()

        tk.Button(popup, text="Guardar", command=guardar).pack(pady=5)

    def correr():
        caminho = entry_ficheiro.get()
        try:
            meses = int(entry_meses.get())
        except:
            messagebox.showerror("Erro", "Meses inválidos")
            return
        recursos = [r for i, r in enumerate(resource_filters) if var_recursos[i].get()]
        if not os.path.isfile(caminho):
            messagebox.showerror("Erro", "Ficheiro inválido")
            return
        if not recursos:
            messagebox.showwarning("Aviso", "Nenhum sistema selecionado")
            return
        try:
            resultado = analisar_inactivos(caminho, meses, recursos)
            txt_resultado.delete("1.0", tk.END)
            txt_resultado.insert(tk.END, "\n\n".join(resultado[r] for r in recursos))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    root = tk.Tk()
    root.title("Inactive Users Checker")

    tk.Label(root, text="Ficheiro CSV:").grid(row=0, column=0, sticky="w")
    entry_ficheiro = tk.Entry(root, width=60)
    entry_ficheiro.grid(row=0, column=1)
    tk.Button(root, text="Selecionar", command=selecionar_ficheiro).grid(row=0, column=2)

    tk.Label(root, text="Meses de inactividade:").grid(row=1, column=0, sticky="w")
    entry_meses = tk.Entry(root, width=5)
    entry_meses.insert(0, "6")
    entry_meses.grid(row=1, column=1, sticky="w")

    tk.Button(root, text="Editar Equipamentos", command=lambda: editar_lista(resource_filters, "Editar Equipamentos", "equip")).grid(row=2, column=0)
    tk.Button(root, text="Editar Lista Exclusão", command=lambda: editar_lista(names_to_exclude, "Editar Exclusão", "excluir")).grid(row=2, column=1)

    tk.Label(root, text="Selecionar Sistemas:").grid(row=3, column=0, sticky="w")
    frame_scroll = tk.Frame(root)
    frame_scroll.grid(row=4, column=0, columnspan=3)
    canvas = tk.Canvas(frame_scroll)
    scrollbar = tk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set, width=700, height=200)

    canvas.pack(side="left")
    scrollbar.pack(side="right", fill="y")

    var_recursos = []
    for r in resource_filters:
        var = tk.BooleanVar(value=True)
        tk.Checkbutton(scroll_frame, text=r, variable=var).pack(anchor="w")
        var_recursos.append(var)

    tk.Button(root, text="Analisar", command=correr).grid(row=5, column=0, pady=10)
    txt_resultado = tk.Text(root, width=90, height=15)
    txt_resultado.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

    root.mainloop()

abrir_interface()
