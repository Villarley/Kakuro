"""
Manager para el manejo del guardado y carga de partidas Kakuro.
Responsable de la gestión de archivos de guardado, carga y validación de datos.
"""

import json
import os
from datetime import datetime
from tkinter import messagebox
from logic.partida_loader import cargar_partida_aleatoria
from logic.config_loader import load_configuracion


class SaveLoadManager:
    def __init__(self):
        self.save_file = "data/kakuro2025_juego_actual.json"
        self.partidas_file = "data/kakuro2025_partidas.json"
        self.records_file = "data/kakuro2025_récords.json"
        
        # Asegurar que el directorio data existe
        os.makedirs("data", exist_ok=True)
    
    def save_game(self, partida_data, estado_tablero, tiempo_transcurrido=None, tiempo_restante=None):
        """
        Guarda el estado actual del juego.
        
        Args:
            partida_data (dict): Datos de la partida
            estado_tablero (list): Estado actual del tablero
            tiempo_transcurrido (int): Tiempo transcurrido en segundos
            tiempo_restante (int): Tiempo restante en segundos
            
        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        try:
            # Preparar datos para guardar
            save_data = {
                "fecha_guardado": datetime.now().isoformat(),
                "partida_data": partida_data,
                "estado_tablero": estado_tablero,
                "tiempo_transcurrido": tiempo_transcurrido or 0,
                "tiempo_restante": tiempo_restante,
                "jugador": partida_data.get("jugador", "Jugador"),
                "nivel_dificultad": partida_data.get("nivel_de_dificultad", "FÁCIL")
            }
            
            # Guardar en archivo
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            print(f"[SAVE] Juego guardado exitosamente en {self.save_file}")
            return True
            
        except Exception as e:
            print(f"[SAVE] Error al guardar juego: {e}")
            messagebox.showerror("Error", f"Error al guardar el juego:\n{str(e)}")
            return False
    
    def load_game(self):
        """
        Carga el estado guardado del juego.
        
        Returns:
            dict or None: Datos del juego guardado o None si no hay guardado
        """
        try:
            if not os.path.exists(self.save_file):
                print("[LOAD] No hay archivo de guardado")
                return None
            
            with open(self.save_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            # Validar datos cargados
            if not self._validate_save_data(save_data):
                print("[LOAD] Datos de guardado inválidos")
                return None
            
            print(f"[LOAD] Juego cargado exitosamente desde {self.save_file}")
            return save_data
            
        except Exception as e:
            print(f"[LOAD] Error al cargar juego: {e}")
            messagebox.showerror("Error", f"Error al cargar el juego:\n{str(e)}")
            return None
    
    def _validate_save_data(self, save_data):
        """
        Valida que los datos de guardado sean correctos.
        
        Args:
            save_data (dict): Datos de guardado a validar
            
        Returns:
            bool: True si los datos son válidos, False en caso contrario
        """
        required_keys = ["partida_data", "estado_tablero", "fecha_guardado"]
        
        # Verificar claves requeridas
        for key in required_keys:
            if key not in save_data:
                print(f"[LOAD] Falta clave requerida: {key}")
                return False
        
        # Verificar estructura del estado del tablero
        estado_tablero = save_data["estado_tablero"]
        if not isinstance(estado_tablero, list) or len(estado_tablero) != 9:
            print("[LOAD] Estado del tablero inválido")
            return False
        
        for fila in estado_tablero:
            if not isinstance(fila, list) or len(fila) != 9:
                print("[LOAD] Fila del tablero inválida")
                return False
        
        # Verificar datos de partida
        partida_data = save_data["partida_data"]
        if not isinstance(partida_data, dict) or "claves" not in partida_data:
            print("[LOAD] Datos de partida inválidos")
            return False
        
        return True
    
    def has_saved_game(self):
        """
        Verifica si existe un juego guardado.
        
        Returns:
            bool: True si existe un juego guardado, False en caso contrario
        """
        return os.path.exists(self.save_file)
    
    def delete_save(self):
        """
        Elimina el archivo de guardado.
        
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        try:
            if os.path.exists(self.save_file):
                os.remove(self.save_file)
                print(f"[SAVE] Archivo de guardado eliminado: {self.save_file}")
                return True
            else:
                print("[SAVE] No hay archivo de guardado para eliminar")
                return False
                
        except Exception as e:
            print(f"[SAVE] Error al eliminar archivo de guardado: {e}")
            return False
    
    def save_to_partidas(self, partida_data, estado_tablero, tiempo_transcurrido, completada=False):
        """
        Guarda la partida en el historial de partidas.
        
        Args:
            partida_data (dict): Datos de la partida
            estado_tablero (list): Estado final del tablero
            tiempo_transcurrido (int): Tiempo transcurrido en segundos
            completada (bool): Si la partida fue completada
            
        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        try:
            # Cargar partidas existentes
            partidas = self._load_partidas_file()
            
            # Crear entrada de partida
            partida_entry = {
                "fecha": datetime.now().isoformat(),
                "jugador": partida_data.get("jugador", "Jugador"),
                "nivel_dificultad": partida_data.get("nivel_de_dificultad", "FÁCIL"),
                "tiempo_transcurrido": tiempo_transcurrido,
                "completada": completada,
                "estado_final": estado_tablero,
                "partida_id": partida_data.get("id", "unknown")
            }
            
            # Agregar al historial
            partidas.append(partida_entry)
            
            # Guardar archivo actualizado
            with open(self.partidas_file, 'w', encoding='utf-8') as f:
                json.dump(partidas, f, indent=2, ensure_ascii=False)
            
            print(f"[SAVE] Partida guardada en historial: {partida_entry['fecha']}")
            return True
            
        except Exception as e:
            print(f"[SAVE] Error al guardar partida en historial: {e}")
            return False
    
    def _load_partidas_file(self):
        """
        Carga el archivo de partidas.
        
        Returns:
            list: Lista de partidas guardadas
        """
        try:
            if os.path.exists(self.partidas_file):
                with open(self.partidas_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            print(f"[LOAD] Error al cargar archivo de partidas: {e}")
            return []
    
    def get_partidas_history(self, limit=None):
        """
        Obtiene el historial de partidas.
        
        Args:
            limit (int): Número máximo de partidas a retornar
            
        Returns:
            list: Lista de partidas del historial
        """
        partidas = self._load_partidas_file()
        
        # Ordenar por fecha (más recientes primero)
        partidas.sort(key=lambda x: x.get("fecha", ""), reverse=True)
        
        # Aplicar límite si se especifica
        if limit:
            partidas = partidas[:limit]
        
        return partidas
    
    def save_record(self, jugador, nivel_dificultad, tiempo_transcurrido):
        """
        Guarda un nuevo récord.
        
        Args:
            jugador (str): Nombre del jugador
            nivel_dificultad (str): Nivel de dificultad
            tiempo_transcurrido (int): Tiempo transcurrido en segundos
            
        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        try:
            # Cargar récords existentes
            records = self._load_records_file()
            
            # Crear entrada de récord
            record_entry = {
                "fecha": datetime.now().isoformat(),
                "jugador": jugador,
                "nivel_dificultad": nivel_dificultad,
                "tiempo_transcurrido": tiempo_transcurrido,
                "tiempo_formato": self._format_time(tiempo_transcurrido)
            }
            
            # Agregar al historial de récords
            records.append(record_entry)
            
            # Ordenar por tiempo (más rápido primero)
            records.sort(key=lambda x: x["tiempo_transcurrido"])
            
            # Mantener solo los mejores 10 récords por nivel
            records_filtered = []
            for nivel in ["FÁCIL", "MEDIO", "DIFÍCIL"]:
                nivel_records = [r for r in records if r["nivel_dificultad"] == nivel]
                records_filtered.extend(nivel_records[:10])
            
            # Guardar archivo actualizado
            with open(self.records_file, 'w', encoding='utf-8') as f:
                json.dump(records_filtered, f, indent=2, ensure_ascii=False)
            
            print(f"[SAVE] Récord guardado: {jugador} - {nivel_dificultad} - {self._format_time(tiempo_transcurrido)}")
            return True
            
        except Exception as e:
            print(f"[SAVE] Error al guardar récord: {e}")
            return False
    
    def _load_records_file(self):
        """
        Carga el archivo de récords.
        
        Returns:
            list: Lista de récords guardados
        """
        try:
            if os.path.exists(self.records_file):
                with open(self.records_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            print(f"[LOAD] Error al cargar archivo de récords: {e}")
            return []
    
    def get_records(self, nivel_dificultad=None):
        """
        Obtiene los récords guardados.
        
        Args:
            nivel_dificultad (str): Filtrar por nivel de dificultad
            
        Returns:
            list: Lista de récords
        """
        records = self._load_records_file()
        
        if nivel_dificultad:
            records = [r for r in records if r["nivel_dificultad"] == nivel_dificultad]
        
        return records
    
    def _format_time(self, segundos):
        """
        Formatea el tiempo en formato legible.
        
        Args:
            segundos (int): Tiempo en segundos
            
        Returns:
            str: Tiempo formateado
        """
        horas = segundos // 3600
        minutos = (segundos % 3600) // 60
        segs = segundos % 60
        
        if horas > 0:
            return f"{horas:02}:{minutos:02}:{segs:02}"
        else:
            return f"{minutos:02}:{segs:02}"
    
    def get_save_info(self):
        """
        Obtiene información sobre el archivo de guardado.
        
        Returns:
            dict: Información del archivo de guardado
        """
        if not os.path.exists(self.save_file):
            return {"exists": False}
        
        try:
            stat = os.stat(self.save_file)
            return {
                "exists": True,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "path": self.save_file
            }
        except Exception as e:
            return {"exists": True, "error": str(e)}
    
    def backup_save(self, backup_name=None):
        """
        Crea una copia de seguridad del archivo de guardado.
        
        Args:
            backup_name (str): Nombre del archivo de respaldo
            
        Returns:
            bool: True si se creó correctamente, False en caso contrario
        """
        try:
            if not os.path.exists(self.save_file):
                print("[BACKUP] No hay archivo de guardado para respaldar")
                return False
            
            if not backup_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"data/kakuro2025_backup_{timestamp}.json"
            
            import shutil
            shutil.copy2(self.save_file, backup_name)
            print(f"[BACKUP] Respaldo creado: {backup_name}")
            return True
            
        except Exception as e:
            print(f"[BACKUP] Error al crear respaldo: {e}")
            return False
    
    def restore_from_backup(self, backup_path):
        """
        Restaura el archivo de guardado desde un respaldo.
        
        Args:
            backup_path (str): Ruta del archivo de respaldo
            
        Returns:
            bool: True si se restauró correctamente, False en caso contrario
        """
        try:
            if not os.path.exists(backup_path):
                print(f"[RESTORE] Archivo de respaldo no encontrado: {backup_path}")
                return False
            
            import shutil
            shutil.copy2(backup_path, self.save_file)
            print(f"[RESTORE] Archivo restaurado desde: {backup_path}")
            return True
            
        except Exception as e:
            print(f"[RESTORE] Error al restaurar archivo: {e}")
            return False 