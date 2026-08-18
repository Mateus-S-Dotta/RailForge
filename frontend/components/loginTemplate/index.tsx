"use client"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import Link from "next/link";
import { useState } from "react";

type input = {
	redirect: string;
	mainButton: string;
	secundaryButton: string;
	func: (login: string, pass: string) => void
}

export default function LoginTemplate({ redirect, mainButton, secundaryButton, func }: input) {
	const [login, setLogin] = useState<string>("");
	const [pass, setPass] = useState<string>("");

	return (
		<>
			<Input placeholder="Login" onChange={(e) => setLogin(e.currentTarget.value)} />
			<Input placeholder="Senha" type="password" onChange={(e) => setPass(e.currentTarget.value)} />
			<Button className="mt-4" onClick={() => func(login, pass)}>
				{mainButton}
			</Button>
			<Button variant="ghost">
				<Link href={`/${redirect}`}>
					{secundaryButton}
				</Link>
			</Button>
		</>
	);
}
