export function getAnonymousId() {
  const key = "slop_anon_id";
  let id = localStorage.getItem(key);
  if (!id) {
    id = crypto.randomUUID();   // built into all modern browsers
    localStorage.setItem(key, id);
  }
  return id;
}