import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';

/**
 * Reads the content of the shared data file.
 * @param dataDir - Absolute path to the data directory containing data.txt
 * @returns The content of data.txt as a string
 */
export async function readData(dataDir: string): Promise<string> {
	const filePath = resolve(dataDir, 'data.txt');
	try {
		return await readFile(filePath, 'utf-8');
	} catch {
		return '';
	}
}
