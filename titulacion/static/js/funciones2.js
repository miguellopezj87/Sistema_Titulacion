
const botonGestionarFecha = (op, fechaFiltro) => {
    console.log("FF : " + fechaFiltro);
    let mensaje = "";
    let icono = "";
    if(op==2){ //Cerrar fecha
        titulo = '<div style="color:#DC3545">Atención</div>';
        icono = 'warning';
        mensaje = '<h5>Al <u>Cerrar</u> la fecha, los siguientes Titulados que se ingresen quedarán como <strong style="color:#DC3545; text-decoration:underline;">\'Atrasados\'</strong></h5>';
    }else if(op==1){ // Abrir fecha
        titulo = '<div style="color:#3355FF">Atención</div>';
        icono = 'info';
        mensaje = '<h5>Al <u>Abrir</u> la fecha, los siguientes Titulados que se ingresen quedarán como <strong style="color:#3355FF; text-decoration:underline;">\'Presentes\'</strong></h5>';
    }

    Swal.fire({
        title: titulo,
        icon: icono,
        html: mensaje,
        showCancelButton: true,
        confirmButtonText: 'OK',
        focusConfirm: false,
      }).then((result) => {
        if (result.isConfirmed) {
            //Swal.fire('Saved!', '', 'success')
            window.location.href="/cambiar_estado_fecha_adm/"+fechaFiltro+"/"+op;
        }
      })
}





const botonGestionarMes = (mes, yea) => {
    console.log("MES : " + mes);
    console.log("YEA : " + yea);
    let op = 0;
    let mensaje = "";
    let icono = 'info';
    let titulo = '<div>Atención</div>';
    
    let texto1 = '<p style="font-size:20px; text-align:justify;"><strong>"Abrir" :</strong> Dejará los siguientes Titulados que se ingresen como <strong style="color:#3355FF; text-decoration:underline;">\'Presentes\'</strong></p>';
    let texto2 = '<p style="font-size:20px; text-align:justify;"><strong>"Cerrar" :</strong> Dejará los siguientes Titulados que se ingresen como <strong style="color:#DC3545; text-decoration:underline;">\'Atrasados\'</strong></p>';    Swal.fire({
        title: titulo,
        html: texto1+texto2,
        showDenyButton: true,
        showCancelButton: true,
        confirmButtonText: 'Abrir Mes Completo',
        denyButtonText: `Cerrar Mes Completo`,
      }).then((result) => {
        if (result.isConfirmed) {
            op = 1;
            //Swal.fire('Mes Abierto', '<p style="font-size:25px;">Los siguientes Titulados que se ingresen quedarán como <strong style="color:#3355FF; text-decoration:underline;">\'Presentes\'</strong></p>', 'success')
        } else if (result.isDenied) {
            op = 2;
            //Swal.fire('Mes Cerrado', '<p style="font-size:25px;">Los siguientes Titulados que se ingresen quedarán como <strong style="color:#DC3545; text-decoration:underline;">\'Atrasados\'</strong></p>', 'info')
        }

        console.log("OP : " + op);
        if(op===1 || op===2){
          window.location.href="/cambiar_estado_mes_adm/"+mes+"/"+yea+"/"+op;
        }

      })

}





