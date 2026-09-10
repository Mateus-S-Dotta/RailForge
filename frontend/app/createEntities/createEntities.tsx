import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { FormConfig } from "./forms";
import { url } from "../constrants";

interface params {
	form: FormConfig,
	close: () => void,
	handleChange: (name: string, value: string) => void
}

export default function ElementForm({ form, close, handleChange }: params) {
	async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
		event.preventDefault();

		await fetch(`${url}${form.call}`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(form.result),
		});

		form.campos.forEach((campo) => {
			handleChange(campo.nome, "");
		});
	}

	return (
		<form onSubmit={handleSubmit}>
			<h1>{form.title}</h1>

			{form.campos.map((campo) => (
				<div key={campo.nome}>
					<label htmlFor={campo.nome}>
						{campo.label ?? campo.nome}
					</label>

					<Input
						id={campo.nome}
						name={campo.nome}
						type={campo.type}
						placeholder={campo.placeholder}
						required={campo.required}
						value={String(form.result[campo.nome] ?? "")}
						onChange={(event) =>
							handleChange(campo.nome, event.target.value)
						}
					/>
				</div>
			))}

			<Button type="submit">
				{form.action}
			</Button>
			<Button onClick={close}>
				Cancelar
			</Button>
		</form>
	);
}