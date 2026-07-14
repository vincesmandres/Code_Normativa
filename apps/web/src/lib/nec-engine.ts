export type SeismicZone = "I" | "II" | "III" | "IV" | "V" | "VI";
export type SoilType = "A" | "B" | "C" | "D" | "E";
export type Region =
  | "Costa (Excepto Esmeralda)"
  | "Sierra, Esmeralda y Galapagos"
  | "Oriente";

export type SpectrumInput = {
  zone: SeismicZone;
  region: Region;
  soil: SoilType;
  rFactor: number;
  importance: number;
  phiP: number;
  phiE: number;
};

export type SpectrumPoint = {
  period: number;
  sa: number;
  se: number;
  si: number;
};

export type SpectrumResult = {
  input: SpectrumInput;
  z: number;
  eta: number;
  fa: number;
  fd: number;
  fs: number;
  falloff: number;
  t0: number;
  tc: number;
  tl: number;
  points: SpectrumPoint[];
};

export const seismicZones: Array<{ value: SeismicZone; label: string }> = [
  { value: "I", label: "I (0.15g)" },
  { value: "II", label: "II (0.25g)" },
  { value: "III", label: "III (0.30g)" },
  { value: "IV", label: "IV (0.35g)" },
  { value: "V", label: "V (0.40g)" },
  { value: "VI", label: "VI (0.50g)" },
];

export const regions: Region[] = [
  "Costa (Excepto Esmeralda)",
  "Sierra, Esmeralda y Galapagos",
  "Oriente",
];

export const soilTypes: Array<{ value: SoilType; label: string }> = [
  { value: "A", label: "A - Roca competente" },
  { value: "B", label: "B - Roca de rigidez media" },
  { value: "C", label: "C - Suelos muy densos o roca blanda" },
  { value: "D", label: "D - Suelos rigidos" },
  { value: "E", label: "E - Suelos blandos" },
];

export const rFactors = [
  { value: 8, label: "8.0 - Porticos especiales sismo resistentes" },
  { value: 7, label: "7.0 - Porticos con vigas banda" },
  { value: 6, label: "6.0 - Porticos intermedios" },
  { value: 5, label: "5.0 - Muros estructurales ductiles" },
  { value: 4, label: "4.0 - Porticos resistentes a momento" },
  { value: 3, label: "3.0 - Mamposteria reforzada" },
  { value: 2.5, label: "2.5 - Estructuras de acero conformado" },
  { value: 1.5, label: "1.5 - Muros de hormigon sin refuerzo" },
  { value: 1, label: "1.0 - Mamposteria sin refuerzo" },
];

export const importanceFactors = [
  { value: 1, label: "1.0 - Estructuras comunes" },
  { value: 1.3, label: "1.3 - Ocupacion especial" },
  { value: 1.5, label: "1.5 - Edificaciones esenciales" },
];

const faValues: Record<SoilType, Record<SeismicZone, number>> = {
  A: { I: 0.9, II: 0.9, III: 0.9, IV: 0.9, V: 0.9, VI: 0.9 },
  B: { I: 1, II: 1, III: 1, IV: 1, V: 1, VI: 1 },
  C: { I: 1.4, II: 1.3, III: 1.25, IV: 1.23, V: 1.2, VI: 1.18 },
  D: { I: 1.6, II: 1.4, III: 1.3, IV: 1.25, V: 1.2, VI: 1.12 },
  E: { I: 1.8, II: 1.4, III: 1.25, IV: 1.1, V: 1, VI: 0.85 },
};

const fdValues: Record<SoilType, Record<SeismicZone, number>> = {
  A: { I: 0.9, II: 0.9, III: 0.9, IV: 0.9, V: 0.9, VI: 0.9 },
  B: { I: 1, II: 1, III: 1, IV: 1, V: 1, VI: 1 },
  C: { I: 1.36, II: 1.28, III: 1.19, IV: 1.15, V: 1.11, VI: 1.06 },
  D: { I: 1.62, II: 1.45, III: 1.36, IV: 1.28, V: 1.19, VI: 1.11 },
  E: { I: 2.1, II: 1.75, III: 1.7, IV: 1.65, V: 1.6, VI: 1.5 },
};

const fsValues: Record<SoilType, Record<SeismicZone, number>> = {
  A: { I: 0.75, II: 0.75, III: 0.75, IV: 0.75, V: 0.75, VI: 0.75 },
  B: { I: 0.75, II: 0.75, III: 0.75, IV: 0.75, V: 0.75, VI: 0.75 },
  C: { I: 0.85, II: 0.94, III: 1.02, IV: 1.06, V: 1.11, VI: 1.23 },
  D: { I: 1.02, II: 1.06, III: 1.11, IV: 1.19, V: 1.28, VI: 1.4 },
  E: { I: 1.5, II: 1.6, III: 1.7, IV: 1.8, V: 1.9, VI: 2 },
};

const falloffValues: Record<SoilType, number> = {
  A: 1,
  B: 1,
  C: 1,
  D: 1,
  E: 1.5,
};

const etaValues: Record<Region, number> = {
  "Costa (Excepto Esmeralda)": 1.8,
  "Sierra, Esmeralda y Galapagos": 2.48,
  Oriente: 2.6,
};

const zValues: Record<SeismicZone, number> = {
  I: 0.15,
  II: 0.25,
  III: 0.3,
  IV: 0.35,
  V: 0.4,
  VI: 0.5,
};

export function calculateSpectrum(input: SpectrumInput): SpectrumResult {
  if (input.rFactor <= 0 || input.importance <= 0 || input.phiP <= 0 || input.phiE <= 0) {
    throw new Error("Todos los factores deben ser mayores que cero.");
  }

  const fa = faValues[input.soil][input.zone];
  const fd = fdValues[input.soil][input.zone];
  const fs = fsValues[input.soil][input.zone];
  const falloff = falloffValues[input.soil];
  const eta = etaValues[input.region];
  const z = zValues[input.zone];
  const t0 = (0.1 * fs * fd) / fa;
  const tc = (0.55 * fs * fd) / fa;
  const tl = 2.4 * fd;
  const points: SpectrumPoint[] = [];

  for (let index = 0; index < 1000; index += 1) {
    const period = (6 * index) / 999;
    let sa = z * fa;

    if (period > 0 && period <= t0) {
      sa = z * fa * (1 + ((eta - 1) * period) / t0);
    } else if (period > t0 && period <= tc) {
      sa = eta * z * fa;
    } else if (period > tc) {
      sa = eta * z * fa * (tc / period) ** falloff;
    }

    const se = sa;
    const si = (input.importance * sa) / (input.rFactor * input.phiP * input.phiE);
    points.push({ period, sa, se, si });
  }

  return { input, z, eta, fa, fd, fs, falloff, t0, tc, tl, points };
}
