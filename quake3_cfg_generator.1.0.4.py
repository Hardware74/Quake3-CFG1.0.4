# quake3_cfg_generator.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from datetime import datetime


class Quake3ConfigGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Quake 3 CFG Generator")
        self.root.geometry("700x900")
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initialize all tabs
        self.create_server_identity_tab()
        self.create_game_settings_tab()
        self.create_player_settings_tab()
        self.create_server_technical_tab()
        self.create_map_rotation_tab()
        self.create_voting_tab()
        self.create_custom_cvars_tab()
        
        # Generate button
        self.generate_btn = ttk.Button(root, text="Generate & Save CFG File", command=self.generate_config)
        self.generate_btn.pack(pady=10, ipadx=10, ipady=5)
    
    def create_server_identity_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Server Identity")
        
        ttk.Label(frame, text="Server Name:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        self.sv_hostname = ttk.Entry(frame, width=40)
        self.sv_hostname.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(frame, text="RCON Password:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        self.rconpassword = ttk.Entry(frame, width=40, show="*")
        self.rconpassword.grid(row=1, column=1, padx=10, pady=10)
        
        # Category 1: Password Protect checkbox
        self.g_needpass = tk.BooleanVar(value=False)
        ttk.Checkbutton(frame, text="Password Protect", variable=self.g_needpass).grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        
        # Category 1: Game Password (changed from Admin Password)
        ttk.Label(frame, text="Game Password:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
        self.g_password = ttk.Entry(frame, width=40, show="*")
        self.g_password.grid(row=3, column=1, padx=10, pady=10)
    
    def create_game_settings_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Game Settings")
        
        ttk.Label(frame, text="Game Type:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        self.g_gametype = ttk.Combobox(frame, values=["0 (FFA)", "1 (Tournament 1v1)", "2 (Team Arena FFA)", "3 (TDM)", "4 (CTF)", "5 (Team Arena OneFlagCTF)", "6 (Team Arena Overload)", "7 (Team Arena Harvester)"], width=37)
        self.g_gametype.grid(row=0, column=1, padx=10, pady=10)
        self.g_gametype.set("0 (FFA)")
        self.g_gametype.bind("<<ComboboxSelected>>", self.on_gametype_changed)
        
        ttk.Label(frame, text="Fraglimit:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        self.fraglimit_label = ttk.Label(frame, text="Fraglimit:", font=("Arial", 10, "bold"))
        self.fraglimit_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        self.fraglimit = ttk.Entry(frame, width=40)
        self.fraglimit.insert(0, "20")
        self.fraglimit.grid(row=1, column=1, padx=10, pady=10)
        self.fraglimit_frame = frame
        self.fraglimit_row = 1
        
        ttk.Label(frame, text="Timelimit (minutes):", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        self.timelimit = ttk.Entry(frame, width=40)
        self.timelimit.insert(0, "15")
        self.timelimit.grid(row=2, column=1, padx=10, pady=10)
        
        # Captures to win (CTF only) - initially hidden
        ttk.Label(frame, text="Captures to Win:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
        self.capturelimit = ttk.Entry(frame, width=40)
        self.capturelimit.insert(0, "0")
        self.capturelimit.grid(row=3, column=1, padx=10, pady=10)
        self.capturelimit_label = ttk.Label(frame, text="Captures to Win:", font=("Arial", 10, "bold"))
        self.capturelimit_label.grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
        self.capturelimit.grid(row=3, column=1, padx=10, pady=10)
        self.hide_ctf_options()
        
        # Category 2: Pure Server option
        ttk.Label(frame, text="Pure Server:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky=tk.W, padx=10, pady=10)
        self.sv_pure = ttk.Combobox(frame, values=["0", "1"], width=37)
        self.sv_pure.set("0")
        self.sv_pure.grid(row=4, column=1, padx=10, pady=10)
        
        # Category 2: Allow Client Downloads option
        ttk.Label(frame, text="Allow Client Downloads from Server:", font=("Arial", 10, "bold")).grid(row=5, column=0, sticky=tk.W, padx=10, pady=10)
        self.sv_allowdownloads = ttk.Combobox(frame, values=["0", "1"], width=37)
        self.sv_allowdownloads.set("0")
        self.sv_allowdownloads.grid(row=5, column=1, padx=10, pady=10)
    
    def on_gametype_changed(self, event=None):
        """Handle game type change to show/hide CTF-specific options"""
        gametype = self.g_gametype.get().split()[0]
        
        if gametype == "4":  # CTF
            self.show_ctf_options()
        else:
            self.hide_ctf_options()
    
    def show_ctf_options(self):
        """Show Captures to Win option and hide Fraglimit"""
        self.fraglimit.grid_remove()
        self.fraglimit_label.grid_remove()
        self.capturelimit_label.grid()
        self.capturelimit.grid()
    
    def hide_ctf_options(self):
        """Hide Captures to Win option and show Fraglimit"""
        self.fraglimit.grid()
        self.fraglimit_label.grid()
        self.capturelimit_label.grid_remove()
        self.capturelimit.grid_remove()
    
    def create_player_settings_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Player Settings")
        
        ttk.Label(frame, text="Max Players:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        self.sv_maxclients = ttk.Entry(frame, width=40)
        self.sv_maxclients.insert(0, "16")
        self.sv_maxclients.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(frame, text="Bot Count:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        self.bot_minplayers = ttk.Entry(frame, width=40)
        self.bot_minplayers.insert(0, "4")
        self.bot_minplayers.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Label(frame, text="Bot Skill (0-5):", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        self.g_botskill = ttk.Combobox(frame, values=["0 (Easy)", "1", "2", "3", "4 (Medium)", "5 (Hard)"], width=37)
        self.g_botskill.grid(row=2, column=1, padx=10, pady=10)
        self.g_botskill.set("2")
    
    def create_server_technical_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Server Technical")
        
        ttk.Label(frame, text="Port:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        self.net_port = ttk.Entry(frame, width=40)
        self.net_port.insert(0, "27960")
        self.net_port.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(frame, text="sv_rate:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        self.sv_rate = ttk.Entry(frame, width=40)
        self.sv_rate.insert(0, "25000")
        self.sv_rate.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Label(frame, text="sv_maxRate:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        self.sv_maxRate = ttk.Entry(frame, width=40)
        self.sv_maxRate.insert(0, "0")
        self.sv_maxRate.grid(row=2, column=1, padx=10, pady=10)
    
    def create_map_rotation_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Map Rotation")
        
        ttk.Label(frame, text="Maplist (one per line):", font=("Arial", 10, "bold")).pack(padx=10, pady=10, anchor=tk.W)
        self.maplist = tk.Text(frame, height=15, width=60)
        self.maplist.pack(padx=10, pady=10)
        
        # Default maps
        default_maps = "q3dm1\nq3dm6\nq3dm7\nq3ctf1\nq3ctf2"
        self.maplist.insert(tk.END, default_maps)
    
    def create_voting_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Voting")
        
        self.g_allowvote = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text="Enable Voting", variable=self.g_allowvote).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        
        ttk.Label(frame, text="Vote Time (seconds):", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        self.g_votetime = ttk.Entry(frame, width=40)
        self.g_votetime.insert(0, "30")
        self.g_votetime.grid(row=1, column=1, padx=10, pady=10)
    
    def create_custom_cvars_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Custom CVARs")
        
        ttk.Label(frame, text="g_motd:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        self.g_motd = ttk.Entry(frame, width=40)
        self.g_motd.insert(0, "Welcome to Quake 3!")
        self.g_motd.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(frame, text="sv_privateClients:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        self.sv_privateClients = ttk.Entry(frame, width=40)
        self.sv_privateClients.insert(0, "0")
        self.sv_privateClients.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Label(frame, text="sv_privatePassword:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        self.sv_privatePassword = ttk.Entry(frame, width=40, show="*")
        self.sv_privatePassword.grid(row=2, column=1, padx=10, pady=10)
        
        ttk.Label(frame, text="g_synchronousClients (0 or 1):", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
        self.g_synchronousClients = ttk.Combobox(frame, values=["0", "1"], width=37)
        self.g_synchronousClients.set("0")
        self.g_synchronousClients.grid(row=3, column=1, padx=10, pady=10)
        
        # Category 3: Required Custom CVARs fields
        ttk.Label(frame, text="sv_fps:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky=tk.W, padx=10, pady=10)
        self.sv_fps = ttk.Entry(frame, width=40)
        self.sv_fps.insert(0, "40")
        self.sv_fps.grid(row=4, column=1, padx=10, pady=10)
        
        ttk.Label(frame, text="sv_maxfps:", font=("Arial", 10, "bold")).grid(row=5, column=0, sticky=tk.W, padx=10, pady=10)
        self.sv_maxfps = ttk.Entry(frame, width=40)
        self.sv_maxfps.insert(0, "100")
        self.sv_maxfps.grid(row=5, column=1, padx=10, pady=10)
        
        ttk.Label(frame, text="server_maxpacketsmax:", font=("Arial", 10, "bold")).grid(row=6, column=0, sticky=tk.W, padx=10, pady=10)
        self.server_maxpacketsmax = ttk.Entry(frame, width=40)
        self.server_maxpacketsmax.insert(0, "125")
        self.server_maxpacketsmax.grid(row=6, column=1, padx=10, pady=10)
        
        ttk.Label(frame, text="server_maxpacketsmin:", font=("Arial", 10, "bold")).grid(row=7, column=0, sticky=tk.W, padx=10, pady=10)
        self.server_maxpacketsmin = ttk.Entry(frame, width=40)
        self.server_maxpacketsmin.insert(0, "125")
        self.server_maxpacketsmin.grid(row=7, column=1, padx=10, pady=10)
    
    def validate_inputs(self):
        # Validate server name
        if not self.sv_hostname.get():
            messagebox.showerror("Error", "Server name is required!")
            return False
        
        # Validate RCON password
        if not self.rconpassword.get():
            messagebox.showerror("Error", "RCON password is required!")
            return False
        
        # Get game type
        gametype = self.g_gametype.get().split()[0]
        
        # Validate fraglimit only if not CTF
        if gametype != "4":
            try:
                int(self.fraglimit.get())
            except ValueError:
                messagebox.showerror("Error", "Fraglimit must be a number!")
                return False
        
        # Validate capturelimit if CTF
        if gametype == "4":
            try:
                int(self.capturelimit.get())
            except ValueError:
                messagebox.showerror("Error", "Captures to Win must be a number!")
                return False
        
        # Validate timelimit
        try:
            int(self.timelimit.get())
        except ValueError:
            messagebox.showerror("Error", "Timelimit must be a number!")
            return False
        
        # Validate max players
        try:
            max_players = int(self.sv_maxclients.get())
            if max_players < 1 or max_players > 64:
                messagebox.showerror("Error", "Max players must be between 1 and 64!")
                return False
        except ValueError:
            messagebox.showerror("Error", "Max players must be a number!")
            return False
        
        # Validate bot count
        try:
            int(self.bot_minplayers.get())
        except ValueError:
            messagebox.showerror("Error", "Bot count must be a number!")
            return False
        
        # Validate port
        try:
            port = int(self.net_port.get())
            if port < 1024 or port > 65535:
                messagebox.showerror("Error", "Port must be between 1024 and 65535!")
                return False
        except ValueError:
            messagebox.showerror("Error", "Port must be a number!")
            return False
        
        # Validate sv_rate
        try:
            int(self.sv_rate.get())
        except ValueError:
            messagebox.showerror("Error", "sv_rate must be a number!")
            return False
        
        # Validate sv_maxRate
        try:
            int(self.sv_maxRate.get())
        except ValueError:
            messagebox.showerror("Error", "sv_maxRate must be a number!")
            return False
        
        # Validate vote time
        try:
            int(self.g_votetime.get())
        except ValueError:
            messagebox.showerror("Error", "Vote time must be a number!")
            return False
        
        # Validate sv_privateClients
        try:
            private_clients = int(self.sv_privateClients.get())
            max_players = int(self.sv_maxclients.get())
            if private_clients > 0 and private_clients < max_players:
                if not self.sv_privatePassword.get():
                    messagebox.showerror("Error", "sv_privatePassword is required when sv_privateClients is set and less than max players!")
                    return False
        except ValueError:
            messagebox.showerror("Error", "sv_privateClients must be a number!")
            return False
        
        # Validate g_synchronousClients
        if self.g_synchronousClients.get() not in ["0", "1"]:
            messagebox.showerror("Error", "g_synchronousClients must be 0 or 1!")
            return False
        
        # Category 3: Validate required fields
        if not self.sv_fps.get():
            messagebox.showerror("Error", "sv_fps is required!")
            return False
        try:
            int(self.sv_fps.get())
        except ValueError:
            messagebox.showerror("Error", "sv_fps must be a number!")
            return False
        
        if not self.sv_maxfps.get():
            messagebox.showerror("Error", "sv_maxfps is required!")
            return False
        try:
            int(self.sv_maxfps.get())
        except ValueError:
            messagebox.showerror("Error", "sv_maxfps must be a number!")
            return False
        
        if not self.server_maxpacketsmax.get():
            messagebox.showerror("Error", "server_maxpacketsmax is required!")
            return False
        try:
            int(self.server_maxpacketsmax.get())
        except ValueError:
            messagebox.showerror("Error", "server_maxpacketsmax must be a number!")
            return False
        
        if not self.server_maxpacketsmin.get():
            messagebox.showerror("Error", "server_maxpacketsmin is required!")
            return False
        try:
            int(self.server_maxpacketsmin.get())
        except ValueError:
            messagebox.showerror("Error", "server_maxpacketsmin must be a number!")
            return False
        
        # Validate maplist
        maps = self.maplist.get("1.0", tk.END).strip().split('\n')
        maps = [m.strip() for m in maps if m.strip()]
        if not maps:
            messagebox.showerror("Error", "At least one map is required!")
            return False
        
        return True
    
    def generate_config(self):
        if not self.validate_inputs():
            return
        
        # Get game type
        gametype = self.g_gametype.get().split()[0]
        is_ctf = gametype == "4"
        
        # Build config content
        config_lines = [
            "// Quake 3 Arena Server Configuration",
            f"// Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "// ============================================",
            "// SERVER IDENTITY",
            "// ============================================",
            f"set sv_hostname \"{self.sv_hostname.get()}\"",
            f"set rconpassword \"{self.rconpassword.get()}\"",
            f"set g_needpass {1 if self.g_needpass.get() else 0}",
            f"set g_password \"{self.g_password.get()}\"",
            "",
            "// ============================================",
            "// GAME SETTINGS",
            "// ============================================",
            f"set g_gametype {gametype}",
        ]
        
        # Add fraglimit or capturelimit based on game type
        if is_ctf:
            config_lines.append(f"set fraglimit 0")
            config_lines.append(f"set capturelimit {self.capturelimit.get()}")
        else:
            config_lines.append(f"set fraglimit {self.fraglimit.get()}")
        
        config_lines.extend([
            f"set timelimit {self.timelimit.get()}",
            f"set sv_pure {self.sv_pure.get()}",
            f"set sv_allowdownloads {self.sv_allowdownloads.get()}",
            "",
            "// ============================================",
            "// PLAYER SETTINGS",
            "// ============================================",
            f"set sv_maxclients {self.sv_maxclients.get()}",
            f"set bot_minplayers {self.bot_minplayers.get()}",
            f"set g_botskill {self.g_botskill.get().split()[0]}",
            "",
            "// ============================================",
            "// SERVER TECHNICAL",
            "// ============================================",
            f"set net_port {self.net_port.get()}",
            f"set sv_rate {self.sv_rate.get()}",
            f"set sv_maxRate {self.sv_maxRate.get()}",
            "",
            "// ============================================",
            "// VOTING",
            "// ============================================",
            f"set g_allowvote {1 if self.g_allowvote.get() else 0}",
            f"set g_votetime {self.g_votetime.get()}",
            "",
            "// ============================================",
            "// CUSTOM CVARS",
            "// ============================================",
            f"set g_motd \"{self.g_motd.get()}\"",
            f"set sv_privateClients {self.sv_privateClients.get()}",
        ])
        
        # Add sv_privatePassword only if set
        if self.sv_privatePassword.get():
            config_lines.append(f"set sv_privatePassword \"{self.sv_privatePassword.get()}\"")
        
        config_lines.extend([
            f"set g_synchronousClients {self.g_synchronousClients.get()}",
            f"set sv_fps {self.sv_fps.get()}",
            f"set sv_maxfps {self.sv_maxfps.get()}",
            f"set server_maxpacketsmax {self.server_maxpacketsmax.get()}",
            f"set server_maxpacketsmin {self.server_maxpacketsmin.get()}",
        ])
        
        # Add CTF-specific settings if game type is CTF
        if is_ctf:
            config_lines.extend([
                "",
                "// ============================================",
                "// CTF SPECIFIC SETTINGS",
                "// ============================================",
                "set bot_enable 1",
                "set g_weaponrespawn 3",
                "set g_dropInactive 1",
                "set g_inactivity 240",
                "set g_forcerespawn 0",
                "set g_friendlyfire 0",
            ])
        
        config_lines.extend([
            "",
            "// ============================================",
            "// MAP ROTATION",
            "// ============================================",
        ])
        
        # Add maplist using vstr chain format
        maps = self.maplist.get("1.0", tk.END).strip().split('\n')
        maps = [m.strip() for m in maps if m.strip()]
        for i, map_name in enumerate(maps):
            next_index = (i + 1) % len(maps)
            config_lines.append(f"set d{i + 1} \"map {map_name} ; set nextmap vstr d{next_index + 1}\"")
        
        config_lines.extend([
            "",
            "// ============================================",
            "// START SERVER",
            "// ============================================",
            "vstr d1",
        ])
        
        config_content = '\n'.join(config_lines)
        
        # Save file dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".cfg",
            filetypes=[("CFG files", "*.cfg"), ("All files", "*.*")],
            initialfile="server.cfg"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(config_content)
                messagebox.showinfo("Success", f"Config file saved successfully!\n\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = Quake3ConfigGenerator(root)
    root.mainloop()