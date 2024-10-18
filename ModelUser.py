from User import User

usuario_contraseña=(("axel", "scrypt:32768:8:1$3GljcjtIfOjKGy52$6aaccded2952863ad79f34f8790061f9d842ea4b90e07e5338bcb3f8ada3ceae8d12167148a56ba95b83aa3f97af0f28cc007ae5e881b5d865dbb78bcb2d3346"),
                        ("alondra", "scrypt:32768:8:1$3GljcjtIfOjKGy52$6aaccded2952863ad79f34f8790061f9d842ea4b90e07e5338bcb3f8ada3ceae8d12167148a56ba95b83aa3f97af0f28cc007ae5e881b5d865dbb78bcb2d3346"),
                        ("kevin", "scrypt:32768:8:1$3GljcjtIfOjKGy52$6aaccded2952863ad79f34f8790061f9d842ea4b90e07e5338bcb3f8ada3ceae8d12167148a56ba95b83aa3f97af0f28cc007ae5e881b5d865dbb78bcb2d3346"),
                        ("daniel", "scrypt:32768:8:1$3GljcjtIfOjKGy52$6aaccded2952863ad79f34f8790061f9d842ea4b90e07e5338bcb3f8ada3ceae8d12167148a56ba95b83aa3f97af0f28cc007ae5e881b5d865dbb78bcb2d3346"))
class ModelUser():

    
    def login(usuario):
        
        for usuarios in  usuario_contraseña:
          print(usuarios[1])
          print(usuario.contraseña)
          if usuarios[0]== usuario.usuario:
            usera=User(usuario.usuario,User.chechar_contraseña(usuarios[1],usuario.contraseña))
            return usera
          else:  
             return None
          