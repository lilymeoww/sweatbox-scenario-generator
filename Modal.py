import customtkinter

class Modal:
    def __init__(self,parent,text,type_=0):
        self.parent = parent
        self.text = text
        self.type_ = "Error" if not type_ else type_
        self.titleColor = "red" if not type_ else "green"
        self.create_modal()

    def create_modal(self):
        modal = customtkinter.CTkToplevel(self.parent)
        modal.title(self.type_)
        self.parent.update_idletasks()
        modal_width = 400
        modal_height = 200
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        x = (screen_width // 2) - (modal_width // 2)
        y = (screen_height // 2) - (modal_height // 2)
        modal.attributes("-topmost", True)
        modal.geometry(f"{modal_width}x{modal_height}+{x}+{y}")

        customtkinter.CTkLabel(modal, text=self.type_.upper(), font=("Arial", 16, "bold"), text_color=self.titleColor).grid(row=0, column=0, pady=10, padx=20, sticky="nsew")
        customtkinter.CTkLabel(modal, text=self.text).grid(row=1, column=0, pady=20, padx=20, sticky="nsew")
        customtkinter.CTkButton(modal, text="Close", command=lambda: modal.destroy()).grid(row=2, column=0, pady=20, padx=20, sticky="nsew")
        
        modal.grid_rowconfigure(0, weight=1)
        modal.grid_rowconfigure(3, weight=1)
        modal.grid_columnconfigure(0, weight=1)