const filtrar2 = (lisbus3, mes, yearTitulacion, fechaFiltro, listaOpcionesFechas) => {
    let res1 = lisbus3;                
    let res2 = lisbus3.replaceAll("&quot;","\"");
    let obj = JSON.parse(res2);

    var aux = document.getElementById("txtbus").value.toUpperCase();
    let filas = "";
    obj["lisbus3"].forEach((item) => {
        nom = item.paterno + " ";
        nom = nom + item.materno + " ";
        nom = nom + item.nombre;

        if (fechaFiltro===item.fechaTitulacion && (item.rut.toUpperCase().match(aux) || nom.toUpperCase().match(aux) || item.carrera.toUpperCase().match(aux))){ 
            if(item.situacion_id===1){
                filas = filas + "<tr class='table-success'>";
            }else if(item.situacion_id===3){
                filas = filas + "<tr class='table-warning'>";
            }
                //filas = filas + "<tr>";
                filas = filas + "<td width='120'>"+item.rut+"</td>";
                filas = filas + "<td>"+item.paterno+" "+item.materno+" "+item.nombre+"</td>";    
                filas = filas + "<td>"+item.carrera+"</td>";
                    
                filas = filas + "<td width='120'>"+item.fechaTitulacion+"</td>";

                id = item.id;
                ye = yearTitulacion;
                    
                marcador = "";
                if(item.situacion_id === 1 || item.situacion_id === 3){
                    marcador = "checked";
                }
                filas = filas + "<td><h3><center><input value=''  id='chk"+id+"' name='chk"+id+"' class='form-check-input' type='checkbox' style='border:1px solid black;' "+marcador+"></center></h3></td>";

                if(item.ninvitados === null){
                    filas = filas + "<td><center><input id='txtninv"+id+"' name='txtninv"+id+"' type='number' min='0' max='2' value=''     class='text-center form-control' placeholder='nro' style='border:1px solid black;'  onkeyup='this.value=validarSoloNumeros(this.value)' required></center></td>";
                }else{
                    n = item.ninvitados
                    filas = filas + "<td><center><input id='txtninv"+id+"' name='txtninv"+id+"' type='number' min='0' max='2' value='"+n+"' class='text-center form-control' placeholder='nro' style='border:1px solid black;' onkeyup='this.value=validarSoloNumeros(this.value)' required></center></td>";
                }

                filas = filas + "<td><center><a onClick='guardarAsistencia("+id+","+mes+","+yearTitulacion+",\""+fechaFiltro+"\")' class='btn btn-primary'><i class='bi bi-save'></i></a></center></td>";
            
            filas = filas + "</tr>";
        }else if (fechaFiltro==="allmydata" && (item.rut.toUpperCase().match(aux) || nom.toUpperCase().match(aux) || item.carrera.toUpperCase().match(aux))){ 
            if(item.situacion_id===1){
                filas = filas + "<tr class='table-success'>";
            }else if(item.situacion_id===3){
                filas = filas + "<tr class='table-warning'>";
            }
                filas = filas + "<td width='120'>"+item.rut+"</td>";
                filas = filas + "<td>"+item.paterno+" "+item.materno+" "+item.nombre+"</td>";    
                filas = filas + "<td>"+item.carrera+"</td>";
                
                filas = filas + "<td width='120'>"+item.fechaTitulacion+"</td>";

                id = item.id;
                ye = yearTitulacion;
                
                marcador = "";
                if(item.situacion_id === 1 || item.situacion_id === 3){
                    marcador = "checked";
                }
                filas = filas + "<td><h3><center><input value=''  id='chk"+id+"' name='chk"+id+"' class='form-check-input' type='checkbox' style='border:1px solid black;' "+marcador+"></center></h3></td>";

                if(item.ninvitados === null){
                    filas = filas + "<td><center><input id='txtninv"+id+"' name='txtninv"+id+"' type='number' min='0' max='2' value=''     class='text-center form-control' placeholder='nro' style='border:1px solid black;'  onkeyup='this.value=validarSoloNumeros(this.value)' required></center></td>";
                }else{
                    n = item.ninvitados
                    filas = filas + "<td><center><input id='txtninv"+id+"' name='txtninv"+id+"' type='number' min='0' max='2' value='"+n+"' class='text-center form-control' placeholder='nro' style='border:1px solid black;' onkeyup='this.value=validarSoloNumeros(this.value)' required></center></td>";
                }

                filas = filas + "<td><center><a onClick='guardarAsistencia("+id+","+mes+","+yearTitulacion+",\""+fechaFiltro+"\")' class='btn btn-primary'><i class='bi bi-save'></i></a></center></td>";

            filas = filas + "</tr>";
        }
    });
    document.getElementById("tabla_titulados").innerHTML = filas;
}





const guardarAsistencia = (id, mes, yearTitulacion, fechaFiltro) => {
    let sit=2, ninv=0;
    console.log("GUARDAR ASISTENCIA: "+String(fechaFiltro));
    
    if(document.getElementById("chk"+id).checked){
        sit = 1;
    }
    
    ninv = Number(document.getElementById("txtninv"+id).value);
    
    let errores = "";
    if(sit===1 && (ninv <0 || ninv>2)){
        errores = errores + "El Nro de Invitados Debe Estar Entre 0 y 2";
    }

    if(sit===2 && ninv!==0){
        errores = errores + "Al no Asistir, El Nro de Invitados Debe Quedar en Cero.";
    }

    
    if(errores === ""){
        window.location.href="/guardar_asistencia_titulados/"+id+"/"+mes+"/"+yearTitulacion+"/"+sit+"/"+ninv+"/"+fechaFiltro+"/x";
    }else{
        sit=0; ninv=0
        window.location.href="/guardar_asistencia_titulados/"+id+"/"+mes+"/"+yearTitulacion+"/"+sit+"/"+ninv+"/"+fechaFiltro+"/"+errores;
    }

}





