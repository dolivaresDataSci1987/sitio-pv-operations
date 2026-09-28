import streamlit as st
from datetime import datetime

st.set_page_config(page_title="SITIO PV Operations",page_icon="⚙️",layout="wide")
st.markdown("""<style>.block-container{max-width:1250px;padding-top:2rem}.red{padding:14px;border-radius:12px;background:#fff1f0;border:1px solid #ffc9c5}.amber{padding:14px;border-radius:12px;background:#fff8e6;border:1px solid #ffe0a3}.green{padding:14px;border-radius:12px;background:#edf9f1;border:1px solid #b9e3c6}</style>""",unsafe_allow_html=True)
st.title("SITIO PV Operations")
st.caption("Centro interno de operaciones · NO accesible a clientes")
page=st.sidebar.radio("Operations",["Command Center","Project Factory","Solicitudes","Clientes","Casos de seguridad","Entregables"])
st.sidebar.warning("INTERNO SITIO")

clients=[{"Cliente":"Demo Pharma Paraguay S.A.","Estado":"🔴 SITIO","Activos":2,"Acción":"Revisar PGR"},{"Cliente":"Laboratorio Guaraní Demo","Estado":"🟠 CLIENTE","Activos":1,"Acción":"Esperando documento"},{"Cliente":"Importadora Salud Demo","Estado":"🟢 OK","Activos":1,"Acción":"Ninguna"}]
if "progress" not in st.session_state: st.session_state.progress=82
if "internal_notes" not in st.session_state: st.session_state.internal_notes=""

if page=="Command Center":
    a,b,c,d=st.columns(4); a.metric("Clientes",30); b.metric("🔴 Requieren SITIO",2); c.metric("🟠 Esperando",3); d.metric("🟢 Sin acción",25)
    st.subheader("🔴 Necesita intervención SITIO")
    st.markdown('<div class="red"><b>Demo Pharma · PV-2026-021 · PGR GLUCOX</b><br>Revisar documentación recibida y definir siguiente acción.</div>',unsafe_allow_html=True)
    st.subheader("🟠 Esperando terceros")
    st.markdown('<div class="amber"><b>Laboratorio Guaraní · BPFV</b><br>Esperando documento del cliente.</div>',unsafe_allow_html=True)
    with st.expander("🟢 25 clientes sin acción"): st.write("No requieren tiempo SITIO ahora.")
elif page=="Project Factory":
    st.header("Project Factory")
    st.selectbox("Proyecto",["PV-2026-018 · Demo Pharma · BPFV Fast Track","PV-2026-021 · Demo Pharma · PGR GLUCOX"])
    st.subheader("Información visible para el cliente")
    st.session_state.progress=st.slider("Progreso visible",0,100,st.session_state.progress)
    st.selectbox("Estado visible",["SITIO trabajando","Acción requerida","Esperando DINAVISA","Completado"])
    st.text_input("Siguiente paso visible","Preparación de presentación ante DINAVISA")
    st.text_input("Necesitamos del cliente","")
    st.divider()
    st.subheader("Información interna SITIO")
    st.selectbox("Responsable interno",["Sin asignar","Lucila","David","Equipo PV"])
    st.selectbox("Prioridad",["Normal","Alta","Urgente"])
    st.session_state.internal_notes=st.text_area("Notas internas — jamás visibles al cliente",st.session_state.internal_notes)
    st.number_input("Minutos SITIO invertidos",0,10000,95)
    st.checkbox("QC interno completado")
    if st.button("Guardar actualización",type="primary"): st.success("Actualización guardada (demo).")
elif page=="Solicitudes":
    st.header("Solicitudes entrantes")
    st.dataframe([{"ID":"REQ-0042","Cliente":"Demo Pharma","Solicitud":"BPFV Fast Track","Estado":"Nueva","Recibida":"Hoy 09:42"},{"ID":"REQ-0041","Cliente":"Demo Pharma","Solicitud":"Consulta producto","Estado":"En revisión","Recibida":"Ayer"}],use_container_width=True,hide_index=True)
elif page=="Clientes":
    st.header("Clientes")
    st.dataframe(clients,use_container_width=True,hide_index=True)
elif page=="Casos de seguridad":
    st.header("Casos de seguridad")
    st.warning("DEMO: no introducir datos reales de pacientes hasta desplegar autenticación, almacenamiento y controles de acceso de producción.")
    st.dataframe([{"Caso":"CASE-DEMO-001","Cliente":"Demo Pharma","Producto":"MED-X 100 mg","Estado":"Triage","Deadline":"Demo"}],use_container_width=True,hide_index=True)
else:
    st.header("Entregables")
    st.dataframe([{"Proyecto":"PV-2026-018","Entregable":"Expediente BPFV","Visibilidad":"CLIENTE","Estado":"Preparación"},{"Proyecto":"PV-2026-018","Entregable":"Checklist interno","Visibilidad":"INTERNO","Estado":"Activo"},{"Proyecto":"PV-2026-021","Entregable":"PGR final","Visibilidad":"CLIENTE","Estado":"Borrador"}],use_container_width=True,hide_index=True)
