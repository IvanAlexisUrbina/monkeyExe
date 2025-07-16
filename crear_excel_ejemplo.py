import pandas as pd

# Crear datos de ejemplo
data = {
    'Numero': ['4111111111111111', '4222222222222222', '4333333333333333', '4444444444444444'],
    'Mes': ['12', '01', '06', '03'],
    'Año': ['25', '26', '24', '27'],
    'CVV': ['123', '456', '789', '321']
}

df = pd.DataFrame(data)
df.to_excel('tarjetas_ejemplo.xlsx', index=False)
print("Archivo Excel de ejemplo creado: tarjetas_ejemplo.xlsx")