const filtrarPorFecha = (lisbus3, mes, yearTitulacion, fechaFiltro, listaOpcionesFechas) => {
    let res1 = lisbus3;                
    let res2 = lisbus3.replaceAll("&quot;","\"");
    let obj = JSON.parse(res2);

    let filas = "";
    obj["lisbus3"].forEach((item) => {
        nom = item.paterno + " ";
        nom = nom + item.materno + " ";
        nom = nom + item.nombre;
        if(fechaFiltro !== "allmydata"){
            if (item.fechaTitulacion == fechaFiltro){
                if(item.situacion_id===1){
                    filas = filas + "<tr class='table-success'>";
                }else if(item.situacion_id===3){
                    filas = filas + "<tr class='table-warning'>";
                }
                //filas = filas + "<tr>";
                    filas = filas + "<td width='120'>"+item.rut+"</td>";
                    filas = filas + "<td>"+item.paterno+" "+item.materno+" "+item.nombre+"</td>";    
                    filas = filas + "<td>"+item.carrera+"</td>";
                    
                    filas = filas + "<td width='120'>"+item.fechaTitulacion+"</td>";

                    id = item.id;
                    ye = yearTitulacion;
                    
                    marcador = "";
                    if(item.situacion_id === 1 || item.situacion_id === 3){
                        marcador = "checked";
                    }
                    filas = filas + "<td><h3><center><input value=''  id='chk"+id+"' name='chk"+id+"' class='form-check-input' type='checkbox' style='border:1px solid black;' "+marcador+"></center></h3></td>";

                    if(item.ninvitados === null){
                        filas = filas + "<td><center><input id='txtninv"+id+"' name='txtninv"+id+"' type='number' min='0' max='2' value=''     class='text-center form-control' placeholder='nro' style='border:1px solid black;'  onkeyup='this.value=validarSoloNumeros(this.value)' required></center></td>";
                    }else{
                        n = item.ninvitados
                        filas = filas + "<td><center><input id='txtninv"+id+"' name='txtninv"+id+"' type='number' min='0' max='2' value='"+n+"' class='text-center form-control' placeholder='nro' style='border:1px solid black;' onkeyup='this.value=validarSoloNumeros(this.value)' required></center></td>";
                    }

                    filas = filas + "<td><center><a onClick='guardarAsistencia("+id+","+mes+","+yearTitulacion+",\""+fechaFiltro+"\")' class='btn btn-primary'><i class='bi bi-save'></i></a></center></td>";

                filas = filas + "</tr>";
            }
        }else{
            if(item.situacion_id===1){
                filas = filas + "<tr class='table-success'>";
            }else if(item.situacion_id===3){
                filas = filas + "<tr class='table-warning'>";
            }
            //filas = filas + "<tr>";
                filas = filas + "<td width='120'>"+item.rut+"</td>";
                filas = filas + "<td>"+item.paterno+" "+item.materno+" "+item.nombre+"</td>";    
                filas = filas + "<td>"+item.carrera+"</td>";
                
                filas = filas + "<td width='120'>"+item.fechaTitulacion+"</td>";

                id = item.id;
                ye = yearTitulacion;
                
                marcador = "";
                if(item.situacion_id === 1 || item.situacion_id === 3){
                    marcador = "checked";
                }
                filas = filas + "<td><h3><center><input value=''  id='chk"+id+"' name='chk"+id+"' class='form-check-input' type='checkbox' style='border:1px solid black;' "+marcador+"></center></h3></td>";

                if(item.ninvitados === null){
                    filas = filas + "<td><center><input id='txtninv"+id+"' name='txtninv"+id+"' type='number' min='0' max='2' value=''     class='text-center form-control' placeholder='nro' style='border:1px solid black;'  onkeyup='this.value=validarSoloNumeros(this.value)' required></center></td>";
                }else{
                    n = item.ninvitados
                    filas = filas + "<td><center><input id='txtninv"+id+"' name='txtninv"+id+"' type='number' min='0' max='2' value='"+n+"' class='text-center form-control' placeholder='nro' style='border:1px solid black;' onkeyup='this.value=validarSoloNumeros(this.value)' required></center></td>";
                }

                filas = filas + "<td><center><a onClick='guardarAsistencia("+id+","+mes+","+yearTitulacion+",\""+fechaFiltro+"\")' class='btn btn-primary'><i class='bi bi-save'></i></a></center></td>";

            filas = filas + "</tr>";
        }
    });
    document.getElementById("tabla_titulados").innerHTML = filas;
}





//-------------------------------------------------------------------------------
//-------------------------------------------------------------------------------
//-------------------------------------------------------------------------------





