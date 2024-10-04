import os
import platform

from laboratorio_poo import (
    ProductoElectronico,
    ProductoAlimenticio,
    Inventario
)




def limpiar_pantalla():
    
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
        
def mostrar_menu():
        print("\n--- Sistema de Gestión de Productos ---")
        print("1. Agregar producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Listar productos")
        print("5. Salir")

def agregar_producto(inventario):
    try:
        tipo_codigo = input("Seleccione el tipo de producto (1: Electrónico, 2: Alimenticio): ")
        codigo = input('Ingrese código del Producto: ')
        nombre = input('Ingrese nombre del Producto: ')
        precio = float(input('Ingrese precio del Producto: '))
        cantidad = int(input('Ingrese cantidad del Producto: '))

        if tipo_codigo == '1':
            garantia = int(input('Ingrese garantía (en años): '))
            producto = ProductoElectronico(codigo, nombre, precio, cantidad, garantia)
        elif tipo_codigo == '2':
            fecha_expiracion = input('Ingrese fecha de expiración ): ')
            producto = ProductoAlimenticio(codigo, nombre, precio, cantidad, fecha_expiracion)
        else:
            print('Opción inválida')
            return

        inventario.agregar_producto(producto)
        print("Producto agregado exitosamente.")

    except ValueError as e:
        print(f'Error: {e}')
    
def eliminar_producto(inventario):
    try:
        codigo = input('Ingrese el código del producto a eliminar: ')
        inventario.eliminar_producto(codigo)
        print("Producto eliminado exitosamente.")
    except ValueError as e:
        print(f'Error: {e}') 

def actualizar_producto(inventario):
    try:
        codigo = input('Ingrese el código del producto a actualizar: ')
        nombre = input('Ingrese nuevo nombre del Producto: ')
        precio = float(input('Ingrese nuevo precio del Producto: '))
        cantidad = int(input('Ingrese nueva cantidad del Producto: '))

        datos = inventario.leer_datos()
        if str(codigo) in datos.keys():
            tipo = datos[str(codigo)]['tipo']
            if tipo == 'ProductoElectronico':
                garantia = int(input('Ingrese nueva garantía (en años): '))
                nuevo_producto = ProductoElectronico(codigo, nombre, precio, cantidad, garantia)
            elif tipo == 'ProductoAlimenticio':
                fecha_expiracion = input('Ingrese nueva fecha de expiración (YYYY-MM-DD): ')
                nuevo_producto = ProductoAlimenticio(codigo, nombre, precio, cantidad, fecha_expiracion)
            else:
                print('Opción inválida')
                return

            inventario.actualizar_producto(codigo, nuevo_producto.to_dict())
            print("Producto actualizado exitosamente.")
        else:
            print("Producto no encontrado.")

    except ValueError as e:
        print(f'Error: {e}')         

def listar_productos(inventario):
    try:
        datos = inventario.leer_datos()
        if datos:
            for codigo, detalles in datos.items():
                print(f"Código: {codigo}")
                for key, value in detalles.items():
                    print(f"  {key.capitalize()}: {value}")
                print("-" * 20)
        else:
            print("No hay productos en el inventario.")
    except Exception as e:
        print(f'Error al listar productos: {e}')




def main():
    inventario = Inventario(host="localhost", user="root", password="febrero2", database="inventario_db")
    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_producto(inventario)
        elif opcion == "2":
            eliminar_producto(inventario)
        elif opcion == "3":
            actualizar_producto(inventario)
        elif opcion == "4":
            listar_productos(inventario)
        elif opcion == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
        input("Presione Enter para continuar...")

if __name__ == "__main__":
    main()