class Deportistas:
    def __init__(self,bdd):
        self.bdd = bdd
        self.conexion = self.bdd.connect()
        self.vigilante = self.conexion.cursor()
        
    def consultar(self):
        sql = f"SELECT * FROM deportistas"
        self.vigilante.execute(sql)
        resultado = self.vigilante.fetchall()
        self.conexion.commit()
        return resultado
    
    def agregar(self,deportista):
        sql = f"INSERT INTO deportistas (id,nombre,estatura,peso,fecha_naci,foto)\
        VALUE ('{deportista[0]}','{deportista[1]}','{deportista[2]}','{deportista[3]}','{deportista[4]}','{deportista[5]}')"
        self.vigilante.execute(sql)
        self.conexion.commit()