const comprobarSituacionFecha = (fechaFiltro) => {
    //window.location.href="/comprobar_situacion_fecha?fecha="+fechaFiltro;
}





const filtrarTituladosAdm = (lisbus3, mes, yearTitulacion, fechaFiltro, listaOpcionesFechas) => {
    let res1 = lisbus3;                
    let res2 = lisbus3.replaceAll("&quot;","\"");
    let obj = JSON.parse(res2);



    var e = document.getElementById("cbodia");
    var texto = e.options[e.selectedIndex].text;
    let textocombo = texto.substr(14,21);

    let pfechasitmes = document.getElementById("pfechasitmes").innerHTML;
    alld = document.getElementById("cbodia").value;

    let btn="";
    if(textocombo === "(Abierta)"){
        btn = '<a class="btn btn-primary text-white float-right" onClick="botonGestionarFecha(2, \''+fechaFiltro+'\')"><strong>Cerra Fecha Seleccionada</strong></a>';
    }
    if(textocombo === "(Cerrada)"){
        btn = '<a class="btn btn-primary text-white float-right" onClick="botonGestionarFecha(1, \''+fechaFiltro+'\')"><strong>Abrir Fecha Seleccionada</strong></a>';
    }
    
    if(alld==="allmydata"){
        btn = '<a class="btn btn-primary text-white float-right" onClick="botonGestionarMes('+mes+', \''+yearTitulacion+'\')"><strong>Gestionar Mes</strong></a>';
    }

    fechaFiltro = e.value;
    document.getElementById("btnges").innerHTML = btn;



    var aux = document.getElementById("txtbus").value.toUpperCase();
    let filas = "";

    obj["lisbus3"].forEach((item) => {
        nom = item.paterno + " ";
        nom = nom + item.materno + " ";
        nom = nom + item.nombre;
        if (fechaFiltro===item.fechaTitulacion && (item.rut.toUpperCase().match(aux) || nom.toUpperCase().match(aux) || item.carrera.toUpperCase().match(aux))){ 
            if(item.situacion_id===1){
                filas = filas + "<tr class='table-success'>";
            }else if(item.situacion_id===3){
                filas = filas + "<tr class='table-warning'>";
            }
            //filas = filas + "<tr>";
                filas = filas + "<td width='120'>"+item.rut+"</td>";
                filas = filas + "<td>"+item.paterno+" "+item.materno+" "+item.nombre+"</td>";    
                filas = filas + "<td>"+item.carrera+"</td>";
                    
                filas = filas + "<td width='120'>"+item.fechaTitulacion+"</td>";

                id = item.id;
                ye = yearTitulacion;
                
                marcador = "";
                if(item.situacion_id === 1 || item.situacion_id === 3){
                    marcador = "checked";
                }
                filas = filas + "<td><h3><center><input value=''  id='chk"+id+"' name='chk"+id+"' class='form-check-input' type='checkbox' style='border:1px solid black;' "+marcador+"></center></h3></td>";

                if(item.ninvitados === null){
                    filas = filas + "<td><center><input id='txtninv"+id+"' name='txtninv"+id+"' type='number' min='0' max='2' value=''     class='text-center form-control' placeholder='nro' style='border:1px solid black;'  onkeyup='this.value=validarSoloNumeros(this.value)' required></center></td>";
                }else{
                    n = item.ninvitados
                    filas = filas + "<td><center><input id='txtninv"+id+"' name='txtninv"+id+"' type='number' min='0' max='2' value='"+n+"' class='text-center form-control' placeholder='nro' style='border:1px solid black;' onkeyup='this.value=validarSoloNumeros(this.value)' required></center></td>";
                }

                filas = filas + "<td><center><a onClick='guardarAsistenciaAdm("+id+","+mes+","+yearTitulacion+",\""+fechaFiltro+"\")' class='btn btn-primary'><i class='bi bi-save'></i></a></center></td>";

            filas = filas + "</tr>";
        }else if (fechaFiltro==="allmydata" && (item.rut.toUpperCase().match(aux) || nom.toUpperCase().match(aux) || item.carrera.toUpperCase().match(aux))){ 
            if(item.situacion_id===1){
                filas = filas + "<tr class='table-success'>";
            }else if(item.situacion_id===3){
                filas = filas + "<tr class='table-warning'>";
            }
            //filas = filas + "<tr>";
                filas = filas + "<td width='120'>"+item.rut+"</td>";
                filas = filas + "<td>"+item.paterno+" "+item.materno+" "+item.nombre+"</td>";    
                filas = filas + "<td>"+item.carrera+"</td>";
                
                filas = filas + "<td width='120'>"+item.fechaTitulacion+"</td>";

                id = item.id;
                ye = yearTitulacion;
                
                marcador = "";
                if(item.situacion_id === 1 || item.situacion_id === 3){
                    marcador = "checked";
                }
                filas = filas + "<td><h3><center><input value=''  id='chk"+id+"' name='chk"+id+"' class='form-check-input' type='checkbox' style='border:1px solid black;' "+marcador+"></center></h3></td>";

                if(item.ninvitados === null){
                    filas = filas + "<td><center><input id='txtninv"+id+"' name='txtninv"+id+"' type='number' min='0' max='2' value=''     class='text-center form-control' placeholder='nro' style='border:1px solid black;'  onkeyup='this.value=validarSoloNumeros(this.value)' required></center></td>";
                }else{
                    n = item.ninvitados
                    filas = filas + "<td><center><input id='txtninv"+id+"' name='txtninv"+id+"' type='number' min='0' max='2' value='"+n+"' class='text-center form-control' placeholder='nro' style='border:1px solid black;' onkeyup='this.value=validarSoloNumeros(this.value)' required></center></td>";
                }

                filas = filas + "<td><center><a onClick='guardarAsistenciaAdm("+id+","+mes+","+yearTitulacion+",\""+fechaFiltro+"\")' class='btn btn-primary'><i class='bi bi-save'></i></a></center></td>";

            filas = filas + "</tr>";
        }
    });
    document.getElementById("tabla_titulados").innerHTML = filas;
}





