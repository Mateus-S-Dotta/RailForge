export type FormField = {
	type: string;
	nome: string;
	label?: string;
	placeholder?: string;
	required?: boolean;
	value?: string;
};

export type FormConfig = {
	call: string;
	title: string;
	action: string;
	campos: FormField[];
	result: Record<string, unknown>;
};

export const formEstacao: FormConfig = {
	call: "stations",
	title: "Criar uma estação",
	action: "Criar Estação",

	campos: [
		{
			type: "text",
			nome: "name",
			label: "Nome",
			placeholder: "Digite o nome",
			required: true,
		},
		{
			type: "text",
			nome: "description",
			label: "Descrição",
			placeholder: "Digite uma descrição",
		},
		{
			type: "number",
			nome: "position_x",
			label: "Posição X",
			placeholder: "Digite Posição X",
			required: true,
		},
		{
			type: "number",
			nome: "position_y",
			label: "Posição Y",
			placeholder: "Digite Posição Y",
			required: true,
		},
	],

	result: {},
};

export const formLine: FormConfig = {
	call: "lines",
	title: "Criar uma linha",
	action: "Criar Linha",

	campos: [
		{
			type: "text",
			nome: "name",
			label: "Nome",
			placeholder: "Digite o nome",
			required: true,
		},
		{
			type: "text",
			nome: "color",
			label: "Cor",
			placeholder: "Digite uma cor (hex)",
		},
	],

	result: {},
};

export const formConections: FormConfig = {
	call: "conections",
	title: "Criar uma conexão",
	action: "Criar Conexão",

	campos: [
		{
			type: "number",
			nome: "id_line",
			label: "Linha Id",
			placeholder: "Digite o Id da Linha",
			required: true,
		},
		{
			type: "text",
			nome: "id_station",
			label: "Estação Id",
			placeholder: "Digite o Id da Estação",
		},
		{
			type: "text",
			nome: "sequence",
			label: "Número na sequencia",
			placeholder: "Digite a posição na linha",
		},
	],

	result: {},
};
