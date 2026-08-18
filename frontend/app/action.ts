"use server"

async function createUser(login: string, pass: string) {
	console.log(login);
	console.log(pass);
}

async function login(login: string, pass: string) {
	console.log(login);
	console.log(pass);
}

export {
	createUser,
	login,
};