const guardarAsistenciaAdm = (id, mes, yearTitulacion, fechaFiltro) => {
    let sit=2, ninv=0; nulo=null;
    
    if(document.getElementById("chk"+id).checked === true){
        sit = 1;
    }
    
    ninv = Number(document.getElementById("txtninv"+id).value);
    
    let errores = "";
    if(sit===1 && (ninv <0 || ninv>2)){
        errores = errores + "El Nro de Invitados Debe Estar Entre 0 y 2";
    }

    if(sit===2 && ninv!==0){
        errores = errores + "Al no Asistir, El Nro de Invitados Debe Quedar en Cero.";
    }

    
    if(errores === ""){
        window.location.href="/guardar_asistencia_titulados_adm/"+id+"/"+mes+"/"+yearTitulacion+"/"+sit+"/"+ninv+"/"+fechaFiltro+"/x";
    }else{
        sit=0;   ninv=0;
        window.location.href="/guardar_asistencia_titulados_adm/"+id+"/"+mes+"/"+yearTitulacion+"/"+sit+"/"+ninv+"/"+fechaFiltro+"/"+errores;
        //window.location.href="/guardar_asistencia_titulados_adm/"+id+"/"+mes+"/"+yearTitulacion+"/"+fechaFiltro+"/"+errores;
    }
}






