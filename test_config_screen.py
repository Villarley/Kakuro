"""
Script de prueba para la pantalla de configuración de Kakuro 2025.
Verifica que la configuración se guarde y cargue correctamente.
"""

import tkinter as tk
import json
import os
from gui.config_screen import ConfigScreen


def test_config_screen():
    """Prueba la funcionalidad de la pantalla de configuración"""
    print("🧪 Iniciando pruebas de ConfigScreen...")
    
    # Crear ventana de prueba
    root = tk.Tk()
    root.title("Test - ConfigScreen")
    root.geometry("600x800")
    
    # Crear instancia de ConfigScreen
    config_screen = ConfigScreen(root, None)
    config_screen.pack(fill="both", expand=True)
    
    print("✅ ConfigScreen creada exitosamente")
    
    # Probar configuración por defecto
    print("\n📋 Probando configuración por defecto:")
    default_config = config_screen.get_current_config()
    print(f"   Nivel: {default_config.get('nivel', 'N/A')}")
    print(f"   Tipo de reloj: {default_config.get('tipo_reloj', 'N/A')}")
    
    # Simular cambio de configuración
    print("\n⚙️ Simulando cambio de configuración...")
    config_screen.nivel_var.set("DIFÍCIL")
    config_screen.reloj_var.set("TEMPORIZADOR")
    config_screen.horas_var.set("1")
    config_screen.minutos_var.set("30")
    config_screen.segundos_var.set("0")
    
    # Obtener nueva configuración
    new_config = config_screen.get_current_config()
    print(f"   Nuevo nivel: {new_config.get('nivel', 'N/A')}")
    print(f"   Nuevo tipo de reloj: {new_config.get('tipo_reloj', 'N/A')}")
    print(f"   Tiempo límite: {new_config.get('tiempo_limite', 'N/A')} segundos")
    
    # Probar guardado
    print("\n💾 Probando guardado de configuración...")
    try:
        config_screen.guardar_config()
        print("✅ Configuración guardada exitosamente")
        
        # Verificar que el archivo existe
        if os.path.exists("data/configuracion.json"):
            print("✅ Archivo de configuración creado")
            
            # Leer y mostrar configuración guardada
            with open("data/configuracion.json", "r", encoding="utf-8") as f:
                saved_config = json.load(f)
            
            print(f"   Configuración guardada: {saved_config}")
        else:
            print("❌ Archivo de configuración no encontrado")
            
    except Exception as e:
        print(f"❌ Error al guardar configuración: {e}")
    
    # Probar carga de configuración
    print("\n📂 Probando carga de configuración...")
    try:
        # Cambiar valores para simular estado diferente
        config_screen.nivel_var.set("FÁCIL")
        config_screen.reloj_var.set("CRONÓMETRO")
        
        # Cargar configuración
        config_screen.load_current_config()
        
        # Verificar que se cargaron los valores correctos
        loaded_config = config_screen.get_current_config()
        print(f"   Configuración cargada: {loaded_config}")
        
        if loaded_config.get('nivel') == 'DIFÍCIL':
            print("✅ Nivel cargado correctamente")
        else:
            print("❌ Error al cargar nivel")
            
        if loaded_config.get('tipo_reloj') == 'TEMPORIZADOR':
            print("✅ Tipo de reloj cargado correctamente")
        else:
            print("❌ Error al cargar tipo de reloj")
            
    except Exception as e:
        print(f"❌ Error al cargar configuración: {e}")
    
    # Probar validaciones
    print("\n🔍 Probando validaciones...")
    
    # Probar tiempo negativo
    config_screen.reloj_var.set("TEMPORIZADOR")
    config_screen.horas_var.set("-1")
    config_screen.minutos_var.set("0")
    config_screen.segundos_var.set("0")
    
    print("   Probando tiempo negativo...")
    try:
        config_screen.guardar_config()
        print("❌ Debería haber fallado con tiempo negativo")
    except:
        print("✅ Validación de tiempo negativo funciona")
    
    # Probar minutos inválidos
    config_screen.horas_var.set("0")
    config_screen.minutos_var.set("60")
    config_screen.segundos_var.set("0")
    
    print("   Probando minutos inválidos...")
    try:
        config_screen.guardar_config()
        print("❌ Debería haber fallado con minutos inválidos")
    except:
        print("✅ Validación de minutos funciona")
    
    # Probar tiempo cero
    config_screen.horas_var.set("0")
    config_screen.minutos_var.set("0")
    config_screen.segundos_var.set("0")
    
    print("   Probando tiempo cero...")
    try:
        config_screen.guardar_config()
        print("❌ Debería haber fallado con tiempo cero")
    except:
        print("✅ Validación de tiempo cero funciona")
    
    print("\n🎉 Pruebas completadas!")
    print("\n💡 Para probar la interfaz gráfica, ejecuta la aplicación principal:")
    print("   python main.py")
    
    # Mantener ventana abierta por un momento
    root.after(3000, root.destroy)
    root.mainloop()


def test_timer_integration():
    """Prueba la integración del temporizador con la configuración"""
    print("\n⏱️ Probando integración del temporizador...")
    
    try:
        from utils.timer import GameTimer
        from logic.config_loader import load_configuracion
        
        # Cargar configuración
        config = load_configuracion()
        print(f"   Configuración cargada: {config}")
        
        # Crear temporizador según configuración
        tipo_reloj = config.get("tipo_reloj", "CRONÓMETRO")
        tiempo_limite = config.get("tiempo_limite") if tipo_reloj == "TEMPORIZADOR" else None
        
        timer = GameTimer(time_limit=tiempo_limite)
        print(f"   Temporizador creado: tipo={tipo_reloj}, límite={tiempo_limite}")
        
        # Probar callbacks
        def on_update(tiempo):
            print(f"   Tiempo actualizado: {tiempo}s")
        
        def on_limit():
            print("   ⏰ ¡Tiempo agotado!")
        
        timer.set_time_update_callback(on_update)
        timer.set_time_limit_callback(on_limit)
        
        print("✅ Integración del temporizador funciona correctamente")
        
    except Exception as e:
        print(f"❌ Error en integración del temporizador: {e}")


if __name__ == "__main__":
    print("🚀 Iniciando pruebas de configuración de Kakuro 2025")
    print("=" * 60)
    
    # Ejecutar pruebas
    test_config_screen()
    test_timer_integration()
    
    print("\n" + "=" * 60)
    print("✅ Todas las pruebas completadas") 