import os
from datetime import datetime
from enum import Enum

class LogLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

class Logs:
    """
    Clase para gestionar logs de ejecución del proceso ETL.
    Genera archivos de log con timestamp y registra mensajes con diferentes niveles.
    """
    
    def __init__(self, log_dir: str = "logs", script_name: str = "etl"):
        """
        Inicializa el sistema de logs.
        
        Args:
            log_dir: Directorio donde se guardarán los logs (relativo al proyecto)
            script_name: Nombre del script para identificar el archivo de log
        """
        self.log_dir = log_dir
        self.script_name = script_name
        
        # Verificar que el directorio de logs existe
        if not os.path.exists(self.log_dir):
            raise FileNotFoundError(f"El directorio '{self.log_dir}' no existe. Por favor créalo antes de ejecutar.")
        
        if not os.path.isdir(self.log_dir):
            raise NotADirectoryError(f"'{self.log_dir}' no es un directorio válido.")
        
        # Generar nombre de archivo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        self.log_file = os.path.join(self.log_dir, f"log_{script_name}_{timestamp}.txt")
        
        # Inicializar archivo de log
        self._write_header()
    
    def _write_header(self):
        """Escribe el encabezado del archivo de log."""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"LOG DE EJECUCIÓN - {self.script_name.upper()}\n")
            f.write(f"Fecha de inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
    
    def _write_log(self, level: LogLevel, message: str):
        """
        Escribe un mensaje en el archivo de log.
        
        Args:
            level: Nivel del log (INFO, WARNING, ERROR)
            message: Mensaje a registrar
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level.value}] {message}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        # También imprimir en consola
        print(log_entry.strip())
    
    def info(self, message: str):
        """Registra un mensaje informativo."""
        self._write_log(LogLevel.INFO, message)
    
    def warning(self, message: str):
        """Registra una advertencia."""
        self._write_log(LogLevel.WARNING, message)
    
    def error(self, message: str):
        """Registra un error."""
        self._write_log(LogLevel.ERROR, message)
    
    def separator(self):
        """Escribe una línea separadora en el log."""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write("-" * 80 + "\n")
    
    def close(self):
        """Cierra el archivo de log con un mensaje de finalización."""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"Fecha de finalización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n")
        print(f"\nLog guardado en: {self.log_file}")