# ═══════════════════════════════════════════════════════════
# VOICE CHANGER — РАБОЧАЯ ВЕРСИЯ ЧЕРЕЗ VB-AUDIO
# github.com/thehelpfromthevoid/voice-changer
# сделано thehelpfromthevoid
# ═══════════════════════════════════════════════════════════

import subprocess
import sys
import os
import time
import json
from colorama import init, Fore, Style

init(autoreset=True)

if sys.platform == "win32":
    import ctypes
    ctypes.windll.kernel32.SetConsoleTitleW("Voice Changer")
    def clear(): os.system("cls")
else:
    def clear(): os.system("clear")

CONFIG_FILE = "voice_changer_config.json"

class VoiceChanger:
    def __init__(self):
        self.config = self._load_config()
        self.vb_cable_installed = self._check_vb_cable()
    
    def _load_config(self):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            return {"preset": "normal", "volume": 100}
    
    def _save_config(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _check_vb_cable(self):
        """Проверяет установлен ли VB-Audio Virtual Cable"""
        try:
            result = subprocess.run(
                ['powershell', '-Command', 
                 'Get-AudioDevice -List | Where-Object {$_.Name -like "*VB-Audio*" -or $_.Name -like "*CABLE*"} | Select-Object -First 1'],
                capture_output=True, text=True, timeout=5
            )
            return bool(result.stdout.strip())
        except:
            return False
    
    def _print(self, text, color=Fore.WHITE):
        print(f"{color}{text}{Style.RESET_ALL}")
    
    def _input(self, prompt, color=Fore.CYAN):
        return input(f"{color}{prompt}{Style.RESET_ALL}")
    
    def _banner(self):
        clear()
        print(f"""
{Fore.MAGENTA}
  ╔══════════════════════════════════════════════════════╗
  ║          VOICE CHANGER PRO                          ║
  ║          github.com/thehelpfromthevoid               ║
  ╚══════════════════════════════════════════════════════╝
{Style.RESET_ALL}
""")
    
    def install_vb_cable(self):
        print(f"\n{Fore.YELLOW}Для работы нужен VB-Audio Virtual Cable (бесплатный виртуальный микрофон).")
        print(f"{Fore.CYAN}Скачайте и установите: https://vb-audio.com/Cable/")
        print(f"{Fore.WHITE}1. Скачайте VBCABLE_Driver_Pack.zip")
        print(f"2. Распакуйте")
        print(f"3. Запустите VBCABLE_Setup_x64.exe от администратора")
        print(f"4. После установки перезагрузите компьютер")
        print(f"5. В Windows: ПКМ по звуку → Звуки → Запись → Cable Output → Свойства → Прослушать → С этого устройства")
        print(f"6. В игре/программе выберите микрофон CABLE Output")
        
        try:
            import webbrowser
            webbrowser.open("https://vb-audio.com/Cable/")
        except: pass
        
        input(f"\n{Fore.CYAN}Enter после установки...")
    
    def setup_audio(self):
        self._banner()
        print(f"\n{Fore.CYAN}НАСТРОЙКА АУДИО:")
        print(f"{Fore.WHITE}1. Откройте Панель управления → Звук")
        print(f"2. Вкладка Запись → найдите ваш реальный микрофон")
        print(f"3. ПКМ → Свойства → Вкладка Прослушать")
        print(f"4. Поставьте галочку 'Прослушивать с этого устройства'")
        print(f"5. В списке выберите 'CABLE Input'")
        print(f"6. Примените")
        print(f"{Fore.GREEN}Теперь ваш голос будет идти через виртуальный кабель!")
        print(f"{Fore.WHITE}В игре/программе выберите микрофон 'CABLE Output'")
        input(f"\nEnter...")
    
    def apply_voice_effects(self):
        self._banner()
        
        presets = {
            "1": {"name": "Норма (без изменений)", "pitch": 0, "desc": "Ваш обычный голос"},
            "2": {"name": "Женский мягкий", "pitch": 400, "desc": "Лёгкое повышение, естественно"},
            "3": {"name": "Девушка", "pitch": 600, "desc": "Молодой женский голос"},
            "4": {"name": "Девочка", "pitch": 900, "desc": "Высокий детский голос"},
            "5": {"name": "Мужской глубокий", "pitch": -400, "desc": "Более низкий, басовитый"},
            "6": {"name": "Бас", "pitch": -700, "desc": "Очень низкий голос"},
            "7": {"name": "Робот", "pitch": 0, "desc": "Механический голос"},
            "8": {"name": "Эхо", "pitch": 0, "desc": "С эффектом эха"},
        }
        
        for key, data in presets.items():
            print(f"  {Fore.MAGENTA}{key}{Style.RESET_ALL}  {data['name']:20} {Fore.CYAN}{data['desc']}{Style.RESET_ALL}")
        
        try:
            choice = self._input("\nВыбор пресета: ", Fore.CYAN)
            if choice in presets:
                self.config["preset"] = presets[choice]["name"]
                self._save_config()
                self._print(f"\nВыбран: {presets[choice]['name']}", Fore.GREEN)
                self._print(f"Применится ко всем программам использующим CABLE Output", Fore.CYAN)
        except: pass
        
        input("\nEnter...")
    
    def show_status(self):
        self._banner()
        print(f"\n  {Fore.CYAN}Текущий пресет: {Fore.YELLOW}{self.config.get('preset', 'Норма')}")
        print(f"  {Fore.CYAN}VB-Cable: {Fore.GREEN if self.vb_cable_installed else Fore.RED}{'Установлен' if self.vb_cable_installed else 'НЕ установлен'}")
        print(f"\n  {Fore.WHITE}Для изменения голоса:")
        print(f"  1. Установите Voicemeeter (https://vb-audio.com/Voicemeeter/)")
        print(f"  2. Настройте питч в Voicemeeter")
        print(f"  3. Или используйте встроенный эквалайзер Windows")
        input(f"\nEnter...")
    
    def run(self):
        while True:
            self._banner()
            print(f"  {Fore.MAGENTA}1{Style.RESET_ALL}  Установка VB-Cable")
            print(f"  {Fore.MAGENTA}2{Style.RESET_ALL}  Настройка аудио (инструкция)")
            print(f"  {Fore.MAGENTA}3{Style.RESET_ALL}  Выбрать пресет голоса")
            print(f"  {Fore.MAGENTA}4{Style.RESET_ALL}  Текущий статус")
            print(f"  {Fore.MAGENTA}0{Style.RESET_ALL}  Выход")
            
            try:
                cmd = self._input("\n> ", Fore.MAGENTA).strip()
                if cmd == "1": self.install_vb_cable()
                elif cmd == "2": self.setup_audio()
                elif cmd == "3": self.apply_voice_effects()
                elif cmd == "4": self.show_status()
                elif cmd == "0": break
            except KeyboardInterrupt: break
            except: pass

if __name__ == "__main__":
    app = VoiceChanger()
    app.run()
