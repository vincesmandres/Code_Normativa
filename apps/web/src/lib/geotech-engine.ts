export type SoilLayer = {
  from: number; to: number; description: string; uscs: string; sample: string;
  n1: number; n2: number; n3: number; moisture: number; gamma: number;
  cohesion: number; friction: number; permeability: number; modulus: number;
};

export type Borehole = {
  id: string; x: number; y: number; elevation: number; finalDepth: number;
  waterDepth: number | null; layers: SoilLayer[];
};

export type GeotechInput = {
  floors: number; columnLoad: number; foundation: string; width: number;
  length: number; diameter: number; groupWidth: number; actualBorings: number;
  actualDepth: number; vs30: number; specialSoil: boolean; serviceLoad: number;
  area: number; qunet: number; qob: number; loadCase: string;
  settlement: number; settlementLimit: number;
};

export type Finding = { state: "pass" | "warn" | "fail"; title: string; detail: string; reference: string };

export const categories = [
  { name: "Baja", borings: 3, depth: 6 }, { name: "Media", borings: 4, depth: 15 },
  { name: "Alta", borings: 4, depth: 25 }, { name: "Especial", borings: 5, depth: 30 },
] as const;

export function categoryIndex(floors: number, load: number) {
  return Math.max(floors <= 3 ? 0 : floors <= 10 ? 1 : floors <= 20 ? 2 : 3,
    load <= 800 ? 0 : load <= 4000 ? 1 : load <= 8000 ? 2 : 3);
}

export function foundationDepth(input: Pick<GeotechInput, "foundation"|"width"|"length"|"diameter"|"groupWidth">) {
  if (input.foundation === "raft") return { value: 1.5 * input.width, basis: "1.5 x ancho de losa" };
  if (input.foundation === "footing") return { value: 2.5 * input.width, basis: "2.5 x ancho de zapata" };
  if (input.foundation === "pile") return { value: input.length + 4 * input.diameter, basis: "longitud + 4 diametros" };
  if (input.foundation === "pile-group") return { value: Math.max(input.length + 2 * input.groupWidth, 2.5 * input.groupWidth), basis: "max(L + 2B grupo, 2.5B cabezal)" };
  return { value: 1.5 * input.length, basis: "1.5 x profundidad de excavacion" };
}

export function classifyProfile(vs30: number, special: boolean) {
  if (special) return { name: "F", detail: "Evaluacion especifica del sitio" };
  if (vs30 >= 1500) return { name: "A", detail: "Vs30 >= 1500 m/s" };
  if (vs30 >= 760) return { name: "B", detail: "760 <= Vs30 < 1500 m/s" };
  if (vs30 >= 360) return { name: "C", detail: "360 <= Vs30 < 760 m/s" };
  if (vs30 >= 180) return { name: "D", detail: "180 <= Vs30 < 360 m/s" };
  return { name: "E", detail: "Vs30 < 180 m/s" };
}

export function evaluateGeotech(input: GeotechInput) {
  const category = categories[categoryIndex(input.floors, input.columnLoad)];
  const depth = foundationDepth(input);
  const requiredDepth = Math.max(category.depth, depth.value);
  const profile = classifyProfile(input.vs30, input.specialSoil);
  const safetyFactor = input.loadCase === "normal" ? 3 : input.loadCase === "maximum" ? 2.5 : 1.5;
  const appliedPressure = input.area > 0 ? input.serviceLoad / input.area : Infinity;
  const allowableCapacity = input.qunet / safetyFactor + input.qob;
  const utilization = allowableCapacity > 0 ? appliedPressure / allowableCapacity : Infinity;
  return { category, depth, requiredDepth, profile, safetyFactor, appliedPressure, allowableCapacity, utilization,
    settlementOk: input.settlement <= input.settlementLimit };
}

export function validateBorehole(borehole: Borehole): string[] {
  const errors: string[] = [];
  if (!borehole.id.trim()) errors.push("La perforacion requiere identificador.");
  if (borehole.finalDepth <= 0) errors.push(`${borehole.id}: profundidad final invalida.`);
  borehole.layers.forEach((layer, index) => {
    if (layer.from < 0 || layer.to <= layer.from) errors.push(`${borehole.id}, estrato ${index + 1}: intervalo invalido.`);
    if (index && Math.abs(layer.from - borehole.layers[index - 1].to) > .001) errors.push(`${borehole.id}: existe vacio o traslape entre estratos ${index} y ${index + 1}.`);
  });
  if (borehole.layers.at(-1)?.to! > borehole.finalDepth + .001) errors.push(`${borehole.id}: los estratos exceden la profundidad final.`);
  return errors;
}

export function materialAtDepth(borehole: Borehole, depth: number) {
  return borehole.layers.find((layer) => depth >= layer.from && depth <= layer.to) ?? null;
}
