-- Systole : la progression de chaque élève, une ligne par compte.
-- À lancer une fois dans Supabase > SQL Editor, sur un projet neuf.

create table if not exists public.progress (
  user_id uuid primary key references auth.users (id) on delete cascade,
  state jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

alter table public.progress enable row level security;

-- Chaque élève ne lit et n'écrit que sa propre ligne.
create policy "progress_select_own" on public.progress
  for select to authenticated using ((select auth.uid()) = user_id);
create policy "progress_insert_own" on public.progress
  for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "progress_update_own" on public.progress
  for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);

-- Le projet n'expose pas les nouvelles tables automatiquement :
-- on ouvre celle-ci, et seulement aux comptes connectés (y compris anonymes).
grant select, insert, update on public.progress to authenticated;
-- Droits techniques inutiles pour l'app.
revoke truncate, references, trigger on public.progress from anon, authenticated;
