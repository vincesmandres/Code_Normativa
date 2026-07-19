export const PROJECT_KEY = "codenormative.project.v2";
export type ModuleSnapshot = { updatedAt: string; input: Record<string, unknown>; result: Record<string, unknown> };
export type ProjectRecord = { schema: "codenormative.project.v2"; spectrum?: ModuleSnapshot; structural?: ModuleSnapshot; geotech?: ModuleSnapshot };

export function readProject(): ProjectRecord {
  try { return { schema: "codenormative.project.v2", ...JSON.parse(localStorage.getItem(PROJECT_KEY) || "{}") }; }
  catch { return { schema: "codenormative.project.v2" }; }
}

export function saveModule(name: "spectrum"|"structural"|"geotech", input: Record<string, unknown>, result: Record<string, unknown>) {
  const project = readProject();
  project[name] = { updatedAt: new Date().toISOString(), input, result };
  localStorage.setItem(PROJECT_KEY, JSON.stringify(project));
}
