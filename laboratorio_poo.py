'''
Desafío 1: Sistema de Gestión de Productos
Objetivo: Desarrollar un sistema para manejar productos en un inventario.

Requisitos:

Crear una clase base Producto con atributos como codigo, nombre, precio, cantidad en stock, etc.
Definir al menos 2 clases derivadas para diferentes categorías de productos (por ejemplo, ProductoElectronico, ProductoAlimenticio) con atributos y métodos específicos.
Implementar operaciones CRUD para gestionar productos del inventario.
Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
Persistir los datos en archivo JSON.
'''

import json
import mysql.connector

class Producto:
    def __init__(self, codigo, nombre, precio, cantidad):
        self.__codigo = self.validar_codigo(codigo)
        self.__nombre = nombre
        self.__precio = precio
        self.__cantidad = cantidad
 
    @property
    def codigo(self):
        return self.__codigo
    
    @property
    def nombre(self):
        return self.__nombre.capitalize()
    
    @property
    def precio(self):
        return self.__precio
    
    @property
    def cantidad(self):
        return self.__cantidad

    def validar_codigo(self,codigo):
        try:
            codigo_num = float(codigo)
            if codigo_num <= 0:
                raise ValueError("El código debe ser numérico positivo.")
            return codigo_num
        except ValueError:
            raise ValueError("El código debe ser un número válido.")

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "cantidad": self.cantidad
        }



    def __str__(self):
        return f"Código:{self.codigo}, Producto: {self.nombre}, Precio: {self.precio}, Cantidad: {self.cantidad}"


class ProductoElectronico(Producto):
    def __init__(self, codigo, nombre, precio, cantidad, garantia):
        super().__init__(codigo, nombre, precio, cantidad)
        self.garantia = garantia

    @property
    def garantia(self):
        return self.__garantia
    
    @garantia.setter
    def garantia(self, valor):
        self.__garantia = valor
    
    def to_dict(self):
        data = super().to_dict()
        data["garantia"] = self.garantia
        return data

    def __str__(self):
        return f"Código: {self.codigo}, Producto Electrónico: {self.nombre}, Precio: {self.precio}, Cantidad: {self.cantidad}, Garantía: {self.garantia} años"


class ProductoAlimenticio(Producto):
    def __init__(self, codigo, nombre, precio, cantidad, fecha_expiracion):
        super().__init__(codigo, nombre, precio, cantidad)
        self.__fecha_expiracion = fecha_expiracion

   
    
    @property
    def fecha_expiracion(self):
        return self.__fecha_expiracion
    
    @fecha_expiracion.setter
    def fecha_expiracion(self, valor):
        self.__fecha_expiracion = valor
    
    def to_dict(self):
        data = super().to_dict()
        data["fecha_expiracion"] = self.fecha_expiracion
        return data
    
    def __str__(self):
        return f" Código: {self.codigo}, Producto Alimenticio: {self.nombre}, Precio: {self.precio}, Cantidad: {self.cantidad}, Fecha de Expiración: {self.fecha_expiracion}"
    

class Inventario:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
           
        self.cursor = self.connection.cursor()
        self.crear_tabla() 
        

    def crear_tabla(self):
        # Crear la tabla si no existe
        query = """
        CREATE TABLE IF NOT EXISTS productos (
            codigo INT PRIMARY KEY,
            nombre VARCHAR(255),
            precio FLOAT,
            cantidad INT,
            tipo VARCHAR(255),
            garantia INT,
            fecha_expiracion DATE
        )
        """
        self.cursor.execute(query)
        self.connection.commit()   

    def agregar_producto(self, producto):
        try:
            if isinstance(producto, ProductoElectronico):
                query = """
                INSERT INTO productos (codigo, nombre, precio, cantidad, tipo, garantia)
                VALUES (%s, %s, %s, %s, 'ProductoElectronico', %s)
                """
                values = (producto.codigo, producto.nombre, producto.precio, producto.cantidad, producto.garantia)
            elif isinstance(producto, ProductoAlimenticio):
                query = """
                INSERT INTO productos (codigo, nombre, precio, cantidad, tipo, fecha_expiracion)
                VALUES (%s, %s, %s, %s, 'ProductoAlimenticio', %s)
                """
                values = (producto.codigo, producto.nombre, producto.precio, producto.cantidad, producto.fecha_expiracion)
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Producto agregado exitosamente.")
        except mysql.connector.Error as error:
            print(f'Error al agregar producto: {error}')

    def eliminar_producto(self, codigo):
        try:
            query = "DELETE FROM productos WHERE codigo = %s"
            self.cursor.execute(query, (codigo,))
            self.connection.commit()
            print(f'Producto con código {codigo} eliminado.')
        except mysql.connector.Error as error:
            print(f'Error al eliminar producto: {error}')

    def actualizar_producto(self, codigo, nuevos_datos):
        try:
            query = """
            UPDATE productos
            SET nombre = %s, precio = %s, cantidad = %s, garantia = %s, fecha_expiracion = %s
            WHERE codigo = %s
            """
            values = (nuevos_datos['nombre'], nuevos_datos['precio'], nuevos_datos['cantidad'],
                    nuevos_datos.get('garantia'), nuevos_datos.get('fecha_expiracion'), codigo)
            self.cursor.execute(query, values)
            self.connection.commit()
            print(f'Producto actualizado Código:{codigo}')
        except mysql.connector.Error as error:
            print(f'Error al actualizar producto: {error}')

    def listar_productos(self):
        try:
            query = "SELECT * FROM productos"
            self.cursor.execute(query)
            productos = self.cursor.fetchall()
            if productos:
                for producto in productos:
                    print(producto)
            else:
                print("No hay productos en el inventario.")
        except mysql.connector.Error as error:
            print(f'Error al listar productos: {error}')
    