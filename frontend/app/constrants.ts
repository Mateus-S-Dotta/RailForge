export const url = 'http://localhost:8000/';

export interface LineStation {
	station_id: number;
	name: string;
	position_x: number;
	position_y: number;
	sequence: number;
}

export interface MapLine {
	id: number;
	name: string;
	color: string | null;
	stations: LineStation[];
}

export interface stationInterface {
	name: string,
	position_y: number,
	position_x: number,
	description: string,
	id: number,
	id_linha: number,
	created_at: string
}
