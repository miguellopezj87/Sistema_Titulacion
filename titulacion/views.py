from django.shortcuts import render
from titulacion.models import Usuario, Tipo, Estado, Archivo, Titulado, SituacionFechasTitulado
from datetime import datetime
from django.db import connection
import json
import pandas
from os import system

cursor = connection.cursor()

#----------------------------------------------------------------------------------------------------------


def mostrarLogin(request):
    return render(request,'index.html')


#----------------------------------------------------------------------------------------------------------


def iniciarSesion(request):
    if request.method == "POST":
        rut = request.POST["txtrut"]
        pas = request.POST["txtpas"]
        
        val = (rut, pas, )
        sql = "select t.id, t.rutUsuario, t.nomUsuario, t.apeUsuario, t.pasUsuario, t.tipo_id, ti.nomTipo, t.estado_id from titulacion_usuario t, titulacion_tipo ti where t.tipo_id=ti.id and t.rutUsuario=%s and t.pasUsuario=%s"
        cursor.execute(sql, val)
        comprobarLogin = cursor.fetchall()
                     
        if len(comprobarLogin) != 0:
            if int(comprobarLogin[0][7]) == 1:
                idUsuario  = comprobarLogin[0][0]
                rutUsuario = comprobarLogin[0][1]
                nomUsuario = comprobarLogin[0][2]
                apeUsuario = comprobarLogin[0][3]
                pasUsuario = comprobarLogin[0][4]
                tipo_id    = comprobarLogin[0][5]
                nomTipo    = comprobarLogin[0][6]
                
                request.session["estadoSesion"] = True
                request.session["idUsuario"]  = idUsuario
                request.session["rutUsuario"] = rutUsuario
                request.session["nomUsuario"] = nomUsuario
                request.session["apeUsuario"] = apeUsuario
                request.session["pasUsuario"] = pasUsuario
                request.session["tipo_id"]    = tipo_id
                request.session["nomTipo"]    = nomTipo
                
                datos = {
                            "idUsuario"  : idUsuario,
                            "rutUsuario" : rutUsuario.upper(),
                            "nomUsuario" : nomUsuario.upper(),
                            "apeUsuario" : apeUsuario.upper(),
                            "nomTipo"    : nomTipo.upper()
                        }
                
                if comprobarLogin[0][5] == 1:
                    return render(request, 'menuAdmin.html', datos)
                elif comprobarLogin[0][5] == 2:
                    return render(request, 'menuAnfitrion.html', datos)
                elif comprobarLogin[0][5] == 3:
                    return render(request, 'menuLocutor.html', datos)
                elif comprobarLogin[0][5] == 4:
                    return render(request, 'menuOrganizador.html', datos)
            else:
                datos = { 'r2' : 'Usuario Deshabilitado. Comuníquese con el Admin!!' }
                return render(request, 'index.html', datos)
        else:
            datos = { 'r2' : 'Error De Usuario y/o Contraseña!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'No Se Puede Procesar La Solicitud!!' }
        return render(request, 'index.html', datos)


#----------------------------------------------------------------------------------------------------------


def cerrarSesion(request):
    try:
        del request.session['estadoSesion']
        del request.session['idUsuario']
        del request.session['rutUsuario']
        del request.session['nomUsuario']
        del request.session['apeUsuario']
        del request.session['pasUsuario']
        del request.session['tipo_id']
        del request.session['nomTipo']
        del request.session['estado_id']
        return render(request, 'index.html')
    except:
        return render(request, 'index.html')


#----------------------------------------------------------------------------------------------------------


def mostrarMenuAdmin(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["tipo_id"] == 1:
            datos = {
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper()
            }
            return render(request, 'menuAdmin.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Admin!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)


#----------------------------------------------------------------------------------------------------------


def mostrarFormRegistrarUsuario(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["tipo_id"] == 1:
            
            opcionesTipos = Tipo.objects.all().values().order_by("nomTipo")
            usu = Usuario.objects.select_related('tipo','estado')
            
            # --- Para la busqueda con Javascript ---
            lisbus = []
            for x in usu:
                lisbus.append({"id":x.id,"rutUsuario":x.rutUsuario,"nomUsuario":x.nomUsuario,"apeUsuario":x.apeUsuario,"tipo.nomTipo":x.tipo.nomTipo,"estado.nomEstado":x.estado.nomEstado})    
            lisbus2 = json.dumps(lisbus)
            lisbus3 = '{ "lisbus3" : '+lisbus2+'}'
            # ---------------------------------------
            
            datos = {
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
                'opcionesTipos' : opcionesTipos,
                'usu' : usu,
                'lisbus3' : lisbus3,
            }

            return render(request, 'form_reg_usu.html', datos)
            
        else:
            datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)


#----------------------------------------------------------------------------------------------------------


def registrarUsuario(request):
    if request.method == "POST":
        rut = request.POST["txtrut"]
        nom = request.POST["txtnom"]
        ape = request.POST["txtape"]
        pas = request.POST["txtpas"]
        tip = request.POST["cbotip"]

        comprobarRut = Usuario.objects.filter(rutUsuario=rut)
        if comprobarRut:
            opcionesTipos = Tipo.objects.all().values().order_by("id")
            opcionesEstados = Estado.objects.all().values().order_by("id")

            # --- Para la busqueda con Javascript ---
            usu = Usuario.objects.select_related('tipo','estado')
            lisbus = []
            for x in usu:
                lisbus.append({"id":x.id,"rutUsuario":x.rutUsuario,"nomUsuario":x.nomUsuario,"apeUsuario":x.apeUsuario,"tipo.nomTipo":x.tipo.nomTipo,"estado.nomEstado":x.estado.nomEstado})    
                lisbus2 = json.dumps(lisbus)
                lisbus3 = '{ "lisbus3" : '+lisbus2+'}'
            # ---------------------------------------
            
            datos = { 
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
                'opcionesTipos' : opcionesTipos,
                'opcionesEstados' : opcionesEstados,
                'rut' : rut,
                'nom' : nom,
                'ape' : ape,
                'pas' : pas,
                'tip' : int(tip),
                'r2' : 'El Rut de Usuario ('+rut.upper()+') Ya Existe!!',
                'usu' : usu,
                'lisbus3' : lisbus3,
            }
            
            return render(request, 'form_reg_usu.html', datos)
        
        else:
            u = Usuario(rutUsuario=rut, nomUsuario=nom, apeUsuario=ape, pasUsuario=pas, estado_id=1, tipo_id=tip)
            u.save()
            opcionesTipos = Tipo.objects.all().values().order_by("id")
            opcionesEstados = Estado.objects.all().values().order_by("id")
            
            # --- Para la busqueda con Javascript ---
            usu = Usuario.objects.select_related('tipo','estado')
            lisbus = []
            for x in usu:
                lisbus.append({"id":x.id,"rutUsuario":x.rutUsuario,"nomUsuario":x.nomUsuario,"apeUsuario":x.apeUsuario,"tipo.nomTipo":x.tipo.nomTipo,"estado.nomEstado":x.estado.nomEstado})    
                lisbus2 = json.dumps(lisbus)
                lisbus3 = '{ "lisbus3" : '+lisbus2+'}'
            # ---------------------------------------
            
            datos = { 
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
                'opcionesTipos' : opcionesTipos,
                'opcionesEstados' : opcionesEstados,
                'r' : 'Usuario ('+rut+') Registrado Correctamente!!',
                'usu' : usu,
                'lisbus3' : lisbus3,
            }
            return render(request, 'form_reg_usu.html', datos)
    else:
        opcionesTipos = Tipo.objects.all().values().order_by("id")
        opcionesEstados = Estado.objects.all().values().order_by("id")
        
        # --- Para la busqueda con Javascript ---
        usu = Usuario.objects.select_related('tipo','estado')
        lisbus = []
        for x in usu:
            lisbus.append({"id":x.id,"rutUsuario":x.rutUsuario,"nomUsuario":x.nomUsuario,"apeUsuario":x.apeUsuario,"tipo.nomTipo":x.tipo.nomTipo,"estado.nomEstado":x.estado.nomEstado})    
            lisbus2 = json.dumps(lisbus)
            lisbus3 = '{ "lisbus3" : '+lisbus2+'}'
        # ---------------------------------------
        
        datos = { 
            'nomUsuario' : request.session["nomUsuario"].upper(),
            'apeUsuario' : request.session["apeUsuario"].upper(),
            'nomTipo'    : request.session["nomTipo"].upper(),
            'opcionesTipos' : opcionesTipos,
            'opcionesEstados' : opcionesEstados,                
            'r2' : 'Debe Presionar El Botón Para Registrar Un Usuario!!',
            'usu' : usu,
            'lisbus3' : lisbus3,
        }
        return render(request, 'form_reg_usu.html', datos)


#----------------------------------------------------------------------------------------------------------


def mostrarFormActualizarUsuario(request, id):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            encontrado = Usuario.objects.get(id=id)
            opcionesTipos = Tipo.objects.all().values().order_by("id")
            opcionesEstados = Estado.objects.all().values().order_by("id")

            # --- Para la busqueda con Javascript ---
            usu = Usuario.objects.select_related('tipo','estado')
            lisbus = []
            for x in usu:
                lisbus.append({"id":x.id,"rutUsuario":x.rutUsuario,"nomUsuario":x.nomUsuario,"apeUsuario":x.apeUsuario,"tipo.nomTipo":x.tipo.nomTipo,"estado.nomEstado":x.estado.nomEstado})    
                lisbus2 = json.dumps(lisbus)
                lisbus3 = '{ "lisbus3" : '+lisbus2+'}'
            # ---------------------------------------
            
            datos = { 
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
                'encontrado' : encontrado,
                'opcionesTipos' : opcionesTipos,
                'opcionesEstados' : opcionesEstados,
                'usu' : usu,
                'lisbus3' : lisbus3,
            }
            
            return render(request, 'form_act_usu.html', datos)
        
        else:
            datos = { 'r' : 'Debe Iniciar Sesión Para Acceder!!' }
            return render(request, 'index.html', datos)
        
    except:
        opcionesTipos = Tipo.objects.all().values().order_by("id")
        opcionesEstados = Estado.objects.all().values().order_by("id")
        
        # --- Para la busqueda con Javascript ---
        usu = Usuario.objects.select_related('tipo','estado')
        lisbus = []
        for x in usu:
            lisbus.append({"id":x.id,"rutUsuario":x.rutUsuario,"nomUsuario":x.nomUsuario,"apeUsuario":x.apeUsuario,"tipo.nomTipo":x.tipo.nomTipo,"estado.nomEstado":x.estado.nomEstado})    
            lisbus2 = json.dumps(lisbus)
            lisbus3 = '{ "lisbus3" : '+lisbus2+'}'
        # ---------------------------------------
        
        datos = { 
            'nomUsuario' : request.session["nomUsuario"].upper(),
            'apeUsuario' : request.session["apeUsuario"].upper(),
            'nomTipo'    : request.session["nomTipo"].upper(),
            'opcionesTipos' : opcionesTipos,
            'opcionesEstados' : opcionesEstados,
            'r2' : "El ID ("+str(id)+") No Existe. Imposible Actualizar!!",
            'usu' : usu,
            'lisbus3' : lisbus3,
        }
        return render(request, 'form_reg_usu.html', datos)

#----------------------------------------------------------------------------------------------------------


def actualizarUsuario(request, id):
    try:
        rut = request.POST["txtrut"]
        nom = request.POST["txtnom"]
        ape = request.POST["txtape"]
        pas = request.POST["txtpas"]
        tip = request.POST["cbotip"]
        est = request.POST["cboest"]
        u = Usuario.objects.get(id=id)
        
        # Si el rut es el mismo o ya existe asociado a alguien más, no cambiará.
        todos = Usuario.objects.all().values().order_by("id")
        res = False
        for x in todos:
            if rut == x["rutUsuario"]:  res=True;  break;
        # Si el rut es uno nuevo, entonces sí se producirá el cambio.
        msg = ""
        if res == False:  u.rutUsuario=rut; msg="!!"
        else: msg=" (El Rut Se Mantiene Porque Ya Está En Uso)!!"
        #else: msg=" (El Rut Se Mantiene Igual Porque Está Asociado a Otro Usuario)!!"
                
        u.nomUsuario = nom
        u.apeUsuario = ape
        u.pasUsuario = pas
        u.tipo_id = tip
        u.estado_id = est
        u.save()

        opcionesTipos = Tipo.objects.all().values().order_by("id")
        opcionesEstados = Estado.objects.all().values().order_by("id")
        
        # --- Para la busqueda con Javascript ---
        usu = Usuario.objects.select_related('tipo','estado')
        lisbus = []
        for x in usu:
            lisbus.append({"id":x.id,"rutUsuario":x.rutUsuario,"nomUsuario":x.nomUsuario,"apeUsuario":x.apeUsuario,"tipo.nomTipo":x.tipo.nomTipo,"estado.nomEstado":x.estado.nomEstado})    
            lisbus2 = json.dumps(lisbus)
            lisbus3 = '{ "lisbus3" : '+lisbus2+'}'
        # ---------------------------------------
        
        datos = { 
            'nomUsuario' : request.session["nomUsuario"].upper(),
            'apeUsuario' : request.session["apeUsuario"].upper(),
            'nomTipo'    : request.session["nomTipo"].upper(),
            'opcionesTipos' : opcionesTipos,
            'opcionesEstados' : opcionesEstados,
            'r':"Datos Modificados Correctamente"+msg,
            'usu' : usu,
            'lisbus3' : lisbus3,
        }
        return render(request, 'form_reg_usu.html', datos)
    
    except:
        
        opcionesTipos = Tipo.objects.all().values().order_by("id")
        opcionesEstados = Estado.objects.all().values().order_by("id")
        
        # --- Para la busqueda con Javascript ---
        usu = Usuario.objects.select_related('tipo','estado')
        lisbus = []
        for x in usu:
            lisbus.append({"id":x.id,"rutUsuario":x.rutUsuario,"nomUsuario":x.nomUsuario,"apeUsuario":x.apeUsuario,"tipo.nomTipo":x.tipo.nomTipo,"estado.nomEstado":x.estado.nomEstado})    
            lisbus2 = json.dumps(lisbus)
            lisbus3 = '{ "lisbus3" : '+lisbus2+'}'
        # ---------------------------------------
        
        datos = {
            'nomUsuario' : request.session["nomUsuario"].upper(),
            'apeUsuario' : request.session["apeUsuario"].upper(),
            'nomTipo'    : request.session["nomTipo"].upper(),
            'opcionesTipos' : opcionesTipos,
            'opcionesEstados' : opcionesEstados,
            'r2' : "El ID ("+str(id)+") No Existe. Imposible Actualizar!!",
            'usu' : usu,
            'lisbus3' : lisbus3,
        }

        return render(request, 'form_reg_usu.html', datos)


#----------------------------------------------------------------------------------------------------------


def deshabilitarUsuario(request, id):
    try:
        u = Usuario.objects.get(id=id, estado_id=1)
        u.estado_id = 2
        u.save()

        opcionesTipos = Tipo.objects.all().values().order_by("id")
        opcionesEstados = Estado.objects.all().values().order_by("id")
        
        # --- Para la busqueda con Javascript ---
        usu = Usuario.objects.select_related('tipo','estado')
        lisbus = []
        for x in usu:
            lisbus.append({"id":x.id,"rutUsuario":x.rutUsuario,"nomUsuario":x.nomUsuario,"apeUsuario":x.apeUsuario,"tipo.nomTipo":x.tipo.nomTipo,"estado.nomEstado":x.estado.nomEstado})    
            lisbus2 = json.dumps(lisbus)
            lisbus3 = '{ "lisbus3" : '+lisbus2+'}'
        # ---------------------------------------
        
        datos = {
            'nomUsuario' : request.session["nomUsuario"].upper(),
            'apeUsuario' : request.session["apeUsuario"].upper(),
            'nomTipo'    : request.session["nomTipo"].upper(),
            'r' : "Usuario ('"+u.rutUsuario+"') Deshabilitado Correctamente!!",
            'opcionesTipos' : opcionesTipos,
            'opcionesEstados' : opcionesEstados,
            'usu' : usu,
            'lisbus3' : lisbus3
        }

        return render(request, "form_reg_usu.html", datos)

    except:
        opcionesTipos = Tipo.objects.all().values().order_by("id")
        opcionesEstados = Estado.objects.all().values().order_by("id")
        
        # --- Para la busqueda con Javascript ---
        usu = Usuario.objects.select_related('tipo','estado')
        lisbus = []
        for x in usu:
            lisbus.append({"id":x.id,"rutUsuario":x.rutUsuario,"nomUsuario":x.nomUsuario,"apeUsuario":x.apeUsuario,"tipo.nomTipo":x.tipo.nomTipo,"estado.nomEstado":x.estado.nomEstado})    
            lisbus2 = json.dumps(lisbus)
            lisbus3 = '{ "lisbus3" : '+lisbus2+'}'
        # ---------------------------------------
        
        datos = {
            'nomUsuario' : request.session["nomUsuario"].upper(),
            'apeUsuario' : request.session["apeUsuario"].upper(),
            'nomTipo'    : request.session["nomTipo"].upper(),
            'r2' : "El Usuario No Existe o ya ha Sido Deshabilitado!!",
            'opcionesTipos' : opcionesTipos,
            'opcionesEstados' : opcionesEstados,
            'usu' : usu,
            'lisbus3' : lisbus3,
        }

        return render(request, 'form_reg_usu.html', datos)


#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------


def cargarArchivo(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["tipo_id"] == 1:
            
            cursor.execute("select year(t.fechaTitulacion), count(year(t.fechaTitulacion)) from titulacion_titulado t group by year(t.fechaTitulacion) order by year(t.fechaTitulacion) desc")
            rs = cursor.fetchall()
            
            datos = {
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
                'pasUsuario' : request.session["pasUsuario"],
                'rs' : rs,
            }
            return render(request, 'cargar_archivo.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Admin!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)


#----------------------------------------------------------------------------------------------------------


def subirArchivo(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["tipo_id"] == 1:
            
            if request.method == 'POST':

                try:
                    
                    miArchivo = request.FILES['miArchivo']
                    arc = Archivo(rutaArchivo=miArchivo)
                    arc.save()
                    
                    #-------------------------------------
                    
                    cursor.execute("select * from titulacion_titulado")
                    rs = cursor.fetchall()
                    
                    i = 0; canrep=0; cannue=0; ft=0
                    
                    if len(rs)==0:
                                             
                        ruta = arc.rutaArchivo
                        datos_excel = pandas.read_excel(ruta)
                        df = pandas.DataFrame(datos_excel, columns=['Rut Alumno ', 'Apellido Paterno', 'Apellido Materno ', 'Nombre ', 'Unnamed: 9', 'Unnamed: 12', 'Sigla PE', 'Fecha Titulación', 'Área Académica'])
                        dd = df.to_dict('records')

                        fec = 0
                        for x in dd:
                            rut = x["Rut Alumno "]
                            pat = x["Apellido Paterno"]
                            mat = x["Apellido Materno "]
                            nom = x["Nombre "]
                            car = x["Unnamed: 9"]
                            men = x["Unnamed: 12"]
                            sig = x["Sigla PE"]
                            fec = x["Fecha Titulación"]
                            are = x["Área Académica"]
                            ft = fec.date().year
                                                        
                            tit = Titulado(rut=rut, nombre=nom, paterno=pat, materno=mat, carrera=car, mencion=men, sigla=sig, fechaTitulacion=fec, yearTitulacion=ft, ninvitados=0, areaAcademica=are)
                            tit.save()
                            cannue += 1
                            
                        sql = "select distinct(t.fechaTitulacion) from titulacion_titulado t order by t.fechaTitulacion asc"
                        cursor.execute(sql)
                        fechasDistintas = cursor.fetchall()
                                        
                        for x in fechasDistintas:
                            sql = "select count(t.fechaTitulacion) from titulacion_situacionfechastitulado t where t.fechaTitulacion=%s"
                            cursor.execute(sql, x[0])
                            rs = cursor.fetchone()
                            if rs[0] == 0:
                                ft = SituacionFechasTitulado(fechaTitulacion=x[0], fechaTitulacionEstado=1)
                                ft.save()
                            
                    else:
                        
                        ruta = arc.rutaArchivo
                        datos_excel = pandas.read_excel(ruta)
                        df = pandas.DataFrame(datos_excel, columns=['Rut Alumno ', 'Apellido Paterno', 'Apellido Materno ', 'Nombre ', 'Unnamed: 9', 'Unnamed: 12', 'Sigla PE', 'Fecha Titulación', 'Área Académica'])
                        dd = df.to_dict('records')
                        
                        for d in dd:
                            val = (d["Rut Alumno "], d["Nombre "], d["Apellido Paterno"], d["Apellido Materno "], d["Unnamed: 9"], d["Unnamed: 12"], d["Sigla PE"], d["Fecha Titulación"], d["Área Académica"])
                            sql = "select count(*) from titulacion_titulado t where t.rut=%s and t.nombre=%s and t.paterno=%s and t.materno=%s and t.carrera=%s and t.mencion=%s and t.sigla=%s and t.fechaTitulacion=%s and t.areaAcademica=%s"
                            cursor.execute(sql, val)
                            r = cursor.fetchone()
                            if r[0] == 0:
                                rut = d["Rut Alumno "]
                                pat = d["Apellido Paterno"]
                                mat = d["Apellido Materno "]
                                nom = d["Nombre "]
                                car = d["Unnamed: 9"]
                                men = d["Unnamed: 12"]
                                sig = d["Sigla PE"]
                                fec = d["Fecha Titulación"]
                                are = d["Área Académica"]
                                ft = fec.date().year
                                                            
                                tit = Titulado(rut=rut, nombre=nom, paterno=pat, materno=mat, carrera=car, mencion=men, sigla=sig, fechaTitulacion=fec, yearTitulacion=ft, ninvitados=0, areaAcademica=are)
                                tit.save()
                                cannue += 1
                            else:
                                canrep += 1
                                        
                        sql = "select distinct(t.fechaTitulacion) from titulacion_titulado t order by t.fechaTitulacion asc"
                        cursor.execute(sql)
                        fechasDistintas = cursor.fetchall()
                                        
                        for x in fechasDistintas:
                            sql = "select count(t.fechaTitulacion) from titulacion_situacionfechastitulado t where t.fechaTitulacion=%s"
                            cursor.execute(sql, x[0])
                            rs = cursor.fetchone()
                            if rs[0] == 0:
                                ft = SituacionFechasTitulado(fechaTitulacion=x[0], fechaTitulacionEstado=1)
                                ft.save()
                    
                    #-------------------------------------
                    
                    datos = { 
                            'nomUsuario' : request.session["nomUsuario"].upper(),
                            'apeUsuario' : request.session["apeUsuario"].upper(),
                            'nomTipo'    : request.session["nomTipo"].upper(),
                            'r' : 'Datos del Archivo Cargados Correctamente!!',
                            'ft':ft,
                            'cannue':cannue,
                            'canrep':canrep,
                            }
                    return render(request, 'cargar_archivo.html', datos)
                
                except:
                    datos = { 
                             'nomUsuario' : request.session["nomUsuario"].upper(),
                             'apeUsuario' : request.session["apeUsuario"].upper(),
                             'nomTipo'    : request.session["nomTipo"].upper(),
                             'r2' : 'No se Detectó Ningún Archivo Adjunto!!'
                            }
                    return render(request, 'cargar_archivo.html', datos)
                
            else:
                datos = { 'r2' : 'Solicitud no Procesada. No se Detectó Ningún Archivo Adjunto!!' }
                return render(request, 'cargar_archivo.html', datos)
            
        else:
            datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Admin!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)


#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------


def mostrarMenuAnfitrion(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["tipo_id"] == 2:
            datos = {
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
            }
            return render(request, 'menuAnfitrion.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Anfitrión!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)


#----------------------------------------------------------------------------------------------------------


def gestionarRecepcion(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["tipo_id"] == 2:

            cursor.execute("select year(t.fechaTitulacion), count(year(t.fechaTitulacion)) from titulacion_titulado t group by year(t.fechaTitulacion) order by year(t.fechaTitulacion) desc")
            rs = cursor.fetchall()
            datos = { 
                    'nomUsuario' : request.session["nomUsuario"].upper(),
                    'apeUsuario' : request.session["apeUsuario"].upper(),
                    'nomTipo'    : request.session["nomTipo"].upper(),
                    'rs' : rs,
                    }
            return render(request, 'gestionar_recepcion.html', datos)
            
        else:
            datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Anfitrión!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)


#----------------------------------------------------------------------------------------------------------


def gestionarRecepcionMensual(request, yearTitulacion):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            if request.session["tipo_id"] == 2:

                sql = "select month(t.fechaTitulacion), year(t.fechaTitulacion), count(year(t.fechaTitulacion)) from titulacion_titulado t where year(t.fechaTitulacion)=%s group by month(t.fechaTitulacion), year(t.fechaTitulacion)"
                cursor.execute(sql, yearTitulacion)
                rs = cursor.fetchall()
                
                if len(rs) != 0:
                    datos = {
                        'nomUsuario' : request.session["nomUsuario"].upper(),
                        'apeUsuario' : request.session["apeUsuario"].upper(),
                        'nomTipo'    : request.session["nomTipo"].upper(),
                        'rs' : rs,
                        }
                    return render(request, 'gestionar_recepcion_mensual.html', datos)
                else:
                    datos = {
                            'nomUsuario' : request.session["nomUsuario"].upper(),
                            'apeUsuario' : request.session["apeUsuario"].upper(),
                            'nomTipo'    : request.session["nomTipo"].upper(),
                            'r2' : 'Sin Registros Para Cargar!!',
                            }
                    return render(request, 'gestionar_recepcion_mensual.html', datos)
            else:
                datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Anfitrión!!' }
                return render(request, 'index.html', datos)
        else:
            datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
            return render(request, 'index.html', datos)
    except:
        datos = { 
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
                'r2' : 'Error al Procesar la Solicitud!!'
                }        
        return render(request, 'menu_anfitrion.html', datos)


#----------------------------------------------------------------------------------------------------------

def cargarTitulados(request, mes, yea):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            if request.session["tipo_id"] == 2:
                
                # --- Para la busqueda con Javascript ---
                
                val = (mes, yea)
                sql = "select distinct(t.fechaTitulacion), t.fechaTitulacionEstado from titulacion_situacionfechastitulado t where month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s order by t.fechaTitulacion asc"
                cursor.execute(sql, val)
                opcionesFechas = cursor.fetchall()
                
                listaOpcionesFechas = []
                for x in opcionesFechas:
                    if x[0].day>=1 and x[0].day<=9:
                        dia = str(0)+str(x[0].day)
                    else:
                        dia = x[0].day
                    if x[0].month>=1 and x[0].month<=9:
                        mes = str(0)+str(x[0].month)
                    else:
                        mes = x[0].month
                    año = x[0].year
                    if x[1] == 1:
                        fechasituacion = "(Abierta)"
                    elif x[1] == 2:
                        fechasituacion = "(Cerrada)"
                    fechanormal = str(dia)+"-"+str(mes)+"-"+str(año)
                    fechareves  = str(año)+"-"+str(mes)+"-"+str(dia)
                    listaOpcionesFechas.append({ "dia":dia, "mes":mes, "año":año, "fechanormal":fechanormal, "fechareves":fechareves, "fechasituacion":fechasituacion })
                
                val = (mes, yea)
                sql = "select count(*) from titulacion_situacionfechastitulado t where month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s"
                cursor.execute(sql, val)
                rs = cursor.fetchone()
                cantot = rs[0]
                sql = "select count(*) from titulacion_situacionfechastitulado t where month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s and t.fechaTitulacionEstado=1"
                cursor.execute(sql, val)
                rs = cursor.fetchone()
                canabi = rs[0]
                fechasitmes = ""
                if cantot == canabi:
                    #Cerrar Mes Seleccionado
                    fechasitmes = 1
                else:
                    #Abrir Mes Seleccionado
                    fechasitmes = 2            
                
                val = (mes, yea)
                sql = "select * from titulacion_titulado t where month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s order by t.fechaTitulacion desc"
                cursor.execute(sql, val)
                tit = cursor.fetchall()
                
                lisbus = []
                for x in tit:
                    if x[8].day>=1 and x[8].day<=9:
                        dia = str(0)+str(x[8].day)
                    else:
                        dia = str(x[8].day)
                    if x[8].month>=1 and x[8].month<=9:
                        mes = str(0)+str(x[8].month)
                    else:
                        mes = str(x[8].month)
                    año = x[8].year
                    fecha = str(dia)+"-"+str(mes)+"-"+str(año)
                    lisbus.append({"id":x[0],"rut":x[1],"nombre":x[2],"paterno":x[3],"materno":x[4],"carrera":x[5],"fechaTitulacion":fecha,"situacion_id":x[12],"ninvitados":x[10]})
                    lisbus2 = json.dumps(lisbus)
                    lisbus3 = '{ "lisbus3" : '+lisbus2+'}'
                
                datos = { 
                        'nomUsuario' : request.session["nomUsuario"].upper(),
                        'apeUsuario' : request.session["apeUsuario"].upper(),
                        'nomTipo'    : request.session["nomTipo"].upper(),
                        'tit' : tit,
                        'mes' : mes,
                        'yea' : yea,
                        'yearTitulacion' : yea,
                        'lisbus3' : lisbus3,
                        'listaOpcionesFechas' : listaOpcionesFechas,
                        'fechasitmes': fechasitmes,
                        }
                return render(request, 'gestionar_titulados.html', datos)
                
            else:
                datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Anfitrión!!' }
                return render(request, 'index.html', datos)
        else:
            datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
            return render(request, 'index.html', datos)
    except:
        datos = { 
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
                'r2' : 'Error al Procesar Solicitud!!'
                }
        return render(request, 'menuAnfitrion.html', datos)


#----------------------------------------------------------------------------------------------------------


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def guardar_asistencia_titulados(request, ide, mes, yea, sit, ninv, ff, msgerror):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            if request.session["tipo_id"] == 2:
                
                if int(ninv)<0 or int(ninv)>2:
                        datos = {
                        'nomUsuario' : request.session["nomUsuario"].upper(),
                        'apeUsuario' : request.session["apeUsuario"].upper(),
                        'nomTipo'    : request.session["nomTipo"].upper(),
                        'r2' : 'Error al Procesar la Solicitud!!'
                        }
                        return render(request, 'menuAnfitrion.html', datos)
                
                if msgerror=="x":
                    msgerror = ""
                res = ""
                
                mensajeAtraso = ""
                
                if msgerror == "":
                    if ff == "allmydata":
                        sql = "select t.fechaTitulacionEstado from titulacion_situacionfechastitulado t where t.fechaTitulacion=(select tt.fechaTitulacion from titulacion_titulado tt where tt.id=%s)"
                        cursor.execute(sql, ide)
                        rs = cursor.fetchone()
                        
                        if rs[0]==1:
                            sst = 1
                        elif rs[0]==2:
                            sst = 3
                            mensajeAtraso = "INGRESO COMO ATRASADO"
                    else:
                        dd = str(ff[0:2])
                        mm = str(ff[3:5])
                        yy = str(ff[6:10])
                        fr = str(yy)+"-"+str(mm)+"-"+str(dd)
                    
                        sql = "select fechaTitulacionEstado from titulacion_situacionfechastitulado t where t.fechaTitulacion=%s"
                        cursor.execute(sql, fr)
                        rs = cursor.fetchone()
                        
                        if rs[0]==1:
                            sst = 1
                        elif rs[0]==2:
                            sst = 3
                            mensajeAtraso = "INGRESO COMO ATRASADO"
                    
                    sql = "update titulacion_titulado set titulacion_titulado.situacion_id=%s, titulacion_titulado.ninvitados=%s where titulacion_titulado.id=%s"
                    if int(sit)==1:
                        val = (sst, ninv, ide)
                        cursor.execute(sql, val)
                        connection.commit()
                    elif int(sit)==2:
                        mensajeAtraso = "ESTUDIANTE SIN ASISTENCIA"
                        val = (None, ninv, ide)
                        cursor.execute(sql, val)
                        connection.commit()
                    
                    if mensajeAtraso == "":
                        res = "INFORMACION INGRESADA"
                    
                if msgerror == "El Nro de Invitados Debe Estar 0 y 1.":
                    msgerror = "El Nro de Invitados Debe Estar Entre 0 y 2"
                
                # --- Para la busqueda con Javascript ---
                
                val = (mes, yea)
                sql = "select distinct(t.fechaTitulacion), t.fechaTitulacionEstado from titulacion_situacionfechastitulado t where month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s order by t.fechaTitulacion asc"
                cursor.execute(sql, val)
                opcionesFechas = cursor.fetchall()
                
                listaOpcionesFechas = []
                for x in opcionesFechas:
                    if x[0].day>=1 and x[0].day<=9:
                        dia = str(0)+str(x[0].day)
                    else:
                        dia = x[0].day
                    if x[0].month>=1 and x[0].month<=9:
                        mes = str(0)+str(x[0].month)
                    else:
                        mes = x[0].month
                    año = x[0].year
                    if x[1] == 1:
                        fechasituacion = "(Abierta)"
                    elif x[1] == 2:
                        fechasituacion = "(Cerrada)"
                    fechanormal = str(dia)+"-"+str(mes)+"-"+str(año)
                    fechareves  = str(año)+"-"+str(mes)+"-"+str(dia)
                    listaOpcionesFechas.append({ "dia":dia, "mes":mes, "año":año, "fechanormal":fechanormal, "fechareves":fechareves, "fechasituacion":fechasituacion })
                            
                val = (mes, yea)
                sql = "select * from titulacion_titulado t where month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s order by t.fechaTitulacion desc"
                cursor.execute(sql, val)
                tit = cursor.fetchall()
                
                lisbus = []
                for x in tit:
                    if x[0]==int(ide):
                        n = str(x[3])+" "+str(x[4])+" "+str(x[2])
                    if x[8].day>=1 and x[8].day<=9:
                        dia = str(0)+str(x[8].day)
                    else:
                        dia = str(x[8].day)
                    if x[8].month>=1 and x[8].month<=9:
                        mes = str(0)+str(x[8].month)
                    else:
                        mes = str(x[8].month)
                    año = x[8].year
                    fecha = str(dia)+"-"+str(mes)+"-"+str(año)
                    lisbus.append({"id":x[0],"rut":x[1],"nombre":x[2],"paterno":x[3],"materno":x[4],"carrera":x[5],"fechaTitulacion":fecha,"situacion_id":x[12],"ninvitados":x[10]})
                    lisbus2 = json.dumps(lisbus)
                    lisbus3 = '{ "lisbus3" : '+lisbus2+'}'
                    
                # ---------------------------------------
                
                datos = { 
                        'nomUsuario' : request.session["nomUsuario"].upper(),
                        'apeUsuario' : request.session["apeUsuario"].upper(),
                        'nomTipo'    : request.session["nomTipo"].upper(),
                        'tit' : tit,
                        'ide' : ide,
                        'mes' : mes,
                        'yea' : yea,
                        'yearTitulacion' : yea,
                        'lisbus3' : lisbus3,
                        'sit' : sit,
                        'ninv': ninv,
                        'res' : res,
                        'msgerror' : msgerror,
                        'mensajeAtraso' : mensajeAtraso,
                        'n' : n,
                        'ff' : ff,
                        'listaOpcionesFechas' : listaOpcionesFechas,
                        }
                return render(request, 'gestionar_titulados.html', datos)
            else:
                datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Anfitrión!!' }
                return render(request, 'index.html', datos)
        else:
            datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
            return render(request, 'index.html', datos)
    except:
        datos = {
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
                'r2' : 'Error al Procesar la Solicitud!!'
                }
        return render(request, 'menuAnfitrion.html', datos)


#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------


def gestionarRecepcionMenAdm(request, yearTitulacion):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            if request.session["tipo_id"] == 1:

                sql = "select month(t.fechaTitulacion), year(t.fechaTitulacion), count(year(t.fechaTitulacion)) from titulacion_titulado t where year(t.fechaTitulacion)=%s group by month(t.fechaTitulacion), year(t.fechaTitulacion)"
                cursor.execute(sql, yearTitulacion)
                rs = cursor.fetchall()
                
                if len(rs) != 0:
                    datos = {
                            'nomUsuario' : request.session["nomUsuario"].upper(),
                            'apeUsuario' : request.session["apeUsuario"].upper(),
                            'nomTipo'    : request.session["nomTipo"].upper(),
                            'rs' : rs,
                            }
                    return render(request, 'gestionar_recepcion_menadm.html', datos)
                else:
                    datos = {
                            'nomUsuario' : request.session["nomUsuario"].upper(),
                            'apeUsuario' : request.session["apeUsuario"].upper(),
                            'nomTipo'    : request.session["nomTipo"].upper(),
                            'r2' : 'Sin Registros Para Cargar!!',
                            }
                    return render(request, 'gestionar_recepcion_menadm.html', datos)
            else:
                datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Anfitrión!!' }
                return render(request, 'index.html', datos)
        else:
            datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
            return render(request, 'index.html', datos)
    except:
        datos = { 
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
                'r2' : 'Error al Procesar Solicitud!!'
                }
        return render(request, 'menuAdmin.html', datos)


#----------------------------------------------------------------------------------------------------------


def cargarTituladosAdm(request, mes, yea):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            if request.session["tipo_id"] == 1:
                
                # --- Para la busqueda con Javascript ---
                
                val = (mes, yea)
                sql = "select distinct(t.fechaTitulacion), t.fechaTitulacionEstado from titulacion_situacionfechastitulado t where month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s order by t.fechaTitulacion asc"
                cursor.execute(sql, val)
                opcionesFechas = cursor.fetchall()
                
                listaOpcionesFechas = []
                for x in opcionesFechas:
                    if x[0].day>=1 and x[0].day<=9:
                        dia = str(0)+str(x[0].day)
                    else:
                        dia = x[0].day
                    if x[0].month>=1 and x[0].month<=9:
                        mes = str(0)+str(x[0].month)
                    else:
                        mes = x[0].month
                    año = x[0].year
                    if x[1] == 1:
                        fechasituacion = "(Abierta)"
                    elif x[1] == 2:
                        fechasituacion = "(Cerrada)"
                    fechanormal = str(dia)+"-"+str(mes)+"-"+str(año)
                    fechareves  = str(año)+"-"+str(mes)+"-"+str(dia)
                    listaOpcionesFechas.append({ "dia":dia, "mes":mes, "año":año, "fechanormal":fechanormal, "fechareves":fechareves, "fechasituacion":fechasituacion })
                
                val = (mes, yea)
                sql = "select count(*) from titulacion_situacionfechastitulado t where month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s"
                cursor.execute(sql, val)
                rs = cursor.fetchone()
                cantot = rs[0]
                sql = "select count(*) from titulacion_situacionfechastitulado t where month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s and t.fechaTitulacionEstado=1"
                cursor.execute(sql, val)
                rs = cursor.fetchone()
                canabi = rs[0]
                fechasitmes = ""
                if cantot == canabi:
                    fechasitmes = 1     #Cerrar Mes Seleccionado
                else:
                    fechasitmes = 2     #Abrir Mes Seleccionado
                
                val = (mes, yea)
                sql = "select * from titulacion_titulado t where month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s order by t.fechaTitulacion desc"
                cursor.execute(sql, val)
                tit = cursor.fetchall()
                
                lisbus = []
                for x in tit:
                    if x[8].day>=1 and x[8].day<=9:
                        dia = str(0)+str(x[8].day)
                    else:
                        dia = str(x[8].day)
                    if x[8].month>=1 and x[8].month<=9:
                        mes = str(0)+str(x[8].month)
                    else:
                        mes = str(x[8].month)
                    año = x[8].year
                    fecha = str(dia)+"-"+str(mes)+"-"+str(año)
                    lisbus.append({"id":x[0],"rut":x[1],"nombre":x[2],"paterno":x[3],"materno":x[4],"carrera":x[5],"fechaTitulacion":fecha,"situacion_id":x[12],"ninvitados":x[10]})
                    lisbus2 = json.dumps(lisbus)
                    lisbus3 = '{ "lisbus3" : '+lisbus2+'}'
                
                datos = { 
                        'nomUsuario' : request.session["nomUsuario"].upper(),
                        'apeUsuario' : request.session["apeUsuario"].upper(),
                        'nomTipo'    : request.session["nomTipo"].upper(),
                        'tit' : tit,
                        'mes' : mes,
                        'yea' : yea,
                        'yearTitulacion' : yea,
                        'lisbus3' : lisbus3,
                        'listaOpcionesFechas' : listaOpcionesFechas,
                        'fechasitmes': fechasitmes,
                        }
                return render(request, 'gestionar_titulados_adm.html', datos)
                
            else:
                datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Admin!!' }
                return render(request, 'index.html', datos)
        else:
            datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
            return render(request, 'index.html', datos)
    
    except:
        datos = { 
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
                'r2' : 'Error al Procesar Solicitud!!'
                }
        return render(request, 'menuAdmin.html', datos)


#----------------------------------------------------------------------------------------------------------


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def guardar_asistencia_titulados_adm(request, ide, mes, yea, sit, ninv, ff, msgerror):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            if request.session["tipo_id"] == 1:
                
                if int(ninv)<0 or int(ninv)>2:
                    datos = { 
                    'nomUsuario' : request.session["nomUsuario"].upper(),
                    'apeUsuario' : request.session["apeUsuario"].upper(),
                    'nomTipo'    : request.session["nomTipo"].upper(),
                    'r2' : 'Error al Procesar la Solicitud!!'
                    }        
                    return render(request, 'menuAdmin.html', datos)
                                        
                if msgerror=="x":
                    msgerror = ""
                res = ""
                
                mensajeAtraso = ""
                
                if msgerror == "":
                    if ff == "allmydata":
                        sql = "select t.fechaTitulacionEstado from titulacion_situacionfechastitulado t where t.fechaTitulacion=(select tt.fechaTitulacion from titulacion_titulado tt where tt.id=%s)"
                        cursor.execute(sql, ide)
                        rs = cursor.fetchone()
                        
                        if rs[0]==1:
                            sst = 1
                        elif rs[0]==2:
                            sst = 3
                            mensajeAtraso = "INGRESO COMO ATRASADO"
                    else:
                        dd = str(ff[0:2])
                        mm = str(ff[3:5])
                        yy = str(ff[6:10])
                        fr = str(yy)+"-"+str(mm)+"-"+str(dd)
                    
                        sql = "select fechaTitulacionEstado from titulacion_situacionfechastitulado t where t.fechaTitulacion=%s"
                        cursor.execute(sql, fr)
                        rs = cursor.fetchone()
                        
                        if rs[0]==1:
                            sst = 1
                        elif rs[0]==2:
                            sst = 3
                            mensajeAtraso = "INGRESO COMO ATRASADO"
                    
                    sql = "update titulacion_titulado set titulacion_titulado.situacion_id=%s, titulacion_titulado.ninvitados=%s where titulacion_titulado.id=%s"
                    if int(sit)==1:
                        val = (sst, ninv, ide)
                        cursor.execute(sql, val)
                        connection.commit()
                    elif int(sit)==2:
                        mensajeAtraso = "ESTUDIANTE SIN ASISTENCIA"
                        val = (None, ninv, ide)
                        cursor.execute(sql, val)
                        connection.commit()
                    
                    if mensajeAtraso == "":
                        res = "INFORMACION INGRESADA"
                
                if msgerror == "El Nro de Invitados Debe Estar 0 y 1.":
                    msgerror = "El Nro de Invitados Debe Estar Entre 0 y 2"
                
                # --- Para la busqueda con Javascript ---
                
                val = (mes, yea)
                sql = "select distinct(t.fechaTitulacion), t.fechaTitulacionEstado from titulacion_situacionfechastitulado t where month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s order by t.fechaTitulacion asc"
                cursor.execute(sql, val)
                opcionesFechas = cursor.fetchall()
                
                listaOpcionesFechas = []
                for x in opcionesFechas:
                    if x[0].day>=1 and x[0].day<=9:
                        dia = str(0)+str(x[0].day)
                    else:
                        dia = x[0].day
                    if x[0].month>=1 and x[0].month<=9:
                        mes = str(0)+str(x[0].month)
                    else:
                        mes = x[0].month
                    año = x[0].year
                    if x[1] == 1:
                        fechasituacion = "(Abierta)"
                    elif x[1] == 2:
                        fechasituacion = "(Cerrada)"
                    fechanormal = str(dia)+"-"+str(mes)+"-"+str(año)
                    fechareves  = str(año)+"-"+str(mes)+"-"+str(dia)
                    listaOpcionesFechas.append({ "dia":dia, "mes":mes, "año":año, "fechanormal":fechanormal, "fechareves":fechareves, "fechasituacion":fechasituacion })
                        
                val = (mes, yea)
                sql = "select * from titulacion_titulado t where month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s order by t.fechaTitulacion desc"
                cursor.execute(sql, val)
                tit = cursor.fetchall()
                
                lisbus = []
                for x in tit:
                    if x[0]==int(ide):
                        n = str(x[3])+" "+str(x[4])+" "+str(x[2])
                    if x[8].day>=1 and x[8].day<=9:
                        dia = str(0)+str(x[8].day)
                    else:
                        dia = str(x[8].day)
                    if x[8].month>=1 and x[8].month<=9:
                        mes = str(0)+str(x[8].month)
                    else:
                        mes = str(x[8].month)
                    año = x[8].year
                    fecha = str(dia)+"-"+str(mes)+"-"+str(año)
                    lisbus.append({"id":x[0],"rut":x[1],"nombre":x[2],"paterno":x[3],"materno":x[4],"carrera":x[5],"fechaTitulacion":fecha,"situacion_id":x[12],"ninvitados":x[10]})
                    lisbus2 = json.dumps(lisbus)
                    lisbus3 = '{ "lisbus3" : '+lisbus2+'}'
                
                # ---------------------------------------
                
                datos = { 
                        'nomUsuario' : request.session["nomUsuario"].upper(),
                        'apeUsuario' : request.session["apeUsuario"].upper(),
                        'nomTipo'    : request.session["nomTipo"].upper(),
                        'tit' : tit,
                        'ide' : ide,
                        'mes':mes,
                        'yea':yea,
                        'yearTitulacion' : yea,
                        'lisbus3' : lisbus3,
                        'sit' : sit,
                        'ninv' : ninv,
                        'res' : res,
                        'msgerror' : msgerror,
                        'mensajeAtraso' : mensajeAtraso,
                        'n' : n,
                        'ff' : ff,
                        'listaOpcionesFechas' : listaOpcionesFechas,
                        }
                
                return render(request, 'gestionar_titulados_adm.html', datos)
                
            else:
                datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Admin!!' }
                return render(request, 'index.html', datos)
        else:
            datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
            return render(request, 'index.html', datos)
    except:
        datos = { 
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
                'r2' : 'Error al Procesar la Solicitud!!'
                }        
        return render(request, 'menuAdmin.html', datos)


#----------------------------------------------------------------------------------------------------------


def cambiar_estado_fecha_adm(request, ff, op):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            if request.session["tipo_id"] == 1:
                
                dia = ff[0:2]
                mes = ff[3:5]
                yea = ff[6:10]
                ffreves = str(yea)+"-"+str(mes)+"-"+str(dia)
                
                val = (op, ffreves)
                sql = "update titulacion_situacionfechastitulado t set t.fechaTitulacionEstado=%s where t.fechaTitulacion=%s"
                cursor.execute(sql, val)
                connection.commit()
                
                # --- Para la busqueda con Javascript ---
                
                val = (mes, yea)
                sql = "select distinct(t.fechaTitulacion), t.fechaTitulacionEstado from titulacion_situacionfechastitulado t where month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s order by t.fechaTitulacion asc"
                cursor.execute(sql, val)
                opcionesFechas = cursor.fetchall()
                
                listaOpcionesFechas = []
                for x in opcionesFechas:
                    if x[0].day>=1 and x[0].day<=9:
                        dia = str(0)+str(x[0].day)
                    else:
                        dia = x[0].day
                    if x[0].month>=1 and x[0].month<=9:
                        mes = str(0)+str(x[0].month)
                    else:
                        mes = x[0].month
                    año = x[0].year
                    if x[1] == 1:
                        fechasituacion = "(Abierta)"
                    elif x[1] == 2:
                        fechasituacion = "(Cerrada)"
                    fechanormal = str(dia)+"-"+str(mes)+"-"+str(año)
                    fechareves  = str(año)+"-"+str(mes)+"-"+str(dia)
                    listaOpcionesFechas.append({ "dia":dia, "mes":mes, "año":año, "fechanormal":fechanormal, "fechareves":fechareves, "fechasituacion":fechasituacion })
                
                val = (mes, yea)
                sql = "select count(*) from titulacion_situacionfechastitulado t where month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s"
                cursor.execute(sql, val)
                rs = cursor.fetchone()
                cantot = rs[0]
                sql = "select count(*) from titulacion_situacionfechastitulado t where month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s and t.fechaTitulacionEstado=1"
                cursor.execute(sql, val)
                rs = cursor.fetchone()
                canabi = rs[0]
                fechasitmes = ""
                if cantot == canabi:
                    fechasitmes = 1     #Cerrar Mes Seleccionado
                else:
                    fechasitmes = 2     #Abrir Mes Seleccionado
                
                val = (mes, yea)
                sql = "select * from titulacion_titulado t where month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s order by t.fechaTitulacion desc"
                cursor.execute(sql, val)
                tit = cursor.fetchall()
                
                lisbus = []
                for x in tit:
                    if x[8].day>=1 and x[8].day<=9:
                        dia = str(0)+str(x[8].day)
                    else:
                        dia = str(x[8].day)
                    if x[8].month>=1 and x[8].month<=9:
                        mes = str(0)+str(x[8].month)
                    else:
                        mes = str(x[8].month)
                    año = x[8].year
                    fecha = str(dia)+"-"+str(mes)+"-"+str(año)
                    lisbus.append({"id":x[0],"rut":x[1],"nombre":x[2],"paterno":x[3],"materno":x[4],"carrera":x[5],"fechaTitulacion":fecha,"situacion_id":x[12],"ninvitados":x[10]})
                    lisbus2 = json.dumps(lisbus)
                    lisbus3 = '{ "lisbus3" : '+lisbus2+'}'
                
                datos = { 
                        'nomUsuario' : request.session["nomUsuario"].upper(),
                        'apeUsuario' : request.session["apeUsuario"].upper(),
                        'nomTipo'    : request.session["nomTipo"].upper(),
                        'tit' : tit,
                        'mes' : mes,
                        'yea' : yea,
                        'yearTitulacion' : yea,
                        'lisbus3' : lisbus3,
                        'listaOpcionesFechas' : listaOpcionesFechas,
                        'fechasitmes' : fechasitmes,
                        'ff' : ff,
                        }
                
                return render(request, 'gestionar_titulados_adm.html', datos)
                
            else:
                datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Admin!!' }
                return render(request, 'index.html', datos)
        else:
            datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
            return render(request, 'index.html', datos)
    except:
        datos = { 
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
                'r2' : 'Error al Procesar Solicitud!!'
                }
        return render(request, 'menuAdmin.html', datos)


#----------------------------------------------------------------------------------------------------------


def cambiar_estado_mes_adm(request, mes, yea, op):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["tipo_id"] == 1:
            
            val = (op, mes, yea)
            sql = "update titulacion_situacionfechastitulado t set t.fechaTitulacionEstado=%s where month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s"
            cursor.execute(sql, val)
            connection.commit()          
            
            # --- Para la busqueda con Javascript ---
            
            val = (mes, yea)
            sql = "select distinct(t.fechaTitulacion), t.fechaTitulacionEstado from titulacion_situacionfechastitulado t where month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s order by t.fechaTitulacion asc"
            cursor.execute(sql, val)
            opcionesFechas = cursor.fetchall()
            
            listaOpcionesFechas = []
            for x in opcionesFechas:
                if x[0].day>=1 and x[0].day<=9:
                    dia = str(0)+str(x[0].day)
                else:
                    dia = x[0].day
                if x[0].month>=1 and x[0].month<=9:
                    mes = str(0)+str(x[0].month)
                else:
                    mes = x[0].month
                año = x[0].year
                if x[1] == 1:
                    fechasituacion = "(Abierta)"
                elif x[1] == 2:
                    fechasituacion = "(Cerrada)"
                fechanormal = str(dia)+"-"+str(mes)+"-"+str(año)
                fechareves  = str(año)+"-"+str(mes)+"-"+str(dia)
                listaOpcionesFechas.append({ "dia":dia, "mes":mes, "año":año, "fechanormal":fechanormal, "fechareves":fechareves, "fechasituacion":fechasituacion })
            
            val = (mes, yea)
            sql = "select count(*) from titulacion_situacionfechastitulado t where month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s"
            cursor.execute(sql, val)
            rs = cursor.fetchone()
            cantot = rs[0]
            sql = "select count(*) from titulacion_situacionfechastitulado t where month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s and t.fechaTitulacionEstado=1"
            cursor.execute(sql, val)
            rs = cursor.fetchone()
            canabi = rs[0]
            fechasitmes = ""
            if cantot == canabi:
                fechasitmes = 1     #Cerrar Mes Seleccionado
            else:
                fechasitmes = 2     #Abrir Mes Seleccionado
            
            val = (mes, yea)
            sql = "select * from titulacion_titulado t where month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s order by t.fechaTitulacion desc"
            cursor.execute(sql, val)
            tit = cursor.fetchall()
            
            lisbus = []
            for x in tit:
                if x[8].day>=1 and x[8].day<=9:
                    dia = str(0)+str(x[8].day)
                else:
                    dia = str(x[8].day)
                if x[8].month>=1 and x[8].month<=9:
                    mes = str(0)+str(x[8].month)
                else:
                    mes = str(x[8].month)
                año = x[8].year
                fecha = str(dia)+"-"+str(mes)+"-"+str(año)
                lisbus.append({"id":x[0],"rut":x[1],"nombre":x[2],"paterno":x[3],"materno":x[4],"carrera":x[5],"fechaTitulacion":fecha,"situacion_id":x[12],"ninvitados":x[10]})
                lisbus2 = json.dumps(lisbus)
                lisbus3 = '{ "lisbus3" : '+lisbus2+'}'
            
            datos = { 
                    'nomUsuario' : request.session["nomUsuario"].upper(),
                    'apeUsuario' : request.session["apeUsuario"].upper(),
                    'nomTipo'    : request.session["nomTipo"].upper(),
                    'tit' : tit,
                    'mes' : mes,
                    'yea' : yea,
                    'yearTitulacion' : yea,
                    'lisbus3' : lisbus3,
                    'listaOpcionesFechas' : listaOpcionesFechas,
                    'fechasitmes' : fechasitmes,
                    'ff' : "allmydata",
                    }
            
            return render(request, 'gestionar_titulados_adm.html', datos)
            
        else:
            datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Admin!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)


#----------------------------------------------------------------------------------------------------------


def mostrarMenuOrganizador(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["tipo_id"] == 4:
            datos = {
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper()
            }
            return render(request, 'menuOrganizador.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Organizador de Diplomas!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)


#----------------------------------------------------------------------------------------------------------


def delete_year_adm(request, year, pasw):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["tipo_id"] == 1:
            pasusu = request.session["pasUsuario"]
            if pasw==pasusu:
                sql = "delete from titulacion_titulado where year(fechaTitulacion)=%s"
                cursor.execute(sql, year)
                connection.commit()
                sql = "delete from titulacion_situacionfechastitulado where year(fechaTitulacion)=%s"
                cursor.execute(sql, year)
                connection.commit()
                sql = "select count(*) from titulacion_titulado"
                cursor.execute(sql)
                ttb = cursor.fetchone()
                if ttb[0]==0:
                    sql = "truncate table titulacion_titulado"
                    cursor.execute(sql)
                    sql = "truncate table titulacion_situacionfechastitulado"
                    cursor.execute(sql)
                tipoMsg = "success"
                textoMsg = "REGISTROS DEL AÑO "+year+" ELIMINADOS CORRECTAMENTE!!"
            else:
                tipoMsg = "error"
                textoMsg = "ERRO DE CONTRASEÑA. ELIMINACIÓN NO REALIZADA!!"
            
            cursor.execute("select year(t.fechaTitulacion), count(year(t.fechaTitulacion)) from titulacion_titulado t group by year(t.fechaTitulacion) order by year(t.fechaTitulacion) desc")
            rs = cursor.fetchall()
            
            datos = {
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
                'rs' : rs,
                'tipoMsg' : tipoMsg,
                'textoMsg' : textoMsg,
            }
            return render(request, 'cargar_archivo.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Admin!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder al Sistema!!' }
        return render(request, 'index.html', datos)


#----------------------------------------------------------------------------------------------------------


def gestionar_recepcion_org(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["tipo_id"] == 4:

            cursor.execute("select year(t.fechaTitulacion), count(year(t.fechaTitulacion)) from titulacion_titulado t group by year(t.fechaTitulacion) order by year(t.fechaTitulacion) desc")
            rs = cursor.fetchall()
            datos = { 
                    'nomUsuario' : request.session["nomUsuario"].upper(),
                    'apeUsuario' : request.session["apeUsuario"].upper(),
                    'nomTipo'    : request.session["nomTipo"].upper(),
                    'rs' : rs,
                    }
            return render(request, 'gestionar_recepcion_org.html', datos)
            
        else:
            datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Anfitrión!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)


#----------------------------------------------------------------------------------------------------------


def gestionar_recepcion_menorg(request, yearTitulacion):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            if request.session["tipo_id"] == 4:
                
                sql = "select month(t.fechaTitulacion), year(t.fechaTitulacion), count(year(t.fechaTitulacion)) from titulacion_titulado t where year(t.fechaTitulacion)=%s group by month(t.fechaTitulacion), year(t.fechaTitulacion)"
                cursor.execute(sql, yearTitulacion)
                rs = cursor.fetchall()
                
                if len(rs) != 0:
                    datos = {
                            'nomUsuario' : request.session["nomUsuario"].upper(),
                            'apeUsuario' : request.session["apeUsuario"].upper(),
                            'nomTipo'    : request.session["nomTipo"].upper(),
                            'rs' : rs,
                            }
                    return render(request, 'gestionar_recepcion_menorg.html', datos)
                else:
                    datos = {
                            'nomUsuario' : request.session["nomUsuario"].upper(),
                            'apeUsuario' : request.session["apeUsuario"].upper(),
                            'nomTipo'    : request.session["nomTipo"].upper(),
                            'r2' : 'Sin Registros Para Cargar!!',
                            }
                    return render(request, 'gestionar_recepcion_menorg.html', datos)
            else:
                datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Organizador!!' }
                return render(request, 'index.html', datos)
        else:
            datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
            return render(request, 'index.html', datos)
    except:
        datos = { 
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
                'r2' : 'Error al Procesar Solicitud!!'
                }
        return render(request, 'menuOrganizador.html', datos)


#----------------------------------------------------------------------------------------------------------


def cargarTituladosOrg(request, mes, yea):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            if request.session["tipo_id"] == 4:
                            
                # --- Para la busqueda con Javascript ---
                
                val = (mes, yea)
                sql = "select distinct(t.fechaTitulacion), t.fechaTitulacionEstado from titulacion_situacionfechastitulado t, titulacion_titulado z where t.fechaTitulacion=z.fechaTitulacion and month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s and z.situacion_id is not null order by t.fechaTitulacion asc"
                cursor.execute(sql, val)
                opcionesFechas = cursor.fetchall()
                
                listaOpcionesFechas = []
                for x in opcionesFechas:
                    if x[0].day>=1 and x[0].day<=9:
                        dia = str(0)+str(x[0].day)
                    else:
                        dia = x[0].day
                    if x[0].month>=1 and x[0].month<=9:
                        mes = str(0)+str(x[0].month)
                    else:
                        mes = x[0].month
                    año = x[0].year
                    if x[1] == 1:
                        fechasituacion = "(Abierta)"
                    elif x[1] == 2:
                        fechasituacion = "(Cerrada)"
                    fechanormal = str(dia)+"-"+str(mes)+"-"+str(año)
                    fechareves  = str(año)+"-"+str(mes)+"-"+str(dia)
                    listaOpcionesFechas.append({ "dia":dia, "mes":mes, "año":año, "fechanormal":fechanormal, "fechareves":fechareves, "fechasituacion":fechasituacion })
                    
                val = (mes, yea)
                sql = "select * from titulacion_titulado t where month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s order by t.fechaTitulacion desc"
                cursor.execute(sql, val)
                tit = cursor.fetchall()
                
                lisbus = []
                for x in tit:
                    if x[8].day>=1 and x[8].day<=9:
                        dia = str(0)+str(x[8].day)
                    else:
                        dia = str(x[8].day)
                    if x[8].month>=1 and x[8].month<=9:
                        mes = str(0)+str(x[8].month)
                    else:
                        mes = str(x[8].month)
                    año = x[8].year
                    fecha = str(dia)+"-"+str(mes)+"-"+str(año)
                    lisbus.append({"id":x[0],"rut":x[1],"nombre":x[2],"paterno":x[3],"materno":x[4],"carrera":x[5],"fechaTitulacion":fecha,"situacion_id":x[12],"ninvitados":x[10]})
                    lisbus2 = json.dumps(lisbus)
                    lisbus3 = '{ "lisbus3" : '+lisbus2+'}'
                
                datos = { 
                        'nomUsuario' : request.session["nomUsuario"].upper(),
                        'apeUsuario' : request.session["apeUsuario"].upper(),
                        'nomTipo'    : request.session["nomTipo"].upper(),
                        'tit' : tit,
                        'mes' : mes,
                        'yea' : yea,
                        'yearTitulacion' : yea,
                        'lisbus3' : lisbus3,
                        'listaOpcionesFechas' : listaOpcionesFechas,
                        }
                return render(request, 'gestionar_titulados_org.html', datos)
                
            else:
                datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Organizador!!' }
                return render(request, 'index.html', datos)
        else:
            datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
            return render(request, 'index.html', datos)
    except:
        datos = { 
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
                'r2' : 'Error al Procesar Solicitud!!'
                }
        return render(request, 'menuOrganizador.html', datos)


#----------------------------------------------------------------------------------------------------------


def cargarTituladosOrgDet(request, mes, yea):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            if request.session["tipo_id"] == 4:
                
                fecha = request.POST["cbodia"]
                dia = fecha[0:2]
                freves  = str(yea)+"-"+str(mes)+"-"+str(dia)
                
                sql = "select distinct(t.carrera), t.areaAcademica from titulacion_titulado t where t.fechaTitulacion=%s and t.situacion_id=1 order by t.areaAcademica asc, t.carrera asc"
                cursor.execute(sql, freves)
                opcionesCarreras1 = cursor.fetchall()
                
                sql = "select distinct(t.carrera), t.areaAcademica from titulacion_titulado t where t.fechaTitulacion=%s and t.situacion_id=3 order by t.areaAcademica asc, t.carrera asc"
                cursor.execute(sql, freves)
                opcionesCarreras3 = cursor.fetchall()            
                
                cancar=0
                if len(opcionesCarreras1)==0 and len(opcionesCarreras3)==0:
                    cancar=1
                
                val = (mes, yea)
                sql = "select distinct(t.fechaTitulacion), t.fechaTitulacionEstado from titulacion_situacionfechastitulado t, titulacion_titulado z where t.fechaTitulacion=z.fechaTitulacion and month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s and z.situacion_id is not null order by t.fechaTitulacion asc"
                cursor.execute(sql, val)
                opcionesFechas = cursor.fetchall()
                
                listaOpcionesFechas = []
                for x in opcionesFechas:
                    if x[0].day>=1 and x[0].day<=9:
                        dia = str(0)+str(x[0].day)
                    else:
                        dia = x[0].day
                    if x[0].month>=1 and x[0].month<=9:
                        mes = str(0)+str(x[0].month)
                    else:
                        mes = x[0].month
                    año = x[0].year
                    if x[1] == 1:
                        fechasituacion = "(Abierta)"
                    elif x[1] == 2:
                        fechasituacion = "(Cerrada)"
                    fechanormal = str(dia)+"-"+str(mes)+"-"+str(año)
                    fechareves  = str(año)+"-"+str(mes)+"-"+str(dia)
                    listaOpcionesFechas.append({ "dia":dia, "mes":mes, "año":año, "fechanormal":fechanormal, "fechareves":fechareves, "fechasituacion":fechasituacion })

                sql = "select * from titulacion_titulado t where t.fechaTitulacion=%s and t.situacion_id=1 order by t.areaAcademica asc, t.carrera asc, t.paterno asc, t.materno asc, t.nombre asc, t.rut"
                cursor.execute(sql, freves)
                listadoTitulados = cursor.fetchall()
                
                sql = "select count(*) from titulacion_titulado t where t.fechaTitulacion=%s and situacion_id=3;"
                cursor.execute(sql, freves)
                listadoTitulados3 = cursor.fetchone()
                cancar3 = listadoTitulados3[0]
                
                sql = "select * from titulacion_titulado t where t.fechaTitulacion=%s and t.situacion_id=3 order by t.carrera asc, t.paterno asc, t.materno asc, t.nombre asc, t.rut"
                cursor.execute(sql, freves)
                listadoTitulados3 = cursor.fetchall()
                
                datos = { 
                        'nomUsuario' : request.session["nomUsuario"].upper(),
                        'apeUsuario' : request.session["apeUsuario"].upper(),
                        'nomTipo'    : request.session["nomTipo"].upper(),
                        'mes' : mes,
                        'yea' : yea,
                        'yearTitulacion' : yea,
                        'fecha' : fecha,
                        'opcionesCarreras1' : opcionesCarreras1,
                        'opcionesCarreras3' : opcionesCarreras3,
                        'listaOpcionesFechas' : listaOpcionesFechas,
                        'listadoTitulados' : listadoTitulados,
                        'listadoTitulados3' : listadoTitulados3,
                        'cancar' : cancar,
                        'cancar3' : cancar3,
                        }
                return render(request, 'gestionar_titulados_org_det.html', datos)
                
            else:
                datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Organizador!!' }
                return render(request, 'index.html', datos)
        else:
            datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
            return render(request, 'index.html', datos)
    except:
        datos = { 
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
                'r2' : 'Error al Procesar Solicitud!!'
                }
        return render(request, 'menuOrganizador.html', datos)


#----------------------------------------------------------------------------------------------------------


def ver_asistentes_adm(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["tipo_id"] == 1:

            cursor.execute("select year(t.fechaTitulacion), count(year(t.fechaTitulacion)) from titulacion_titulado t group by year(t.fechaTitulacion) order by year(t.fechaTitulacion) desc")
            rs = cursor.fetchall()
            datos = { 
                    'nomUsuario' : request.session["nomUsuario"].upper(),
                    'apeUsuario' : request.session["apeUsuario"].upper(),
                    'nomTipo'    : request.session["nomTipo"].upper(),
                    'rs' : rs,
                    }
            return render(request, 'ver_asistentes_adm.html', datos)
            
        else:
            datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Admin!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)


#----------------------------------------------------------------------------------------------------------


def ver_asistentes_menadm(request, yearTitulacion):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            if request.session["tipo_id"] == 1:
                
                sql = "select month(t.fechaTitulacion), year(t.fechaTitulacion), count(year(t.fechaTitulacion)) from titulacion_titulado t where year(t.fechaTitulacion)=%s group by month(t.fechaTitulacion), year(t.fechaTitulacion)"
                cursor.execute(sql, yearTitulacion)
                rs = cursor.fetchall()
                
                if len(rs) != 0:
                    datos = {
                            'nomUsuario' : request.session["nomUsuario"].upper(),
                            'apeUsuario' : request.session["apeUsuario"].upper(),
                            'nomTipo'    : request.session["nomTipo"].upper(),
                            'rs' : rs,
                            }
                    return render(request, 'ver_asistentes_menadm.html', datos)
                else:
                    datos = {
                            'nomUsuario' : request.session["nomUsuario"].upper(),
                            'apeUsuario' : request.session["apeUsuario"].upper(),
                            'nomTipo'    : request.session["nomTipo"].upper(),
                            'r2' : 'Sin Registros Para Cargar!!',
                            }
                    return render(request, 'ver_asistentes_menadm.html', datos)
            else:
                datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Organizador!!' }
                return render(request, 'index.html', datos)
        else:
            datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
            return render(request, 'index.html', datos)
    except:
        datos = { 
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
                'r2' : 'Error al Procesar Solicitud!!'
                }
        return render(request, 'menuAdmin.html', datos)


#----------------------------------------------------------------------------------------------------------


def ver_asistentes_menadm_cargar(request, mes, yea):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            if request.session["tipo_id"] == 1:
                            
                # --- Para la busqueda con Javascript ---
                
                val = (mes, yea)
                sql = "select distinct(t.fechaTitulacion), t.fechaTitulacionEstado from titulacion_situacionfechastitulado t, titulacion_titulado z where t.fechaTitulacion=z.fechaTitulacion and month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s and z.situacion_id is not null order by t.fechaTitulacion asc"
                cursor.execute(sql, val)
                opcionesFechas = cursor.fetchall()
                
                listaOpcionesFechas = []
                for x in opcionesFechas:
                    if x[0].day>=1 and x[0].day<=9:
                        dia = str(0)+str(x[0].day)
                    else:
                        dia = x[0].day
                    if x[0].month>=1 and x[0].month<=9:
                        mes = str(0)+str(x[0].month)
                    else:
                        mes = x[0].month
                    año = x[0].year
                    if x[1] == 1:
                        fechasituacion = "(Abierta)"
                    elif x[1] == 2:
                        fechasituacion = "(Cerrada)"
                    fechanormal = str(dia)+"-"+str(mes)+"-"+str(año)
                    fechareves  = str(año)+"-"+str(mes)+"-"+str(dia)
                    listaOpcionesFechas.append({ "dia":dia, "mes":mes, "año":año, "fechanormal":fechanormal, "fechareves":fechareves, "fechasituacion":fechasituacion })
                    
                val = (mes, yea)
                sql = "select * from titulacion_titulado t where month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s order by t.fechaTitulacion desc"
                cursor.execute(sql, val)
                tit = cursor.fetchall()
                
                lisbus = []
                for x in tit:
                    if x[8].day>=1 and x[8].day<=9:
                        dia = str(0)+str(x[8].day)
                    else:
                        dia = str(x[8].day)
                    if x[8].month>=1 and x[8].month<=9:
                        mes = str(0)+str(x[8].month)
                    else:
                        mes = str(x[8].month)
                    año = x[8].year
                    fecha = str(dia)+"-"+str(mes)+"-"+str(año)
                    lisbus.append({"id":x[0],"rut":x[1],"nombre":x[2],"paterno":x[3],"materno":x[4],"carrera":x[5],"fechaTitulacion":fecha,"situacion_id":x[12],"ninvitados":x[10]})
                    lisbus2 = json.dumps(lisbus)
                    lisbus3 = '{ "lisbus3" : '+lisbus2+'}'
                
                datos = { 
                        'nomUsuario' : request.session["nomUsuario"].upper(),
                        'apeUsuario' : request.session["apeUsuario"].upper(),
                        'nomTipo'    : request.session["nomTipo"].upper(),
                        'tit' : tit,
                        'mes' : mes,
                        'yea' : yea,
                        'yearTitulacion' : yea,
                        'lisbus3' : lisbus3,
                        'listaOpcionesFechas' : listaOpcionesFechas,
                        }
                return render(request, 'ver_asistentes_menadm_cargar.html', datos)
                
            else:
                datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Admin!!' }
                return render(request, 'index.html', datos)
        else:
            datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
            return render(request, 'index.html', datos)
    except:
        datos = { 
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
                'r2' : 'Error al Procesar Solicitud!!'
                }
        return render(request, 'menuAdmin.html', datos)


#----------------------------------------------------------------------------------------------------------


def ver_asistentes_menadm_cargar_det(request, mes, yea):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            if request.session["tipo_id"] == 1:
                
                fecha = request.POST["cbodia"]
                dia = fecha[0:2]
                freves  = str(yea)+"-"+str(mes)+"-"+str(dia)
                
                sql = "select distinct(t.carrera), t.areaAcademica from titulacion_titulado t where t.fechaTitulacion=%s and t.situacion_id=1 order by t.areaAcademica asc, t.carrera asc"
                cursor.execute(sql, freves)
                opcionesCarreras1 = cursor.fetchall()
                
                sql = "select distinct(t.carrera), t.areaAcademica from titulacion_titulado t where t.fechaTitulacion=%s and t.situacion_id=3 order by t.areaAcademica asc, t.carrera asc"
                cursor.execute(sql, freves)
                opcionesCarreras3 = cursor.fetchall()
                
                cancar=0
                if len(opcionesCarreras1)==0 and len(opcionesCarreras3)==0:
                    cancar=1
                
                val = (mes, yea)
                sql = "select distinct(t.fechaTitulacion), t.fechaTitulacionEstado from titulacion_situacionfechastitulado t, titulacion_titulado z where t.fechaTitulacion=z.fechaTitulacion and month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s and z.situacion_id is not null order by t.fechaTitulacion asc"
                cursor.execute(sql, val)
                opcionesFechas = cursor.fetchall()
                
                listaOpcionesFechas = []
                for x in opcionesFechas:
                    if x[0].day>=1 and x[0].day<=9:
                        dia = str(0)+str(x[0].day)
                    else:
                        dia = x[0].day
                    if x[0].month>=1 and x[0].month<=9:
                        mes = str(0)+str(x[0].month)
                    else:
                        mes = x[0].month
                    año = x[0].year
                    if x[1] == 1:
                        fechasituacion = "(Abierta)"
                    elif x[1] == 2:
                        fechasituacion = "(Cerrada)"
                    fechanormal = str(dia)+"-"+str(mes)+"-"+str(año)
                    fechareves  = str(año)+"-"+str(mes)+"-"+str(dia)
                    listaOpcionesFechas.append({ "dia":dia, "mes":mes, "año":año, "fechanormal":fechanormal, "fechareves":fechareves, "fechasituacion":fechasituacion })

                sql = "select * from titulacion_titulado t where t.fechaTitulacion=%s and t.situacion_id=1 order by t.areaAcademica asc, t.carrera asc, t.paterno asc, t.materno asc, t.nombre asc, t.rut"
                cursor.execute(sql, freves)
                listadoTitulados = cursor.fetchall()
                
                sql = "select count(*) from titulacion_titulado t where t.fechaTitulacion=%s and situacion_id=3;"
                cursor.execute(sql, freves)
                listadoTitulados3 = cursor.fetchone()
                cancar3 = listadoTitulados3[0]
                
                sql = "select * from titulacion_titulado t where t.fechaTitulacion=%s and t.situacion_id=3 order by t.carrera asc, t.paterno asc, t.materno asc, t.nombre asc, t.rut"
                cursor.execute(sql, freves)
                listadoTitulados3 = cursor.fetchall()
                
                datos = { 
                        'nomUsuario' : request.session["nomUsuario"].upper(),
                        'apeUsuario' : request.session["apeUsuario"].upper(),
                        'nomTipo'    : request.session["nomTipo"].upper(),
                        'mes' : mes,
                        'yea' : yea,
                        'yearTitulacion' : yea,
                        'fecha' : fecha,
                        'opcionesCarreras1' : opcionesCarreras1,
                        'opcionesCarreras3' : opcionesCarreras3,
                        'listaOpcionesFechas' : listaOpcionesFechas,
                        'listadoTitulados' : listadoTitulados,
                        'listadoTitulados3' : listadoTitulados3,
                        'cancar' : cancar,
                        'cancar3' : cancar3,
                        }
                return render(request, 'ver_asistentes_menadm_cargar_det.html', datos)
                
            else:
                datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Organizador!!' }
                return render(request, 'index.html', datos)
        else:
            datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
            return render(request, 'index.html', datos)
    except:
        datos = { 
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
                'r2' : 'Error al Procesar Solicitud!!'
                }
        return render(request, 'menuAdmin.html', datos)


#----------------------------------------------------------------------------------------------------------


def mostrarFormGestionarLibretoAdm(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["tipo_id"] == 1:
            
            sql = "select * from titulacion_libreto"
            cursor.execute(sql)
            rs = cursor.fetchone()
            
            if rs is None:
                datos = {
                    'nomUsuario' : request.session["nomUsuario"].upper(),
                    'apeUsuario' : request.session["apeUsuario"].upper(),
                    'nomTipo'    : request.session["nomTipo"].upper(),
                    'ini' : "",
                    'sal' : "",
                    'atr' : "",
                    'fin' : "",
                    'ter' : "",
                }
            else:
                ini = rs[1]
                sal = rs[2]
                atr = rs[3]
                fin = rs[4]
                ter = rs[5]
                datos = {
                    'nomUsuario' : request.session["nomUsuario"].upper(),
                    'apeUsuario' : request.session["apeUsuario"].upper(),
                    'nomTipo'    : request.session["nomTipo"].upper(),
                    'ini' : ini,
                    'sal' : sal,
                    'atr' : atr,
                    'fin' : fin,
                    'ter' : ter,
                }
            return render(request, 'form_gestionar_libreto_adm.html', datos)            
        else:
            datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)


#----------------------------------------------------------------------------------------------------------


def guardarLibretoAdm(request):
    try:
        if request.method == "POST":
            ini = request.POST["txtini"]
            sal = request.POST["txtsal"]
            atr = request.POST["txtatr"]
            fin = request.POST["txtfin"]
            ter = request.POST["txtter"]
            
            sql = "select count(*) from titulacion_libreto"
            cursor.execute(sql)
            rs = cursor.fetchone()
            
            if rs[0] == 0:
                val = (ini, sal, atr, fin, ter)
                sql = "insert into titulacion_libreto (iniLibreto, salLibreto, atrLibreto, finLibreto, terLibreto) values (%s, %s, %s, %s, %s)"
                cursor.execute(sql, val)
                connection.commit()
            else:
                sql = "select id from titulacion_libreto"
                cursor.execute(sql)
                rs = cursor.fetchone()
                
                val = (ini, sal, atr, fin, ter, rs[0])
                sql = "update titulacion_libreto set iniLibreto=%s, salLibreto=%s, atrLibreto=%s, finLibreto=%s, terLibreto=%s where id=%s"
                cursor.execute(sql, val)
                rs = cursor.fetchone()                

            datos = { 
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
                'ini' : ini,
                'sal' : sal,
                'atr' : atr,
                'fin' : fin,
                'ter' : ter,
                'res' : 'Libreto Guardado Correctamente!!',
            }
            return render(request, 'form_gestionar_libreto_adm.html', datos)
        else:
            datos = { 
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
                'ini' : ini,
                'sal' : sal,
                'atr' : atr,
                'fin' : fin,
                'ter' : ter,
                'r2' : 'No Se Puede Procesar La Solicitud!!',
            }
            return render(request, 'form_gestionar_libreto_adm.html', datos)
    except:
        datos = { 
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
                'ini' : ini,
                'sal' : sal,
                'atr' : atr,
                'fin' : fin,
                'ter' : ter,
                'r2' : 'No Se Puede Procesar La Solicitud!!',
            }
        return render(request, 'form_gestionar_libreto_adm.html', datos)
        
        
#----------------------------------------------------------------------------------------------------------


def mostrarMenuLocutor(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["tipo_id"] == 3:
            datos = {
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper()
            }
            return render(request, 'menuLocutor.html', datos)
        else:
            datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Locutor!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)


#----------------------------------------------------------------------------------------------------------


def ver_libreto_loc(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["tipo_id"] == 3:

            cursor.execute("select year(t.fechaTitulacion), count(year(t.fechaTitulacion)) from titulacion_titulado t group by year(t.fechaTitulacion) order by year(t.fechaTitulacion) desc")
            rs = cursor.fetchall()
            datos = { 
                    'nomUsuario' : request.session["nomUsuario"].upper(),
                    'apeUsuario' : request.session["apeUsuario"].upper(),
                    'nomTipo'    : request.session["nomTipo"].upper(),
                    'rs' : rs,
                    }
            return render(request, 'ver_libreto_loc.html', datos)
            
        else:
            datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Locutor!!' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
        return render(request, 'index.html', datos)


#----------------------------------------------------------------------------------------------------------


def ver_libreto_menloc(request, yearTitulacion):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            if request.session["tipo_id"] == 3:
                
                sql = "select month(t.fechaTitulacion), year(t.fechaTitulacion), count(year(t.fechaTitulacion)) from titulacion_titulado t where year(t.fechaTitulacion)=%s group by month(t.fechaTitulacion), year(t.fechaTitulacion)"
                cursor.execute(sql, yearTitulacion)
                rs = cursor.fetchall()
                
                if len(rs) != 0:
                    datos = {
                            'nomUsuario' : request.session["nomUsuario"].upper(),
                            'apeUsuario' : request.session["apeUsuario"].upper(),
                            'nomTipo'    : request.session["nomTipo"].upper(),
                            'rs' : rs,
                            }
                    return render(request, 'ver_libreto_menloc.html', datos)
                else:
                    datos = {
                            'nomUsuario' : request.session["nomUsuario"].upper(),
                            'apeUsuario' : request.session["apeUsuario"].upper(),
                            'nomTipo'    : request.session["nomTipo"].upper(),
                            'r2' : 'Sin Registros Para Cargar!!',
                            }
                    return render(request, 'ver_asistentes_menadm.html', datos)
            else:
                datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Locutor!!' }
                return render(request, 'index.html', datos)
        else:
            datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
            return render(request, 'index.html', datos)
    except:
        datos = { 
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
                'r2' : 'Error al Procesar Solicitud!!'
                }
        return render(request, 'menuLocutor.html', datos)


#----------------------------------------------------------------------------------------------------------


def ver_libreto_menloc_cargar(request, mes, yea):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            if request.session["tipo_id"] == 3:
                            
                # --- Para la busqueda con Javascript ---
                
                val = (mes, yea)
                sql = "select distinct(t.fechaTitulacion), t.fechaTitulacionEstado from titulacion_situacionfechastitulado t, titulacion_titulado z where t.fechaTitulacion=z.fechaTitulacion and month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s and z.situacion_id is not null order by t.fechaTitulacion asc"
                cursor.execute(sql, val)
                opcionesFechas = cursor.fetchall()
                
                listaOpcionesFechas = []
                for x in opcionesFechas:
                    if x[0].day>=1 and x[0].day<=9:
                        dia = str(0)+str(x[0].day)
                    else:
                        dia = x[0].day
                    if x[0].month>=1 and x[0].month<=9:
                        mes = str(0)+str(x[0].month)
                    else:
                        mes = x[0].month
                    año = x[0].year
                    if x[1] == 1:
                        fechasituacion = "(Abierta)"
                    elif x[1] == 2:
                        fechasituacion = "(Cerrada)"
                    fechanormal = str(dia)+"-"+str(mes)+"-"+str(año)
                    fechareves  = str(año)+"-"+str(mes)+"-"+str(dia)
                    listaOpcionesFechas.append({ "dia":dia, "mes":mes, "año":año, "fechanormal":fechanormal, "fechareves":fechareves, "fechasituacion":fechasituacion })
                    
                val = (mes, yea)
                sql = "select * from titulacion_titulado t where month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s order by t.fechaTitulacion desc"
                cursor.execute(sql, val)
                tit = cursor.fetchall()
                
                lisbus = []
                for x in tit:
                    if x[8].day>=1 and x[8].day<=9:
                        dia = str(0)+str(x[8].day)
                    else:
                        dia = str(x[8].day)
                    if x[8].month>=1 and x[8].month<=9:
                        mes = str(0)+str(x[8].month)
                    else:
                        mes = str(x[8].month)
                    año = x[8].year
                    fecha = str(dia)+"-"+str(mes)+"-"+str(año)
                    lisbus.append({"id":x[0],"rut":x[1],"nombre":x[2],"paterno":x[3],"materno":x[4],"carrera":x[5],"fechaTitulacion":fecha,"situacion_id":x[12],"ninvitados":x[10]})
                    lisbus2 = json.dumps(lisbus)
                    lisbus3 = '{ "lisbus3" : '+lisbus2+'}'
                
                datos = { 
                        'nomUsuario' : request.session["nomUsuario"].upper(),
                        'apeUsuario' : request.session["apeUsuario"].upper(),
                        'nomTipo'    : request.session["nomTipo"].upper(),
                        'tit' : tit,
                        'mes' : mes,
                        'yea' : yea,
                        'yearTitulacion' : yea,
                        'lisbus3' : lisbus3,
                        'listaOpcionesFechas' : listaOpcionesFechas,
                        }
                return render(request, 'ver_libreto_menloc_cargar.html', datos)
                
            else:
                datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Locutor!!' }
                return render(request, 'index.html', datos)
        else:
            datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
            return render(request, 'index.html', datos)
    except:
        datos = { 
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
                'r2' : 'Error al Procesar Solicitud!!'
                }
        return render(request, 'menuLocutor.html', datos)


#----------------------------------------------------------------------------------------------------------


def ver_libreto_menloc_cargar_det(request, mes, yea):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:
            if request.session["tipo_id"] == 3:
                
                fecha = request.POST["cbodia"]
                dia = fecha[0:2]
                freves  = str(yea)+"-"+str(mes)+"-"+str(dia)
                
                sql = "select t.rut, t.nombre, t.paterno, t.materno, t.carrera, t.areaAcademica, t.situacion_id from titulacion_titulado t where t.fechaTitulacion=%s and t.situacion_id=1  order by areaAcademica asc, carrera asc, paterno asc, materno asc, nombre asc, rut asc"
                cursor.execute(sql, freves)
                listadoTitulados = cursor.fetchall()
                                
                val = (mes, yea)
                sql = "select distinct(t.fechaTitulacion), t.fechaTitulacionEstado from titulacion_situacionfechastitulado t, titulacion_titulado z where t.fechaTitulacion=z.fechaTitulacion and month(t.fechaTitulacion)=%s and year(t.fechaTitulacion)=%s and z.situacion_id is not null order by t.fechaTitulacion asc"
                cursor.execute(sql, val)
                opcionesFechas = cursor.fetchall()
                
                listaOpcionesFechas = []
                for x in opcionesFechas:
                    if x[0].day>=1 and x[0].day<=9:
                        dia = str(0)+str(x[0].day)
                    else:
                        dia = x[0].day
                    if x[0].month>=1 and x[0].month<=9:
                        mes = str(0)+str(x[0].month)
                    else:
                        mes = x[0].month
                    año = x[0].year
                    if x[1] == 1:
                        fechasituacion = "(Abierta)"
                    elif x[1] == 2:
                        fechasituacion = "(Cerrada)"
                    fechanormal = str(dia)+"-"+str(mes)+"-"+str(año)
                    fechareves  = str(año)+"-"+str(mes)+"-"+str(dia)
                    listaOpcionesFechas.append({ "dia":dia, "mes":mes, "año":año, "fechanormal":fechanormal, "fechareves":fechareves, "fechasituacion":fechasituacion })
                
                sql = "select count(*) from titulacion_titulado t where t.fechaTitulacion=%s and situacion_id=3;"
                cursor.execute(sql, freves)
                listadoTitulados3 = cursor.fetchone()
                cancar3 = listadoTitulados3[0]
                                
                sql = "select * from titulacion_libreto"
                cursor.execute(sql)
                rslib = cursor.fetchall()
                ini = rslib[0][1]
                sal = rslib[0][2]
                atr = rslib[0][3]
                fin = rslib[0][4]
                ter = rslib[0][5]
                
                ini = ini.replace("CEREMONIA DE TITULACIÓN","CEREMONIA DE TITULACIÓN "+str(yea))
                ter = ter.replace("CEREMONIA DE TITULACIÓN","CEREMONIA DE TITULACION "+str(yea))
                
                sql = "select distinct(t.areaAcademica) from titulacion_titulado t where t.fechaTitulacion=%s and t.situacion_id=1 order by t.areaAcademica asc"
                cursor.execute(sql, freves)
                areas = cursor.fetchall()
                
                #sql = "select count(distinct(t.areaAcademica)) from titulacion_titulado t where t.fechaTitulacion=%s and t.situacion_id=1 order by t.areaAcademica asc"
                #cursor.execute(sql, freves)
                #cantAreas = cursor.fetchone()
                
                sql = "select t.carrera, t.areaAcademica from titulacion_titulado t where t.fechaTitulacion=%s and t.situacion_id=1 group by (t.carrera) order by t.areaAcademica asc, t.carrera asc"
                cursor.execute(sql, freves)
                carreras = cursor.fetchall()
                
                sql = "select distinct(t.carrera) from titulacion_titulado t where t.fechaTitulacion=%s and t.situacion_id=1 group by (t.carrera) order by t.areaAcademica asc, t.carrera asc"
                cursor.execute(sql, freves)
                soloCarreras = cursor.fetchall()
                
                textoArea = "<u><h2 style='margin:0; padding:0;'>ÁREA "+str(areas[0][0]).upper()+"</h2></u>"
                textojefe = "<br/>HACE ENTREGA DE LOS TÍTULOS, EL(LA) DIRECTOR(A) DE CARRERA SEÑOR(A) NOMBRE DE JEFE"
                textoSolicitar1 = ""
                textoSolicitar2 = ""
                textoAplauso = ""
                listafinal = []
                i=0; jc=0; ja=0                
                cantControl = 0
                
                listafinal.append(textoArea)
                listafinal.append(textojefe)
                for car in carreras:
                    jc += 1
                    val = (freves, car[0])
                    sql = "select t.nombre, t.paterno, t.materno, t.carrera from titulacion_titulado t where t.fechaTitulacion=%s and t.carrera=%s and t.situacion_id=1 order by t.areaAcademica, t.carrera asc, t.paterno asc, t.materno asc, t.nombre asc, t.rut asc"
                    cursor.execute(sql, val)
                    carrerasAreas = cursor.fetchall()
                    
                    val = (freves, car[1])
                    sql = "select count(*) from titulacion_titulado t where t.fechaTitulacion=%s and t.areaAcademica=%s and t.situacion_id=1"
                    cursor.execute(sql, val)
                    cantCarrerasAreas = cursor.fetchone()
                                        
                    if i==0:
                        textoSolicitar1 = "<br/><br/>SE SOLICITA SUBIR AL ESCENARIO A LOS TITULADOS DEL PROGRAMA DE ESTUDIO <strong style='background-color:#FAF962;'>"+carrerasAreas[0][3].upper()+"</strong>.<br/>"
                        listafinal.append(textoSolicitar1)
                        listafinal.append("<br/>")
                        i += 1
                    
                    for ca in carrerasAreas:
                        cantControl += 1
                        if car[0] == ca[3]:
                            listafinal.append("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#9830; "+str(ca[0])+" "+str(ca[1])+" "+str(ca[2]))
                            listafinal.append("<br/>")
                    
                    textoAplauso = "<br/>BRINDEMOS UN FUERTE APLAUSO A ESTOS NUEVOS PROFESIONALES DE <strong style='background-color:#FAF962;'>"+ca[3].upper()+"</strong>.<br/>"
                    listafinal.append(textoAplauso)
                    
                    if cantControl < cantCarrerasAreas[0]:
                        textoSolicitar2 = "<br/>SOLICITAMOS AL(LA) DIRECTOR(A) PERMANECER EN EL ESCENARIO PARA LA ENTREGA DE LOS SIGUIENTES TÍTULOS DEL PROGRAMA DE ESTUDIO <strong style='background-color:#FAF962;'>"+str(soloCarreras[jc][0].upper())+"</strong><br/><br/>"
                        listafinal.append(textoSolicitar2)
                    else:                        
                        textoAgradecimiento = "<br/>JUNTO CON FELICITARLOS, AGRADECEMOS LA PRESENCIA DEL(LA) DIRECTOR(A) DE CARRERA NOMBRE JEFE CARRERA.<br/>"
                        listafinal.append(textoAgradecimiento)
                        
                        cantControl = 0
                        if ja<len(areas)-1:
                            ja += 1               
                            texto = "<br/><br/><br/><u><h2 style='margin:0; padding:0;'>ÁREA "+str(areas[ja][0]).upper()+"</h2></u><br/>"
                            listafinal.append(texto)
                    
                        textojefe = "HACE ENTREGA DE LOS TÍTULOS, EL(LA) DIRECTOR(A) DE CARRERA SEÑOR(A) NOMBRE DE JEFE<br/><br/>"
                        listafinal.append(textojefe)
                        if jc<len(soloCarreras):
                            texto3 = "SE SOLICITA SUBIR AL ESCENARIO A LOS TITULADOS DEL PROGRAMA DE ESTUDIO <strong style='background-color:#FAF962;'>"+str(soloCarreras[jc][0].upper())+"</strong>.<br/><br/>"
                            listafinal.append(texto3)
                
                listafinal.pop()
                
                sql = "select t.rut, t.nombre, t.paterno, t.materno, t.carrera, t.situacion_id from titulacion_titulado t where t.fechaTitulacion=%s and t.situacion_id=3 order by t.carrera asc, t.paterno asc, t.materno asc, t.nombre asc, t.rut asc"
                cursor.execute(sql, freves)
                asistentesTarde = cursor.fetchall()
                
                listaAtrasos = []
                if len(asistentesTarde)!=0:
                    listaAtrasos.append(atr)
                    for x in asistentesTarde:
                        listaAtrasos.append("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#9830; "+str(x[1]).upper()+" "+str(x[2]).upper()+" "+str(x[3]).upper()+" <u>("+str(x[4]).upper()+")</u><br/>")
                    listaAtrasos.append("<br/>"+str(fin))
                
                fechaPalabras = ""
                sql = "set lc_time_names = 'es_ES'"
                cursor.execute(sql)
                sql = "select distinct(t.fechaTitulacion), dayname(t.fechaTitulacion), day(t.fechaTitulacion), monthname(t.fechaTitulacion), year(t.fechaTitulacion) from titulacion_titulado t where t.fechaTitulacion=%s"
                cursor.execute(sql, freves)
                rs = cursor.fetchone()
                if len(rs)>1:
                    if int(rs[2])<9:
                        fechaPalabras = "RANCAGUA, "+str(rs[1]).upper()+" 0"+str(rs[2])+" DE "+str(rs[3]).upper()+" DEL "+str(rs[4])
                    else:
                        fechaPalabras = "RANCAGUA, "+str(rs[1]).upper()+" "+str(rs[2])+" DE "+str(rs[3]).upper()+" DEL "+str(rs[4])
                    

                datos = { 
                        'nomUsuario' : request.session["nomUsuario"].upper(),
                        'apeUsuario' : request.session["apeUsuario"].upper(),
                        'nomTipo'    : request.session["nomTipo"].upper(),
                        'mes' : mes,
                        'yea' : yea,
                        'yearTitulacion' : yea,
                        'fecha' : fecha,
                        'listaOpcionesFechas' : listaOpcionesFechas,
                        'listadoTitulados' : listadoTitulados,
                        'listafinal' : listafinal,
                        'asistentesTarde' : asistentesTarde,
                        'cancar3' : cancar3,
                        'ini' : ini,
                        'sal' : sal,
                        'atr' : atr,
                        'fin' : fin,
                        'ter' : ter,
                        'fechaPalabras' : fechaPalabras,
                        'listaAtrasos' : listaAtrasos,
                        }
                
                return render(request, 'ver_libreto_menloc_cargar_det.html', datos)
                
            else:
                datos = { 'r2' : 'No Tiene Privilegios Suficientes Para Acceder al Menú del Locutor!!' }
                return render(request, 'index.html', datos)
        else:
            datos = { 'r2' : 'Debe Iniciar Sesión Para Acceder!!' }
            return render(request, 'index.html', datos)
    except:
        datos = { 
                'nomUsuario' : request.session["nomUsuario"].upper(),
                'apeUsuario' : request.session["apeUsuario"].upper(),
                'nomTipo'    : request.session["nomTipo"].upper(),
                'r2' : 'Error al Procesar Solicitud!!'
                }
        return render(request, 'menuLocutor.html', datos)


#----------------------------------------------------------------------------------------------------------

