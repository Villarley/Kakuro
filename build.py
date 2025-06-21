import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--name=Kakuro2025',
    '--onefile',
    '--noconsole',
    '--icon=assets/icon.ico'  # Asegúrate de tener el icono en assets/icon.ico
])

print("\n✅ Ejecutable generado. Puedes encontrarlo en la carpeta 'dist'.") 