const filtrarPorFechaAdm = (lisbus3, mes, yearTitulacion, fechaFiltro, listaOpcionesFechas) => {
    let res1 = lisbus3;                
    let res2 = lisbus3.replaceAll("&quot;","\"");
    let obj = JSON.parse(res2);

    var e = document.getElementById("cbodia");
    var texto = e.options[e.selectedIndex].text;
    let textocombo = texto.substr(14,21);

    let pfechasitmes = document.getElementById("pfechasitmes").innerHTML;
    alld = document.getElementById("cbodia").value;

    let btn="";
    if(textocombo === "(Abierta)"){
        btn = '<a class="btn btn-primary text-white float-right" onClick="botonGestionarFecha(2, \''+fechaFiltro+'\')"><strong>Cerra Fecha Seleccionada</strong></a>';
    }
    if(textocombo === "(Cerrada)"){
        btn = '<a class="btn btn-primary text-white float-right" onClick="botonGestionarFecha(1, \''+fechaFiltro+'\')"><strong>Abrir Fecha Seleccionada</strong></a>';
    }
    
    if(alld==="allmydata"){
        btn = '<a class="btn btn-primary text-white float-right" onClick="botonGestionarMes('+mes+', '+yearTitulacion+')"><strong>Gestionar Mes</strong></a>';
    }
    
    fechaFiltro = e.value;
    document.getElementById("btnges").innerHTML = btn;

    let filas = "";
    obj["lisbus3"].forEach((item) => {
        nom = item.paterno + " ";
        nom = nom + item.materno + " ";
        nom = nom + item.nombre;
        if(fechaFiltro !== "allmydata"){
            if (item.fechaTitulacion == fechaFiltro){
                if(item.situacion_id===1){
                    filas = filas + "<tr class='table-success'>";
                }else if(item.situacion_id===3){
                    filas = filas + "<tr class='table-warning'>";
                }
                //filas = filas + "<tr>";
                    filas = filas + "<td width='120'>"+item.rut+"</td>";
                    filas = filas + "<td>"+item.paterno+" "+item.materno+" "+item.nombre+"</td>";    
                    filas = filas + "<td>"+item.carrera+"</td>";
                    
                    filas = filas + "<td width='120'>"+item.fechaTitulacion+"</td>";

                    id = item.id;
                    ye = yearTitulacion;
                    
                    id = item.id;
                    marcador = "";
                    if(item.situacion_id === 1 || item.situacion_id === 3){
                        marcador = "checked";
                    }
                    filas = filas + "<td><h3><center><input value=''  id='chk"+id+"' name='chk"+id+"' class='form-check-input' type='checkbox' style='border:1px solid black;' "+marcador+"></center></h3></td>";

                    if(item.ninvitados === null){
                        filas = filas + "<td><center><input id='txtninv"+id+"' name='txtninv"+id+"' type='number' min='0' max='2' value=''     class='text-center form-control' placeholder='nro' style='border:1px solid black;'  onkeyup='this.value=validarSoloNumeros(this.value)' required></center></td>";
                    }else{
                        n = item.ninvitados
                        filas = filas + "<td><center><input id='txtninv"+id+"' name='txtninv"+id+"' type='number' min='0' max='2' value='"+n+"' class='text-center form-control' placeholder='nro' style='border:1px solid black;' onkeyup='this.value=validarSoloNumeros(this.value)' required></center></td>";
                    }

                    filas = filas + "<td><center><a onClick='guardarAsistenciaAdm("+id+","+mes+","+yearTitulacion+",\""+fechaFiltro+"\")' class='btn btn-primary'><i class='bi bi-save'></i></a></center></td>";

                filas = filas + "</tr>";
            }
        }else{
            if(item.situacion_id===1){
                filas = filas + "<tr class='table-success'>";
            }else if(item.situacion_id===3){
                filas = filas + "<tr class='table-warning'>";
            }
            //filas = filas + "<tr>";
                filas = filas + "<td width='120'>"+item.rut+"</td>";
                filas = filas + "<td>"+item.paterno+" "+item.materno+" "+item.nombre+"</td>";    
                filas = filas + "<td>"+item.carrera+"</td>";
                
                filas = filas + "<td width='120'>"+item.fechaTitulacion+"</td>";

                id = item.id;
                ye = yearTitulacion;
                
                id = item.id;
                marcador = "";
                if(item.situacion_id === 1 || item.situacion_id === 3){
                    marcador = "checked";
                }
                filas = filas + "<td><h3><center><input value=''  id='chk"+id+"' name='chk"+id+"' class='form-check-input' type='checkbox' style='border:1px solid black;' "+marcador+"></center></h3></td>";

                if(item.ninvitados === null){
                    filas = filas + "<td><center><input id='txtninv"+id+"' name='txtninv"+id+"' type='number' min='0' max='2' value=''     class='text-center form-control' placeholder='nro' style='border:1px solid black;'  onkeyup='this.value=validarSoloNumeros(this.value)' required></center></td>";
                }else{
                    n = item.ninvitados
                    filas = filas + "<td><center><input id='txtninv"+id+"' name='txtninv"+id+"' type='number' min='0' max='2' value='"+n+"' class='text-center form-control' placeholder='nro' style='border:1px solid black;' onkeyup='this.value=validarSoloNumeros(this.value)' required></center></td>";
                }

                filas = filas + "<td><center><a onClick='guardarAsistenciaAdm("+id+","+mes+","+yearTitulacion+",\""+fechaFiltro+"\")' class='btn btn-primary'><i class='bi bi-save'></i></a></center></td>";

            filas = filas + "</tr>";
        }
    });
    document.getElementById("tabla_titulados").innerHTML = filas;
}





function validarSoloNumeros(string){
    var out = '';
    var filtro = '1234567890';
    
    for (var i=0; i<string.length; i++){
       if (filtro.indexOf(string.charAt(i)) != -1){
         out += string.charAt(i);
       }
    }
    return out;
} 







