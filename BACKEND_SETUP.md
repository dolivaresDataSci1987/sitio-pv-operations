# Backend setup
1. Create a Supabase project.
2. Run `schema.sql` from sitio-pv-operations in Supabase SQL Editor.
3. Add the values from `.streamlit/secrets.example.toml` to each Streamlit deployment's Secrets.
4. Never commit real secrets.

Demo only. The client uses the anon key + RLS; Operations uses the service-role key and must be access-controlled. Before real patient data, replace demo tenant policy with authenticated per-user tenant claims and complete security/privacy controls.
