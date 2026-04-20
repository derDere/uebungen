import { readData } from '@repo/data-read/server';
import { writeData } from '@repo/data-write/server';
import { resolve } from 'node:path';
import type { Actions, PageServerLoad } from './$types';

const DATA_DIR = resolve(process.cwd(), '../../data');

export const load: PageServerLoad = async () => {
	const content = await readData(DATA_DIR);
	return { content };
};

export const actions: Actions = {
	write: async ({ request }) => {
		const formData = await request.formData();
		const content = formData.get('content')?.toString() ?? '';
		await writeData(DATA_DIR, content);
		return { success: true };
	}
};
