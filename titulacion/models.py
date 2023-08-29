from django.db import models

#class EstadoLista(models.Model):
#    nro = models.IntegerField(null=True)


class Archivo(models.Model):
    rutaArchivo = models.ImageField(upload_to="archivos_excel/", null=True, blank=True)

    
class Situacion(models.Model):
    nomSituacion = models.TextField(max_length=20)


class Titulado(models.Model):
    rut = models.TextField(max_length=12)
    nombre = models.TextField(max_length=50)
    paterno = models.TextField(max_length=50)
    materno = models.TextField(max_length=50)
    carrera = models.TextField(max_length=100)
    mencion = models.TextField(max_length=50)
    sigla = models.TextField(max_length=50)
    fechaTitulacion = models.DateTimeField()
    yearTitulacion = models.IntegerField(null=False)
    situacion = models.ForeignKey(Situacion, on_delete=models.CASCADE, null=True)
    ninvitados = models.IntegerField(null=True)
    areaAcademica = models.TextField(max_length=255)
    

class SituacionFechasTitulado(models.Model):
    fechaTitulacion = models.DateTimeField()
    fechaTitulacionEstado = models.IntegerField(null=True)
    

class Tipo(models.Model):
    nomTipo = models.TextField(max_length=20)


class Estado(models.Model):
    nomEstado = models.TextField(max_length=20)


class Usuario(models.Model):
    rutUsuario = models.TextField(max_length=12)
    nomUsuario = models.TextField(max_length=20)
    apeUsuario = models.TextField(max_length=20)
    pasUsuario = models.TextField(max_length=20)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)


class Libreto(models.Model):
    iniLibreto = models.TextField()
    salLibreto = models.TextField()
    atrLibreto = models.TextField()
    finLibreto = models.TextField()
    terLibreto = models.TextField()
