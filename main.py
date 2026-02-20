import customtkinter as ctk
from PIL import Image
import hashlib, os, zlib, random
from datetime import datetime, timedelta
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from tkinter import filedialog, messagebox

class LeviathanEngine:
    def __init__(self, password):
        self.key = hashlib.sha256(password.encode()).digest()
        self.marker = hashlib.sha256(("APEX" + password).encode()).digest()[:16]
        
    def crypt(self, data, encrypt=True):
        cipher = AES.new(self.key, AES.MODE_CBC, b'\x00' * 16)
        if encrypt:
            return cipher.encrypt(pad(zlib.compress(data), 16))
        else:
            try:
                decrypted = unpad(cipher.decrypt(data), 16)
                return zlib.decompress(decrypted)
            except Exception as e:
                raise ValueError(f"Dekripcija nije uspela: {str(e)}")

    @staticmethod
    def generate_iphone_exif():
        """Generiše autentične iPhone 15 Pro metapodatke"""
        date_now = datetime.now() - timedelta(days=random.randint(1, 30))
        fmt_date = date_now.strftime("%Y:%m:%d %H:%M:%S")
        return {
            271: "Apple",                             # Make
            272: "iPhone 15 Pro",                    # Model
            305: "iOS 17.5.1",                       # Software
            306: fmt_date,                           # DateTime
            36867: fmt_date,                         # DateTimeOriginal
            37510: "Processed with Deep Fusion",      # UserComment
            42036: "iPhone 15 Pro back triple camera" # LensModel
        }

class SteganoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LEVIATHAN v21.0 - GHOST METADATA")
        self.geometry("1200x900")
        ctk.set_appearance_mode("dark")
        
        self.carrier_path = ""
        self.true_payload = None
        self.true_name = ""
        self.fake_payload = None
        self.fake_name = ""
        
        self.build_interface()

    def build_interface(self):
        self.sidebar = ctk.CTkFrame(self, width=350, fg_color="#050505", corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.sidebar, text="VAULT STATUS: ONLINE", font=("System", 10), text_color="#00ff41").pack(pady=(20,0))
        ctk.CTkLabel(self.sidebar, text="DUO-VAULT", font=("Impact", 45), text_color="#00ff41").pack(pady=(0,20))
        
        ctk.CTkLabel(self.sidebar, text="--- PRIMARY SECRET (TRUE) ---", text_color="cyan", font=("System", 12, "bold")).pack(pady=5)
        ctk.CTkButton(self.sidebar, text="SELECT TRUE PAYLOAD", command=self.load_true, fg_color="#1a1a1a").pack(pady=5, padx=20)
        self.pass_true = ctk.CTkEntry(self.sidebar, show="*", placeholder_text="ACCESS KEY / TRUE PASSWORD", height=45, border_color="cyan")
        self.pass_true.pack(pady=10, padx=20)

        self.duo_var = ctk.BooleanVar(value=False)
        self.duo_switch = ctk.CTkSwitch(self.sidebar, text="ENABLE DOUBLE BOTTOM", variable=self.duo_var, command=self.toggle_duo, progress_color="orange")
        self.duo_switch.pack(pady=20)

        self.fake_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        ctk.CTkLabel(self.fake_frame, text="--- DECOY DATA (FAKE) ---", text_color="orange", font=("System", 12, "bold")).pack(pady=5)
        ctk.CTkButton(self.fake_frame, text="SELECT FAKE PAYLOAD", command=self.load_fake, fg_color="#1a1a1a").pack(pady=5, padx=20)
        self.pass_fake = ctk.CTkEntry(self.fake_frame, show="*", placeholder_text="DECOY PASSWORD", height=45, border_color="orange")
        self.pass_fake.pack(pady=10, padx=20)

        ctk.CTkButton(self.sidebar, text="LOAD CARRIER IMAGE", command=self.load_carrier, fg_color="#333", height=40).pack(pady=(30,10), padx=20)
        ctk.CTkButton(self.sidebar, text="EXECUTE INJECTION", fg_color="#1b5e20", hover_color="#2e7d32", height=60, font=("System", 18, "bold"), command=self.run_injection).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="EXTRACT DATA", fg_color="#0d47a1", hover_color="#1565c0", height=50, command=self.run_extraction).pack(pady=5, padx=20)

        self.main_view = ctk.CTkFrame(self, fg_color="#0a0a0a")
        self.main_view.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.terminal = ctk.CTkTextbox(self.main_view, height=250, fg_color="black", text_color="#00ff41", font=("Consolas", 13), border_width=1, border_color="#1a1a1a")
        self.terminal.pack(side="bottom", fill="x", padx=15, pady=15)
        self.preview = ctk.CTkLabel(self.main_view, text="[ STANDBY ]", text_color="#333", font=("System", 14))
        self.preview.pack(expand=True)

    def toggle_duo(self):
        if self.duo_var.get(): self.fake_frame.pack(fill="x")
        else: self.fake_frame.pack_forget()

    def log(self, msg):
        self.terminal.insert("end", f">>> {msg}\n"); self.terminal.see("end")

    def load_carrier(self):
        path = filedialog.askopenfilename()
        if path:
            self.carrier_path = path
            img = Image.open(path); img.thumbnail((500,500))
            self.preview.configure(image=ctk.CTkImage(img, size=(img.width, img.height)), text="")
            self.log(f"Carrier Loaded: {os.path.basename(path)}")

    def load_true(self):
        path = filedialog.askopenfilename()
        if path:
            with open(path, "rb") as f: self.true_payload = f.read()
            self.true_name = os.path.basename(path)
            self.log(f"Primary Payload: {self.true_name}")

    def load_fake(self):
        path = filedialog.askopenfilename()
        if path:
            with open(path, "rb") as f: self.fake_payload = f.read()
            self.fake_name = os.path.basename(path)
            self.log(f"Decoy Payload: {self.fake_name}")

    def run_injection(self):
        true_pwd = self.pass_true.get()
        if not self.carrier_path or not true_pwd or not self.true_payload:
            messagebox.showerror("Error", "Missing Data!")
            return
        
        try:
            self.log("Applying iPhone Camouflage & Ghost Protocol...")
            
            # 1. Kreiranje privremene slike sa iPhone EXIF podacima
            img = Image.open(self.carrier_path)
            exif_data = img.getexif()
            iphone_tags = LeviathanEngine.generate_iphone_exif()
            for tag, val in iphone_tags.items():
                exif_data[tag] = val
            
            temp_camo = "temp_camo.png"
            img.save(temp_camo, exif=exif_data)
            
            with open(temp_camo, 'rb') as f:
                final_bin = f.read()
            
            os.remove(temp_camo) # Brišemo temp odmah nakon čitanja
            
            # 2. Maskiranje kraja fajla (ICC Profile mimicry)
            final_bin += b"\x00\x00\x04\x30Lino\x02\x10\x00\x00mntrRGB XYZ "

            # 3. Decoy Layer
            if self.duo_var.get() and self.fake_payload and self.pass_fake.get():
                self.log("Adding Decoy Layer...")
                fake_engine = LeviathanEngine(self.pass_fake.get())
                fake_data = f"{self.fake_name}|".encode() + self.fake_payload
                encrypted = fake_engine.crypt(fake_data)
                final_bin += fake_engine.marker + len(encrypted).to_bytes(8, 'big') + encrypted
            
            # 4. True Layer
            self.log("Adding Primary Secret Layer...")
            true_engine = LeviathanEngine(true_pwd)
            true_data = f"{self.true_name}|".encode() + self.true_payload
            encrypted_true = true_engine.crypt(true_data)
            final_bin += true_engine.marker + len(encrypted_true).to_bytes(8, 'big') + encrypted_true
            
            save_path = filedialog.asksaveasfilename(defaultextension=".png")
            if save_path:
                with open(save_path, 'wb') as f: f.write(final_bin)
                self.log("MISSION ACCOMPLISHED: File is iPhone-camouflaged and secured.")
            
            self.pass_true.delete(0, 'end'); self.pass_fake.delete(0, 'end')
        except Exception as e:
            self.log(f"FAILURE: {e}")

    def run_extraction(self):
        pwd = self.pass_true.get()
        path = filedialog.askopenfilename()
        if not path or not pwd: return
        
        try:
            self.log("Omni-Scanning for matching layers...")
            engine = LeviathanEngine(pwd)
            with open(path, 'rb') as f: data = f.read()
            
            marker = engine.marker
            start_search = 0
            found = False

            while True:
                idx = data.find(marker, start_search)
                if idx == -1: break
                
                try:
                    len_start = idx + len(marker)
                    data_len = int.from_bytes(data[len_start : len_start + 8], 'big')
                    encrypted_zone = data[len_start + 8 : len_start + 8 + data_len]
                    
                    decrypted = engine.crypt(encrypted_zone, encrypt=False)
                    if b"|" in decrypted:
                        name_b, content = decrypted.split(b"|", 1)
                        name = name_b.decode('utf-8', errors='ignore')
                        
                        save_p = filedialog.asksaveasfilename(initialfile=name)
                        if save_p:
                            with open(save_p, 'wb') as f: f.write(content)
                            self.log(f"SUCCESS: Layer '{name}' extracted.")
                        found = True
                        break 
                except:
                    start_search = idx + 1
                    continue
            
            if not found: self.log("ACCESS DENIED: No layers match this key.")
            self.pass_true.delete(0, 'end')
        except Exception as e:
            self.log(f"SCAN ERROR: {str(e)}")

if __name__ == "__main__":
    app = SteganoApp()
    app.mainloop()