const filtrarTituladosOrg = (lisbus3, mes, yearTitulacion, fechaFiltro, listaOpcionesFechas) => {
    let res1 = lisbus3;
    let res2 = lisbus3.replaceAll("&quot;","\"");
    let obj = JSON.parse(res2);

    var aux = document.getElementById("txtbus").value.toUpperCase();
    let filas = "";
    obj["lisbus3"].forEach((item) => {
        nom = item.paterno + " ";
        nom = nom + item.materno + " ";
        nom = nom + item.nombre;

        if (fechaFiltro===item.fechaTitulacion && (item.rut.toUpperCase().match(aux) || nom.toUpperCase().match(aux) || item.carrera.toUpperCase().match(aux))){ 
            if(item.situacion_id===1){
                filas = filas + "<tr class='table-success'>";
            }else if(item.situacion_id===3){
                filas = filas + "<tr class='table-warning'>";
            }
                //filas = filas + "<tr>";
                filas = filas + "<td width='120'>"+item.rut+"</td>";
                filas = filas + "<td>"+item.paterno+" "+item.materno+" "+item.nombre+"</td>";    
                filas = filas + "<td>"+item.carrera+"</td>";
                    
                filas = filas + "<td width='120'>"+item.fechaTitulacion+"</td>";

                id = item.id;
                ye = yearTitulacion;
                    
                marcador = "";
                if(item.situacion_id === 1 || item.situacion_id === 3){
                    marcador = "checked";
                }
                filas = filas + "<td><h3><center><input value=''  id='chk"+id+"' name='chk"+id+"' class='form-check-input' type='checkbox' style='border:1px solid black;' "+marcador+"></center></h3></td>";

                if(item.ninvitados === null){
                    filas = filas + "<td><center><input id='txtninv"+id+"' name='txtninv"+id+"' type='number' min='0' max='2' value=''     class='text-center form-control' placeholder='nro' style='border:1px solid black;'  onkeyup='this.value=validarSoloNumeros(this.value)' required></center></td>";
                }else{
                    n = item.ninvitados
                    filas = filas + "<td><center><input id='txtninv"+id+"' name='txtninv"+id+"' type='number' min='0' max='2' value='"+n+"' class='text-center form-control' placeholder='nro' style='border:1px solid black;' onkeyup='this.value=validarSoloNumeros(this.value)' required></center></td>";
                }

                filas = filas + "<td><center><a onClick='guardarAsistencia("+id+","+mes+","+yearTitulacion+",\""+fechaFiltro+"\")' class='btn btn-primary'><i class='bi bi-save'></i></a></center></td>";
            
            filas = filas + "</tr>";
        }else if (fechaFiltro==="allmydata" && (item.rut.toUpperCase().match(aux) || nom.toUpperCase().match(aux) || item.carrera.toUpperCase().match(aux))){ 
            if(item.situacion_id===1){
                filas = filas + "<tr class='table-success'>";
            }else if(item.situacion_id===3){
                filas = filas + "<tr class='table-warning'>";
            }
                filas = filas + "<td width='120'>"+item.rut+"</td>";
                filas = filas + "<td>"+item.paterno+" "+item.materno+" "+item.nombre+"</td>";    
                filas = filas + "<td>"+item.carrera+"</td>";
                
                filas = filas + "<td width='120'>"+item.fechaTitulacion+"</td>";

                id = item.id;
                ye = yearTitulacion;
                
                marcador = "";
                if(item.situacion_id === 1 || item.situacion_id === 3){
                    marcador = "checked";
                }
                filas = filas + "<td><h3><center><input value=''  id='chk"+id+"' name='chk"+id+"' class='form-check-input' type='checkbox' style='border:1px solid black;' "+marcador+"></center></h3></td>";

                if(item.ninvitados === null){
                    filas = filas + "<td><center><input id='txtninv"+id+"' name='txtninv"+id+"' type='number' min='0' max='2' value=''     class='text-center form-control' placeholder='nro' style='border:1px solid black;'  onkeyup='this.value=validarSoloNumeros(this.value)' required></center></td>";
                }else{
                    n = item.ninvitados
                    filas = filas + "<td><center><input id='txtninv"+id+"' name='txtninv"+id+"' type='number' min='0' max='2' value='"+n+"' class='text-center form-control' placeholder='nro' style='border:1px solid black;' onkeyup='this.value=validarSoloNumeros(this.value)' required></center></td>";
                }

                filas = filas + "<td><center><a onClick='guardarAsistencia("+id+","+mes+","+yearTitulacion+",\""+fechaFiltro+"\")' class='btn btn-primary'><i class='bi bi-save'></i></a></center></td>";

            filas = filas + "</tr>";
        }
    });
    document.getElementById("tabla_titulados").innerHTML = filas;
}





