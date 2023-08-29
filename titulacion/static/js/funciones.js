
const botonCerrarSesion = () => {
    swal({
        title: "Pregunta",
        text: "¿Está Seguro(a) De Querer Cerrar La Sesión?",
        buttons: true,
        dangerMode: true,
      })
      .then((willDelete) => {
        if (willDelete) {
            window.location.href = "/logout";
        }
    });
}



const botonDeshabilitarUsuario = (id) => {
    swal({
        title: "Pregunta",
        text: "¿Está Seguro(a) de Querer Eliminar/Deshabilitar el Registro del Usuario Seleccionado?",
        buttons: true,
        dangerMode: true,
      })
      .then((willDelete) => {
        if (willDelete) {
            window.location.href = "/deshabilitar_usuario/"+ id;                    }
    });
}



const filtrar = (lisbus3) => {
    let res1 = lisbus3;                             // Se recibe el json str desde django.
    //console.log(res1);
    let res2 = lisbus3.replaceAll("&quot;","\"");   // Se le quitan los textos "&quot;".
    let obj = JSON.parse(res2);                     // Se convierte a json de javascript.

    var aux = document.getElementById("txtbus").value.toUpperCase();      // Se captura la palabra buscada.

    let filas = "";
    obj["lisbus3"].forEach((item) => {                      // Recorre todos los registro json recuperados.
        //console.log('RUT: ' + item.rutUsuario);           // Para comprobar.
        //console.log('NOMBRE: ' + item.nomUsuario);        // Para comprobar.
        //console.log('APELLIDO: ' + item.apeUsuario);      // Para comprobar.
        //console.log('TIPO: ' + item["tipo.nomTipo"]);     // Para comprobar.
        
        // Si la palabra buscada coincide con rut, nom, ape o tipo, entonces...
        if (item.rutUsuario.toUpperCase().match(aux) || item.nomUsuario.toUpperCase().match(aux) || item.apeUsuario.toUpperCase().match(aux) || item["tipo.nomTipo"].toUpperCase().match(aux) || item["estado.nomEstado"].toUpperCase().match(aux)){ 
            filas = filas + "<tr>";
                filas = filas + "<td>"+item.rutUsuario+"</td>";
                filas = filas + "<td>"+item.nomUsuario+"</td>";    
                filas = filas + "<td>"+item.apeUsuario+"</td>";    
                filas = filas + "<td>"+item["tipo.nomTipo"]+"</td>";
                if(item["estado.nomEstado"] === "Habilitado"){
                    filas = filas + "<td style='color:green'>"+item["estado.nomEstado"]+"</td>";
                }else{
                    filas = filas + "<td style='color:red'>"+item["estado.nomEstado"]+"</td>";
                }
                
                id = item.id;
                filas = filas + '<td>';
                    filas = filas + '<a href="/form_act_usu/'+id+'" class="btn btn-lg">';
                        filas = filas + '<i class="bi bi-pencil-fill"></i>';
                    filas = filas + '</a>';
                filas = filas + '</td>';
                
                filas = filas + '<td>';
                    filas = filas + '<button type="button" onClick="botonDeshabilitarUsuario('+id+')" class="btn btn-lg">';
                        filas = filas + '<i class="bi bi-trash-fill"></i>';
                    filas = filas + '</button>';
                filas = filas + '</td>';
            filas = filas + '</tr>';
        }
    });
    document.getElementById("tabla_usuarios").innerHTML = filas;
}



async function eliminarYear(year){
    const { value : txtpas } = await Swal.fire({
        icon: 'question',
        title: '<h3>¿Desea Eliminar los Registros del Año '+year+'?</h3>',
        input: 'password',
        inputLabel: 'Digite su Contraseña de Admin para Confirmar!!',
        inputPlaceholder: '******',
        showCancelButton: true,
    });

    if (typeof txtpas !== 'undefined'){
        if(txtpas === ""){
            //console.log("Vacío");
            alertify.error('SE NECESITA LA CONTRASEÑA PARA CONFIRMAR LA ACCIÓN DE ELIMINACIÓN DEL AÑO ' + year);
        }else if(txtpas !== ""){
            //console.log("Contenido : " + txtpas);
            //alertify.success('Success message');
            window.location.href="/delete_year_adm/"+year+"/"+txtpas;
        }
    }
}



function mensajeAlertifyDeleteYear(tipoMsg, textoMsg){
    if(tipoMsg==="success"){
        alertify.success(textoMsg.toUpperCase());
    }else if(tipoMsg==="error"){
        alertify.error(textoMsg.toUpperCase());
    }else if(tipoMsg==="warning"){
        alertify.warning(textoMsg.toUpperCase());
    }
}



function mensajeAlertifyUsu(texto, tipoMsg){
    if(tipoMsg==="success"){
        alertify.success(texto.toUpperCase());
    }else if(tipoMsg==="error"){
        alertify.error(texto.toUpperCase());
    }else if(tipoMsg==="warning"){
        alertify.warning(texto.toUpperCase());
    }
}



function deleteEmptyRows() {
    var myTable = document.getElementById("myTable")
    var rowToDelete = 2;
    myTable.deleteRow(rowToDelete)
}


function contadorDeTitulos(){
    document.getElementById("txthid").value = 0;
}