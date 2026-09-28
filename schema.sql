-- SITIO PV Hub shared backend (Supabase/PostgreSQL)
create extension if not exists pgcrypto;

create table if not exists clients (
 id uuid primary key default gen_random_uuid(), slug text unique not null, name text not null,
 pv_status text not null default 'GREEN', created_at timestamptz default now()
);
create table if not exists products (
 id uuid primary key default gen_random_uuid(), client_slug text not null references clients(slug) on delete cascade,
 name text not null, registration text, pv_status text default 'GREEN', next_milestone text, created_at timestamptz default now()
);
create table if not exists projects (
 id uuid primary key default gen_random_uuid(), client_slug text not null references clients(slug) on delete cascade,
 code text unique not null, title text not null, product text, client_status text default 'SITIO trabajando',
 client_progress int default 0 check(client_progress between 0 and 100), client_next_step text, client_need text,
 internal_status text default 'OPEN', internal_priority text default 'Normal', internal_owner text,
 internal_notes text, internal_minutes int default 0, created_at timestamptz default now(), updated_at timestamptz default now()
);
create table if not exists client_requests (
 id uuid primary key default gen_random_uuid(), client_slug text not null references clients(slug) on delete cascade,
 kind text not null, product text, detail text, status text default 'Nueva', created_at timestamptz default now()
);
create table if not exists client_safety_intake (
 id uuid primary key default gen_random_uuid(), client_slug text not null references clients(slug) on delete cascade,
 product text, detail text not null, status text default 'Recibido', created_at timestamptz default now()
);
create table if not exists documents (
 id uuid primary key default gen_random_uuid(), client_slug text not null references clients(slug) on delete cascade,
 project_code text, name text not null, visibility text not null check(visibility in ('CLIENT','INTERNAL')),
 status text, storage_path text, created_at timestamptz default now()
);

create or replace view client_projects as
 select id,client_slug,code,title,product,client_status,client_progress,client_next_step,client_need,created_at,updated_at from projects;
create or replace view client_products as
 select id,client_slug,name,registration,pv_status,next_milestone,created_at from products;
create or replace view client_documents as
 select id,client_slug,project_code,name,status,storage_path,created_at from documents where visibility='CLIENT';

alter table clients enable row level security;
alter table products enable row level security;
alter table projects enable row level security;
alter table client_requests enable row level security;
alter table client_safety_intake enable row level security;
alter table documents enable row level security;

-- DEMO policies: anon may access ONLY the configured demo tenant through these tables/views.
-- Before real clients, replace with Supabase Auth JWT tenant claims.
create policy "demo products read" on products for select to anon using (client_slug='demo-pharma');
create policy "demo projects read" on projects for select to anon using (client_slug='demo-pharma');
create policy "demo documents read" on documents for select to anon using (client_slug='demo-pharma' and visibility='CLIENT');
create policy "demo requests insert" on client_requests for insert to anon with check (client_slug='demo-pharma');
create policy "demo requests read" on client_requests for select to anon using (client_slug='demo-pharma');
create policy "demo safety insert" on client_safety_intake for insert to anon with check (client_slug='demo-pharma');

insert into clients(slug,name) values ('demo-pharma','Demo Pharma Paraguay S.A.') on conflict(slug) do nothing;
insert into products(client_slug,name,registration,pv_status,next_milestone)
select 'demo-pharma','CARDIOMAX 10 mg','DINAVISA DEMO-001','GREEN','Revisión anual'
where not exists(select 1 from products where client_slug='demo-pharma' and name='CARDIOMAX 10 mg');
insert into products(client_slug,name,registration,pv_status,next_milestone)
select 'demo-pharma','GLUCOX 5 mg','DINAVISA DEMO-002','AMBER','PGR'
where not exists(select 1 from products where client_slug='demo-pharma' and name='GLUCOX 5 mg');
insert into projects(client_slug,code,title,client_progress,client_status,client_next_step)
select 'demo-pharma','PV-2026-018','Implementación BPFV',82,'SITIO trabajando','Preparación de presentación ante DINAVISA'
where not exists(select 1 from projects where code='PV-2026-018');
insert into projects(client_slug,code,title,product,client_progress,client_status,client_next_step,client_need)
select 'demo-pharma','PV-2026-021','PGR','GLUCOX 5 mg',54,'Acción requerida','Completar documentación del producto','Subir información de seguridad vigente'
where not exists(select 1 from projects where code='PV-2026-021');
