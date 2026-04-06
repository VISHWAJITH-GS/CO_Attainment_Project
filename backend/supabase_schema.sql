-- Run this SQL in Supabase SQL Editor before starting the app.

-- Keep all record timestamps consistent without requiring manual updates in API code.
create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create table if not exists public.user_profiles (
  id bigint generated always as identity primary key,
  email text not null unique,
  full_name text,
  role text not null default 'Staff',
  department text not null default 'Computer Science and Engineering',
  employee_id text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint user_profiles_tce_email_check check (email ~* '^[A-Za-z0-9._%+-]+@tce\\.edu$')
);

create unique index if not exists user_profiles_employee_id_unique
  on public.user_profiles (employee_id)
  where employee_id is not null;

create table if not exists public.workspace_progress (
  id bigint generated always as identity primary key,
  user_email text not null,
  subject_code text not null,
  uploaded_files jsonb not null default '{}'::jsonb,
  parameters jsonb not null default '{}'::jsonb,
  step integer not null default 1,
  updated_at timestamptz not null default now(),
  constraint workspace_progress_step_check check (step >= 1),
  constraint workspace_progress_tce_email_check check (user_email ~* '^[A-Za-z0-9._%+-]+@tce\\.edu$'),
  unique (user_email, subject_code),
  constraint workspace_progress_user_email_fkey
    foreign key (user_email)
    references public.user_profiles (email)
    on update cascade
    on delete cascade
);

create index if not exists workspace_progress_user_email_updated_at_idx
  on public.workspace_progress (user_email, updated_at desc);

create table if not exists public.reports (
  id bigint generated always as identity primary key,
  user_email text not null,
  subject_code text not null,
  subject_name text,
  semester text,
  status text not null default 'Pending',
  generated_on timestamptz,
  report_text text,
  updated_at timestamptz not null default now(),
  constraint reports_status_check check (status in ('Pending', 'Generated')),
  constraint reports_tce_email_check check (user_email ~* '^[A-Za-z0-9._%+-]+@tce\\.edu$'),
  unique (user_email, subject_code),
  constraint reports_user_email_fkey
    foreign key (user_email)
    references public.user_profiles (email)
    on update cascade
    on delete cascade
);

create index if not exists reports_user_email_updated_at_idx
  on public.reports (user_email, updated_at desc);

create table if not exists public.workspace_files (
  id bigint generated always as identity primary key,
  user_email text not null,
  subject_code text not null,
  file_key text not null,
  file_name text not null,
  content_type text,
  file_size bigint,
  file_base64 text not null,
  updated_at timestamptz not null default now(),
  constraint workspace_files_tce_email_check check (user_email ~* '^[A-Za-z0-9._%+-]+@tce\.edu$'),
  unique (user_email, subject_code, file_key),
  constraint workspace_files_user_email_fkey
    foreign key (user_email)
    references public.user_profiles (email)
    on update cascade
    on delete cascade
);

create index if not exists workspace_files_user_email_subject_idx
  on public.workspace_files (user_email, subject_code);

drop trigger if exists user_profiles_set_updated_at on public.user_profiles;
create trigger user_profiles_set_updated_at
before update on public.user_profiles
for each row
execute function public.set_updated_at();

drop trigger if exists workspace_progress_set_updated_at on public.workspace_progress;
create trigger workspace_progress_set_updated_at
before update on public.workspace_progress
for each row
execute function public.set_updated_at();

drop trigger if exists reports_set_updated_at on public.reports;
create trigger reports_set_updated_at
before update on public.reports
for each row
execute function public.set_updated_at();

drop trigger if exists workspace_files_set_updated_at on public.workspace_files;
create trigger workspace_files_set_updated_at
before update on public.workspace_files
for each row
execute function public.set_updated_at();