const filtrarPorFechaOrg = (lisbus3, mes, yearTitulacion, fechaFiltro) => {
    let res2 = lisbus3.replaceAll("&quot;","\"");
    let obj = JSON.parse(res2);

    var e = document.getElementById("cbodia");

    alld = document.getElementById("cbodia").value;

    let filas = "";
    let cajaPuntual = '';
    obj["lisbus3"].forEach((item) => {
        nom = item.paterno + " ";
        nom = nom + item.materno + " ";
        nom = nom + item.nombre;
        if(fechaFiltro !== "allmydata"){
            if (item.fechaTitulacion == fechaFiltro){
                if(item.situacion_id===1){
                    filas = filas + "<tr class='table-success'>";
                }else if(item.situacion_id===3){
                    filas = filas + "<tr class='table-warning'>";
                }
                //filas = filas + "<tr>";
                    filas = filas + "<td width='120'>"+item.rut+"</td>";
                    filas = filas + "<td>"+item.paterno+" "+item.materno+" "+item.nombre+"</td>";    
                    filas = filas + "<td>"+item.carrera+"</td>";
                    
                    filas = filas + "<td width='120'>"+item.fechaTitulacion+"</td>";

                    id = item.id;
                    ye = yearTitulacion;
                    
                    id = item.id;
                    marcador = "";
                    if(item.situacion_id === 1 || item.situacion_id === 3){
                        marcador = "checked";
                    }
                    filas = filas + "<td><h3><center><input value=''  id='chk"+id+"' name='chk"+id+"' class='form-check-input' type='checkbox' style='border:1px solid black;' "+marcador+"></center></h3></td>";

                    if(item.ninvitados === null){
                        filas = filas + "<td><center><input id='txtninv"+id+"' name='txtninv"+id+"' type='number' min='0' max='2' value=''     class='text-center form-control' placeholder='nro' style='border:1px solid black;'  onkeyup='this.value=validarSoloNumeros(this.value)' required></center></td>";
                    }else{
                        n = item.ninvitados
                        filas = filas + "<td><center><input id='txtninv"+id+"' name='txtninv"+id+"' type='number' min='0' max='2' value='"+n+"' class='text-center form-control' placeholder='nro' style='border:1px solid black;' onkeyup='this.value=validarSoloNumeros(this.value)' required></center></td>";
                    }

                    filas = filas + "<td><center><a onClick='guardarAsistenciaAdm("+id+","+mes+","+yearTitulacion+",\""+fechaFiltro+"\")' class='btn btn-primary'><i class='bi bi-save'></i></a></center></td>";

                filas = filas + "</tr>";
            }
        }else{
            if(item.situacion_id===1){
                filas = filas + "<tr class='table-success'>";
            }else if(item.situacion_id===3){
                filas = filas + "<tr class='table-warning'>";
            }
            //filas = filas + "<tr>";
                filas = filas + "<td width='120'>"+item.rut+"</td>";
                filas = filas + "<td>"+item.paterno+" "+item.materno+" "+item.nombre+"</td>";    
                filas = filas + "<td>"+item.carrera+"</td>";
                
                filas = filas + "<td width='120'>"+item.fechaTitulacion+"</td>";

                id = item.id;
                ye = yearTitulacion;
                
                id = item.id;
                marcador = "";
                if(item.situacion_id === 1 || item.situacion_id === 3){
                    marcador = "checked";
                }
                filas = filas + "<td><h3><center><input value=''  id='chk"+id+"' name='chk"+id+"' class='form-check-input' type='checkbox' style='border:1px solid black;' "+marcador+"></center></h3></td>";

                if(item.ninvitados === null){
                    filas = filas + "<td><center><input id='txtninv"+id+"' name='txtninv"+id+"' type='number' min='0' max='2' value=''     class='text-center form-control' placeholder='nro' style='border:1px solid black;'  onkeyup='this.value=validarSoloNumeros(this.value)' required></center></td>";
                }else{
                    n = item.ninvitados
                    filas = filas + "<td><center><input id='txtninv"+id+"' name='txtninv"+id+"' type='number' min='0' max='2' value='"+n+"' class='text-center form-control' placeholder='nro' style='border:1px solid black;' onkeyup='this.value=validarSoloNumeros(this.value)' required></center></td>";
                }

                filas = filas + "<td><center><a onClick='guardarAsistenciaAdm("+id+","+mes+","+yearTitulacion+",\""+fechaFiltro+"\")' class='btn btn-primary'><i class='bi bi-save'></i></a></center></td>";

            filas = filas + "</tr>";
        }
    });
    document.getElementById("tabla_titulados").innerHTML = filas;
    document.getElementById("cajaTitulados").innerHTML = cajaPuntual;
    console.log(cajaPuntual);
}


