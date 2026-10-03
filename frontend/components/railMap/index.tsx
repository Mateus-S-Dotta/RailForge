import type { LineStation, MapLine } from "@/app/constrants";

interface RailMapProps {
  lines: MapLine[];
  message?: string;
}

export default function RailMap({ lines, message }: RailMapProps) {
  // Uma estação compartilhada por linhas deve ter apenas um marcador.
  const stationsById = new Map<number, LineStation>();
  for (const line of lines) {
    for (const station of line.stations) {
      stationsById.set(station.station_id, station);
    }
  }
  const stations = Array.from(stationsById.values());
  const bounds = stations.reduce(
    (result, station) => ({
      minX: Math.min(result.minX, station.position_x),
      maxX: Math.max(result.maxX, station.position_x),
      minY: Math.min(result.minY, station.position_y),
      maxY: Math.max(result.maxY, station.position_y),
    }),
    { minX: Infinity, maxX: -Infinity, minY: Infinity, maxY: -Infinity },
  );
  const padding = 30;
  const viewBox = stations.length
    ? `${bounds.minX - padding} ${bounds.minY - padding} ${bounds.maxX - bounds.minX + padding * 2} ${bounds.maxY - bounds.minY + padding * 2}`
    : "0 0 600 400";

  return (
    <svg
      className="min-h-0 w-full flex-1"
      viewBox={viewBox}
      preserveAspectRatio="xMidYMid meet"
      role="img"
      aria-label={message || "Mapa das linhas e estações"}
    >
      <title>{message || "Mapa das linhas e estações"}</title>
      {lines.map((line) => (
        <g key={line.id} stroke={line.color || "#94a3b8"} strokeWidth={4}>
          <title>{`${line.name} -> ID: ${line.id}`}</title>
          {line.stations.slice(1).map((station, index) => {
            const previous = line.stations[index];
            return (
              <line
                key={`${previous.station_id}-${station.station_id}`}
                x1={previous.position_x}
                y1={previous.position_y}
                x2={station.position_x}
                y2={station.position_y}
                strokeLinecap="round"
              />
            );
          })}
        </g>
      ))}
      {stations.map((station) => (
        <circle
          key={station.station_id}
          cx={station.position_x}
          cy={station.position_y}
          r={7}
          fill="white"
          stroke="#334155"
          strokeWidth={2}
        >
          <title>{`${station.name} -> ID: ${station.station_id}`}</title>
        </circle>
      ))}
      {stations.length === 0 && (
        <text x={300} y={200} textAnchor="middle" fill="currentColor" fontSize={16}>
          {message || "Nenhuma estação vinculada às linhas."}
        </text>
      )}
    </svg>
  );
}
