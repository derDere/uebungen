import { readData } from '@repo/data-read/server';
import { resolve } from 'node:path';
import type { PageServerLoad } from './$types';

const DATA_DIR = resolve(process.cwd(), '../../data');

export const load: PageServerLoad = async () => {
	const content = await readData(DATA_DIR);
	return { content };
};
