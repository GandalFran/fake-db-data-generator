Project IdManagement {
  database_type: 'PostgreSQL'
  Note: '''
    # I+D+i management database
    **Management system for human resources, projects, planification and material database**
  '''
}

Table pacientes {
  id int [pk, increment, not null]
  nombre varchar
  apellido1 varchar
  apellido2 varchar
  fecha_nacimiento timestamp [default: `now()`]
  sexo tipo_sexo
  tarjeta_sanitaria varchar [unique]
  nhc varchar [unique]
  dni varchar [unique]
  nss varchar [unique]
  pasaporte varchar [unique]
  telefono varchar
  email varchar
  direccion varchar 
  municipio varchar 
  provincia varchar 
  codigo_postal varchar
  activo boolean [default:`TRUE`]
}


Table registros{
  id int [pk, increment, not null]
  paciente int
  fecha_dato timestamp [default: `now()`]
  fecha_recepcion timestamp [default: `now()`]
  tipo_registro int
  estado estados_info
  visto boolean
  responsable int [unique]
}

Table campos_registro{
  id int [pk, increment, not null]
  registro int
  fecha timestamp [default: `now()`]
  codigo varchar 
  sistema_codificacion sistemas_de_codificacion 
  dato varchar
  unidades varchar 
  flag estados_info 
}

Table tipos_registro {
  id int [pk, increment, not null]
  nombre varchar
}


Table usuarios{
  id int [pk, increment, not null]
  rol tipo_rol [not null]
  codigo varchar [unique] // el nombre de usuario para usuarios normales, y el id del sensor cuando el rol sea sensor
  foto_url varchar
  password varchar [not null]
  activo boolean [default:`TRUE`] // Note: if the employee is fired, the active flat is set to false
  fecha_creacion timestamp [default: `now()`]
  nombre varchar
  apellido1 varchar
  apellido2 varchar
  email varchar [not null]
  paciente_id int [unique]
}


//aqui se relacionand tanto la asociacion de un paciente con los medicos/enfermeras que deben ser notificados, como la asociacion de identificadores de los sensores con el paciente que lo tiene asignado
Table seguimiento{
  id int [pk, increment, not null]
  usuario int
  paciente int
  fecha_inicio timestamp [default: `now()`]
  fecha_fin timestamp [default: `now()`]
}


Table formulario {
  id int [pk, increment, not null]
  paciente int [not null]
  fecha timestamp [default: `now()`]
  vive_solo varchar
  posibilidad_provisiones varchar
  condiciones_empleo varchar
  vivienda varchar
  saturacion_o2 int
  temperatura float
  fr int
  fc int
  aqi int
  tas float
  tad float
  fiebre boolean
  fatiga boolean
  tos_productiva boolean
  tos_improductiva boolean
  diarrea boolean
  dolor_cabeza boolean
  dolor_garganta boolean
  dolor_muscular boolean
  alteraciones_gusto boolean
  estado_conciencia boolean
  dificultad_respiratoria boolean
  hipotension_arterial boolean
  alteracion_conducta boolean
  signos_clinicos boolean
  hipertension_arterial boolean
  enfermedad_cardiovascular boolean
  diabetes_mellitus boolean
  inmunodeficiencias boolean
  enfermedad_respiratoria_cronica boolean
  habito_de_fumar boolean
  enfermedad_renal_cronica boolean
  enfermedad_hepatica_cronica boolean
  trasplantes boolean
  rs67579710 boolean
  rs35508621 boolean
  rs111837807 boolean
  rs41435745 boolean
  rs505922 boolean
  rs721917 boolean
  rs35705950 boolean
  rs766828 boolean
  rs10774679 boolean
  rs12809318 boolean
  rs117169628 boolean
  rs61667602  boolean
  rs77534576 boolean
  rs2109069 boolean
  rs11085727 boolean
  rs1405655 boolean
  rs13050728 boolean
  tratamiento varchar
  evolucion varchar
  recomendaciones varchar
}

Table estudios {
  id int [pk, increment, not null]
  usuario int [not null]
  paciente int [not null]
  motivo varchar
  fecha timestamp
  estado estado_estudio
}

Table datos_pandemias{
  id int [pk, increment, not null]
  fecha timestamp
  dato int 
  tipo_dato tipo_dato_datos_pandemia
  tipo tipo_datos_pandemia
  modelo modelo_datos_pandemia
}

Ref: registros.paciente > pacientes.id
Ref: registros.tipo_registro > tipos_registro.id
Ref: registros.responsable > usuarios.id

Ref: seguimiento.usuario > usuarios.id
Ref: seguimiento.paciente > pacientes.id

Ref: "pacientes"."id" < "formulario"."paciente"

Ref: "usuarios"."id" < "estudios"."usuario"
Ref: "pacientes"."id" < "estudios"."paciente"

Ref: "pacientes"."id" - "usuarios"."paciente_id"

Enum tipo_sexo {
  hombre
  mujer
  otro
}

Enum estados_info {
  provisional
  consolidado
  alterado
  eliminado
}

Enum tipo_rol {
  admin
  gestor
  clinico
  paciente
  sensor
}

Enum sistemas_de_codificacion {
  LOINC
  SNOMED
  CIE9
  CIE10
  INN
}

Enum estado_estudio{
  pendiente
  aprobado
  denegado
}

Enum tipo_dato_datos_pandemia{
  muertos
  contagiados
  casos_abiertos
}

Enum tipo_datos_pandemia{
  PRD
  RID
}

Enum modelo_datos_pandemia {
  SIR
  SEIR
}