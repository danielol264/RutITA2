from .User import User
class modelo():
    def login(db,usuario):
        
          cur=db.connection.cursor()
          cur.execute("SELECT ID_Persona,Usuario,Contraseña FROM persona WHERE Usuario='{}'".format(usuario.usuario))
          row=cur.fetchone()
          if row != None:
            usera=User(row[0],row[1],User.chechar_contraseña(row[2],usuario.contraseña))
            return usera
          else:  
             return None
    
    def get_by_id(db,id):
        
          cur=db.connection.cursor()
          cur.execute("SELECT ID_Persona,Usuario,Contraseña FROM persona WHERE ID_Persona='{}'".format(id))
          row=cur.fetchone()
          
          if row != None:
            usera=User(row[0],row[1],row[2])
            return usera
          else:  
             return None 