import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from types import SimpleNamespace

from ptypy.cli.command_line_interface import run as cli_run


class PtyPyGUI(tk.Tk):
    """Simple GUI wrapper around :mod:`ptypy.cli.command_line_interface`."""

    def __init__(self):
        super().__init__()
        self.title("PtyPy GUI")
        self.geometry("400x220")
        self._create_widgets()

    def _create_widgets(self):
        tk.Label(self, text="Config file:").grid(row=0, column=0, sticky="e", pady=5, padx=5)
        self.file_entry = tk.Entry(self, width=30)
        self.file_entry.grid(row=0, column=1, pady=5)
        tk.Button(self, text="Browse", command=self._browse_file).grid(row=0, column=2, padx=5)

        tk.Label(self, text="Output folder:").grid(row=1, column=0, sticky="e", pady=5, padx=5)
        self.output_entry = tk.Entry(self, width=30)
        self.output_entry.grid(row=1, column=1, pady=5)
        tk.Button(self, text="Browse", command=self._browse_folder).grid(row=1, column=2, padx=5)

        tk.Label(self, text="PtyPy level:").grid(row=2, column=0, sticky="e", pady=5, padx=5)
        self.level_var = tk.StringVar(value="5")
        tk.Entry(self, textvariable=self.level_var, width=5).grid(row=2, column=1, sticky="w")

        tk.Label(self, text="Identifier:").grid(row=3, column=0, sticky="e", pady=5, padx=5)
        self.id_entry = tk.Entry(self, width=30)
        self.id_entry.grid(row=3, column=1, pady=5)

        self.plot_var = tk.IntVar(value=0)
        tk.Checkbutton(self, text="Plot", variable=self.plot_var).grid(row=4, column=1, sticky="w", pady=5)

        tk.Button(self, text="Run", command=self._run).grid(row=5, column=1, pady=10)

    def _browse_file(self):
        path = filedialog.askopenfilename(filetypes=[("Config", "*.json *.yaml *.yml")])
        if path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, path)

    def _browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, path)

    def _run(self):
        config = self.file_entry.get().strip()
        if not config:
            messagebox.showerror("Error", "Please select a configuration file")
            return
        args = SimpleNamespace(
            file=config,
            output_folder=self.output_entry.get().strip() or None,
            ptypy_level=int(self.level_var.get() or 5),
            identifier=self.id_entry.get().strip() or None,
            plot=bool(self.plot_var.get()),
            ptyscan_modules=None,
            backends=None,
            json=None,
        )
        threading.Thread(target=self._run_cli, args=(args,), daemon=True).start()
        messagebox.showinfo("Running", "PtyPy run started. Check console for output.")

    @staticmethod
    def _run_cli(args):
        cli_run(args)


def main():
    app = PtyPyGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
