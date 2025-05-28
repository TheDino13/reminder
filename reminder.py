import customtkinter as ctk
from tkinter import messagebox
import winsound

class Reminder:
    def __init__(self, main_window):
        self.main = main_window
        self.main.title("Reminder")

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        self.is_reminder_on = False
        self.current_after_id = None
        self.reminder_text = ""
        self.interval_minutes = 0


        self.settings_frame = ctk.CTkFrame(self.main)
        self.settings_frame.pack(pady=10, padx=10, fill="x")

        self.text_label = ctk.CTkLabel(self.settings_frame, text="Text of reminder")
        self.text_label.pack(anchor='w', padx=10, pady=(10, 0))
        self.text_entry = ctk.CTkEntry(self.settings_frame, width=300)
        self.text_entry.pack(pady=(0, 10), padx=10)
        self.text_entry.insert(0, self.reminder_text) 

        self.interval_label = ctk.CTkLabel(self.settings_frame, text="Interval (minutes):")
        self.interval_label.pack(anchor='w', padx=10, pady=(10, 0))
        self.interval_entry = ctk.CTkEntry(self.settings_frame, width=100)
        self.interval_entry.pack(pady=(0, 10), padx=10)
        self.interval_entry.insert(0, str(self.interval_minutes))
        self.interval_entry.bind("<FocusIn>", self.clear_on_focus)
        
        self.button_frame = ctk.CTkFrame(self.main)
        self.button_frame.pack(pady=10, padx=10)

        self.start_button = ctk.CTkButton(self.button_frame, text="Launch reminder", command=self.start_reminder)
        self.start_button.pack(side=ctk.LEFT, padx=5)

        self.stop_button = ctk.CTkButton(self.button_frame, text="Stop reminder", command=self.stop_reminder)
        self.stop_button.pack(side=ctk.LEFT, padx=5)
        self.stop_button.configure(state='disabled')

        self.status_label = ctk.CTkLabel(self.main, text="Reminder wasn't launched.", text_color="white")
        self.status_label.pack(pady=10)

        self.main.protocol("WM_DELETE_WINDOW", self.on_closing)

        
    def clear_on_focus(self, event):
        if self.interval_entry.get() == "0":
            self.interval_entry.delete(0, ctk.END)
    def start_reminder(self):
        if self.is_reminder_on:
            return
        text_from_entry = self.text_entry.get()
        interval_str_from_entry=self.interval_entry.get()
        if not text_from_entry:
            messagebox.showerror("Input error","Enter text please")
            return
        try:
            minutes = int(interval_str_from_entry)
            if minutes <=0:
                messagebox.showerror("Input error","Time has to be positive number")
                return
        except ValueError:
            messagebox.showerror("Error","Invalid Internal")
            return
        
        self.reminder_text = text_from_entry
        self.interval_minutes = minutes
        self.is_reminder_on = True
        #--------------------
        self.start_button.configure(state="Disabled")
        self.stop_button.configure(state="Normal")
        self.status_label.configure(text_color="green", text=f"Reminder launched: '{self.reminder_text}' every {self.interval_minutes} minutes.")
        
        self.schedule_next_reminder()
        
        
    def stop_reminder(self):
        if self.is_reminder_on == False:
            return
        self.is_reminder_on = False
        if self.current_after_id !=None:
            self.main.after_cancel(self.current_after_id)
            self.current_after_id=None
        
        self.start_button.configure(state="Normal")
        self.stop_button.configure(state="Disabled")
        self.status_label.configure(text_color = "red",text="Reminder is stopped")
        
    def schedule_next_reminder(self):
        if self.is_reminder_on == False:
            return
        delay_ms = self.interval_minutes *60*1000
        self.current_after_id = self.main.after(delay_ms,self.trigger_reminder)
        self.status_label.configure(text = f"Next reminder in {self.interval_minutes} minutes.")
    def trigger_reminder(self):
        if self.is_reminder_on == False:
            return
        self.show_notification(self.reminder_text)
        if self.is_reminder_on == True:
            self.schedule_next_reminder()
    def show_notification(self, message):
        notification_window = ctk.CTkToplevel(self.main)
        notification_window.title("Reminder!")
        notification_window.attributes('-topmost', True)


        notification_label = ctk.CTkLabel(notification_window, text=message, font=ctk.CTkFont(size=16, weight="bold"))
        notification_label.pack(padx=20, pady=20)


        ok_button = ctk.CTkButton(notification_window, text="OK", command=notification_window.destroy)
        ok_button.pack(pady=10)
        winsound.PlaySound("SystemDefault", winsound.SND_ALIAS | winsound.SND_ASYNC)
    def on_closing(self):
        if self.is_reminder_on == True:
            self.stop_reminder()
        self.main.destroy()

if __name__ == "__main__":
    root_window = ctk.CTk() 
    app = Reminder(root_window)
    root_window.mainloop()