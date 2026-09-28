import streamlit as st
from database import projects,requests,safety,update_project
st.set_page_config(page_title="SITIO PV Operations",page_icon="⚙️",layout="wide")
st.title("SITIO PV Operations"); st.caption("Centro interno · acceso exclusivo SITIO")
page=st.sidebar.radio("Operations",["Command Center","Project Factory","Solicitudes","Casos de seguridad"])
st.sidebar.error("INTERNO SITIO")
try: ps=projects()
except Exception:
 st.error("Backend no configurado. Añada SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY en los Secrets de este deployment."); st.stop()
if page=="Command Center":
 req=requests(); ev=safety(); a,b,c=st.columns(3); a.metric("Proyectos",len(ps)); b.metric("Solicitudes nuevas",sum(x.get("status")=="Nueva" for x in req)); c.metric("Safety intake",len(ev))
 st.subheader("Necesita intervención"); st.dataframe([{"Proyecto":x["code"],"Cliente":x["client_slug"],"Interno":x.get("internal_status"),"Prioridad":x.get("internal_priority"),"Cliente ve":x.get("client_status")} for x in ps],use_container_width=True,hide_index=True)
elif page=="Project Factory":
 labels={f'{x["code"]} · {x["client_slug"]} · {x["title"]}':x for x in ps}
 if not labels: st.info("Sin proyectos."); st.stop()
 label=st.selectbox("Proyecto",list(labels)); p=labels[label]
 st.subheader("VISIBLE PARA CLIENTE")
 progress=st.slider("Progreso",0,100,p.get("client_progress") or 0); status=st.selectbox("Estado",["SITIO trabajando","Acción requerida","Esperando DINAVISA","Completado"],index=0)
 nxt=st.text_input("Siguiente paso",p.get("client_next_step") or ""); need=st.text_input("Necesitamos del cliente",p.get("client_need") or "")
 st.divider(); st.subheader("INTERNO SITIO — nunca expuesto al portal")
 owner=st.text_input("Responsable interno",p.get("internal_owner") or ""); priority=st.selectbox("Prioridad",["Normal","Alta","Urgente"]); notes=st.text_area("Notas internas",p.get("internal_notes") or ""); mins=st.number_input("Minutos SITIO",0,100000,p.get("internal_minutes") or 0)
 if st.button("Guardar",type="primary"):
  update_project(p["id"],{"client_progress":progress,"client_status":status,"client_next_step":nxt,"client_need":need or None,"internal_owner":owner,"internal_priority":priority,"internal_notes":notes,"internal_minutes":mins}); st.success("Guardado. El portal cliente verá solo los campos externos."); st.rerun()
elif page=="Solicitudes":
 st.dataframe(requests(),use_container_width=True,hide_index=True)
else:
 st.warning("No introducir datos reales de pacientes en la demo."); st.dataframe(safety(),use_container_width=True,hide_index=True)
