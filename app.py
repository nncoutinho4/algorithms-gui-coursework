"""Algorithms GUI Application (Tkinter).

Run:
  python app.py
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any, Dict, List

from patterns.creational_factory import CommandFactory
from patterns.structural_facade import AlgorithmsFacade


ALGORITHMS = [
    "RSA Encrypt/Decrypt",
    "Fibonacci (DP)",
    "Selection Sort",
    "Bubble Sort",
    "Merge Sort",
    "Shuffle Deck",
    "Factorial (Recursion)",
    "Array Statistics",
    "Palindrome Substrings (DP)",
]


def parse_int_array(text: str) -> List[int]:
    raw = text.strip()
    if not raw:
        raise ValueError("Array input is empty")
    parts = [p.strip() for p in raw.split(",")]
    return [int(p) for p in parts if p != ""]


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Algorithms Coursework App")
        self.geometry("980x620")

        self.facade = AlgorithmsFacade()
        self.factory = CommandFactory(self.facade)

        self.widgets: Dict[str, Any] = {}
        self.current_algorithm = ""

        self._build_layout()
        self._set_algorithm(ALGORITHMS[0])

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        left = ttk.Frame(self, padding=10)
        left.grid(row=0, column=0, sticky="ns")

        ttk.Label(left, text="Choose Algorithm", font=("Arial", 12, "bold")).pack(anchor="w")
        self.alg_list = tk.Listbox(left, height=16, exportselection=False)
        for name in ALGORITHMS:
            self.alg_list.insert(tk.END, name)
        self.alg_list.pack(fill="y", pady=8)
        self.alg_list.bind("<<ListboxSelect>>", self._on_select)

        right = ttk.Frame(self, padding=10)
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(4, weight=1)

        ttk.Label(right, text="Inputs", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
        self.inputs_frame = ttk.Frame(right)
        self.inputs_frame.grid(row=1, column=0, sticky="ew", pady=6)
        self.inputs_frame.columnconfigure(1, weight=1)

        btns = ttk.Frame(right)
        btns.grid(row=2, column=0, sticky="ew")
        self.run_btn = ttk.Button(btns, text="Run", command=self._run)
        self.run_btn.grid(row=0, column=0, sticky="w")
        self.clear_btn = ttk.Button(btns, text="Clear Output", command=self._clear_output)
        self.clear_btn.grid(row=0, column=1, sticky="w", padx=(8, 0))

        ttk.Label(right, text="Output", font=("Arial", 12, "bold")).grid(row=3, column=0, sticky="w", pady=(12, 0))
        self.output = tk.Text(right, height=16, wrap="word")
        self.output.grid(row=4, column=0, sticky="nsew", pady=(6, 0))

    def _on_select(self, _event: Any) -> None:
        selection = self.alg_list.curselection()
        if not selection:
            return
        idx = selection[0]
        self._set_algorithm(self.alg_list.get(idx))

    def _set_algorithm(self, name: str) -> None:
        self.current_algorithm = name
        for child in self.inputs_frame.winfo_children():
            child.destroy()
        self.widgets.clear()

        row = 0
        if name == "RSA Encrypt/Decrypt":
            self.widgets["mode"] = tk.StringVar(value="encrypt")
            ttk.Label(self.inputs_frame, text="Mode").grid(row=row, column=0, sticky="w")
            mode_box = ttk.Combobox(self.inputs_frame, textvariable=self.widgets["mode"], values=["encrypt", "decrypt"], state="readonly")
            mode_box.grid(row=row, column=1, sticky="ew")
            mode_box.bind("<<ComboboxSelected>>", lambda _e: self._set_algorithm("RSA Encrypt/Decrypt"))
            row += 1

            mode = self.widgets["mode"].get()
            if mode == "encrypt":
                self._add_entry(row, "message", "Message")
                row += 1
                self._add_entry(row, "p", "Optional prime p")
                row += 1
                self._add_entry(row, "q", "Optional prime q")
                row += 1
                self._add_entry(row, "e", "Optional e")
                row += 1
                ttk.Label(self.inputs_frame, text="(Leave p/q/e blank to auto-generate keys)", foreground="#555").grid(row=row, column=1, sticky="w")
                row += 1
            else:
                self._add_entry(row, "ciphertext", "Ciphertext blocks")
                row += 1
                self._add_entry(row, "n", "n")
                row += 1
                self._add_entry(row, "d", "d")
                row += 1
            return

        if name in ("Selection Sort", "Bubble Sort", "Merge Sort", "Array Statistics"):
            self._add_entry(row, "array", "Array (comma-separated)")
            row += 1

        if name in ("Selection Sort", "Bubble Sort", "Merge Sort"):
            self.widgets["ascending"] = tk.StringVar(value="Ascending")
            ttk.Label(self.inputs_frame, text="Order").grid(row=row, column=0, sticky="w")
            order_box = ttk.Combobox(self.inputs_frame, textvariable=self.widgets["ascending"], values=["Ascending", "Descending"], state="readonly")
            order_box.grid(row=row, column=1, sticky="ew")
            row += 1

        if name in ("Fibonacci (DP)", "Factorial (Recursion)"):
            self._add_entry(row, "n", "n")
            row += 1

        if name == "Shuffle Deck":
            self._add_entry(row, "seed", "Optional seed (int)")
            row += 1

        if name == "Palindrome Substrings (DP)":
            self._add_entry(row, "text", "Input string")
            row += 1

    def _add_entry(self, row: int, key: str, label: str) -> None:
        ttk.Label(self.inputs_frame, text=label).grid(row=row, column=0, sticky="w", pady=2)
        ent = ttk.Entry(self.inputs_frame)
        ent.grid(row=row, column=1, sticky="ew", pady=2)
        self.widgets[key] = ent

    def _clear_output(self) -> None:
        self.output.delete("1.0", tk.END)

    def _run(self) -> None:
        try:
            params = self._collect_params()
            cmd = self.factory.create(self.current_algorithm, params)
            result = cmd.execute()
            self.output.insert(tk.END, result + "\n")
            self.output.see(tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _collect_params(self) -> Dict[str, Any]:
        name = self.current_algorithm
        params: Dict[str, Any] = {}

        if name == "RSA Encrypt/Decrypt":
            mode = self.widgets["mode"].get()
            params["mode"] = mode
            if mode == "encrypt":
                params["message"] = self.widgets["message"].get()
                params["p"] = self.widgets["p"].get()
                params["q"] = self.widgets["q"].get()
                params["e"] = self.widgets["e"].get()
            else:
                params["ciphertext"] = self.widgets["ciphertext"].get()
                params["n"] = self.widgets["n"].get()
                params["d"] = self.widgets["d"].get()
            return params

        if name in ("Selection Sort", "Bubble Sort", "Merge Sort", "Array Statistics"):
            params["array"] = parse_int_array(self.widgets["array"].get())

        if name in ("Selection Sort", "Bubble Sort", "Merge Sort"):
            order = self.widgets["ascending"].get()
            params["ascending"] = (order == "Ascending")

        if name in ("Fibonacci (DP)", "Factorial (Recursion)"):
            params["n"] = int(self.widgets["n"].get())

        if name == "Shuffle Deck":
            seed_text = self.widgets["seed"].get().strip()
            params["seed"] = int(seed_text) if seed_text else None

        if name == "Palindrome Substrings (DP)":
            params["text"] = self.widgets["text"].get()

        return params


def main() -> None:
    app = App()
    app.alg_list.selection_set(0)
    app.mainloop()


if __name__ == "__main__":
    main()
